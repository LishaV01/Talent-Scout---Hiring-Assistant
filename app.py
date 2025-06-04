import streamlit as st
import os
from datetime import datetime
import json
import re
from typing import Dict, List, Optional
import openai
from dataclasses import dataclass, asdict
import logging
from dotenv import load_dotenv
import time
import threading
from live_UI import (
    apply_minimal_color_changing_theme, 
    create_minimal_header, 
    create_glass_card, 
    create_minimal_progress,
    create_minimal_progress_simple,
    create_pulse_button
)

# Import database module
from database import DatabaseManager, generate_session_id

# Import language manager
from translations import get_language_manager

# Handle different secret sources (MUST BE BEFORE ANY CONFIG USAGE)
def load_secrets():
    """Load secrets from various sources"""
    # First, try Streamlit secrets (for Streamlit Cloud)
    if hasattr(st, 'secrets'):
        try:
            if 'OPENAI_API_KEY' in st.secrets:
                os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
                os.environ['MODEL_NAME'] = st.secrets.get('MODEL_NAME', 'gpt-3.5-turbo')
                os.environ['MAX_TOKENS'] = str(st.secrets.get('MAX_TOKENS', '500'))
                os.environ['TEMPERATURE'] = str(st.secrets.get('TEMPERATURE', '0.7'))
                os.environ['ENABLE_VOICE'] = str(st.secrets.get('ENABLE_VOICE', 'false'))
                return True
        except Exception as e:
            logging.warning(f"Could not load from st.secrets: {e}")
    
    # Then try environment variables (for Docker, Heroku, etc.)
    if os.getenv('OPENAI_API_KEY'):
        return True
    
    # Finally, try .env file (for local development)
    load_dotenv()
    return bool(os.getenv('OPENAI_API_KEY'))

# Load secrets before anything else
secrets_loaded = load_secrets()

# Import VoiceService conditionally
VOICE_AVAILABLE = False
# Only try to import voice if it's enabled
if os.getenv('ENABLE_VOICE', 'false').lower() == 'true':
    try:
        from voice_service import VoiceService
        VOICE_AVAILABLE = True
    except ImportError:
        VOICE_AVAILABLE = False
        logging.warning("Voice service not available. Text-only mode enabled.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
@dataclass
class Config:
    """Application configuration"""
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "500"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    ENABLE_VOICE: bool = os.getenv("ENABLE_VOICE", "false").lower() == "true"
    
config = Config()

# Data Models (keeping the same)
@dataclass
class CandidateInfo:
    """Candidate information structure"""
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    years_experience: Optional[int] = None
    desired_positions: List[str] = None
    current_location: Optional[str] = None
    tech_stack: List[str] = None
    
    def __post_init__(self):
        if self.desired_positions is None:
            self.desired_positions = []
        if self.tech_stack is None:
            self.tech_stack = []
    
    def is_complete(self) -> bool:
        """Check if all required information is collected"""
        return all([
            self.full_name,
            self.email,
            self.phone,
            self.years_experience is not None,
            self.desired_positions,
            self.current_location,
            self.tech_stack
        ])

# Prompt Templates with Language Support
class PromptTemplates:
    """Centralized prompt management with language support"""
    
    @staticmethod
    def get_system_prompt(lang_manager):
        """Get system prompt in current language"""
        return lang_manager.get("system_prompt")
    
    @staticmethod
    def get_greeting(lang_manager):
        """Get greeting in current language"""
        return lang_manager.format_greeting()
    
    @staticmethod
    def get_info_extraction(lang_manager, message: str):
        """Get extraction prompt in current language"""
        extraction_instruction = lang_manager.get_extraction_prompt()
        
        return f"""{extraction_instruction}:
- Full name (can be single name like "Helen", "John", or full names like "John Doe")
- Email address
- Phone number
- Years of experience
- Desired positions (including job titles like developer, tester, engineer, analyst, manager, etc.)
- Current location (city, state, or country names)
- Tech stack

Important notes:
- If the message is a simple name (1-3 words with only letters), extract it as full_name
- Single names like "Helen", "Sarah", "John" should be recognized as full_name
- If the user mentions any job role or position (e.g., "software tester", "tester", "QA engineer", "developer"), extract it as desired_positions
- Simple responses like "tester" or "software tester" should be recognized as desired positions
- If the message is a single word or simple location name (e.g., "Goa", "Mumbai", "Bangalore", "Delhi", "USA"), extract it as current_location
- Location names can be cities, states, or countries - extract them as current_location
- Do NOT extract names as positions
- Names should NOT be interpreted as job positions

User message: "{message}"

Return the extracted information in JSON format. If information is not present, use null.

Examples:
User message: "helen"
Expected output: {{"full_name": "helen"}}

User message: "John Doe"
Expected output: {{"full_name": "John Doe"}}

User message: "software tester"
Expected output: {{"desired_positions": "software tester"}}

User message: "I'm Sarah and I want to be a tester"
Expected output: {{"full_name": "Sarah", "desired_positions": "tester"}}

User message: "goa"
Expected output: {{"current_location": "goa"}}

User message: "Mumbai"
Expected output: {{"current_location": "Mumbai"}}

User message: "I live in Bangalore"
Expected output: {{"current_location": "Bangalore"}}"""
    
    @staticmethod
    def get_next_question(lang_manager, collected_info: Dict, missing_info: List[str]):
        """Get next question prompt in current language"""
        system_prompt = lang_manager.get("system_prompt")
        
        # Use language-specific prompting
        lang_instruction = {
            "en": "Generate an appropriate question to collect the next piece of missing information. Be conversational and natural.",
            "de": "Generieren Sie eine angemessene Frage, um die nächste fehlende Information zu sammeln. Seien Sie gesprächig und natürlich.",
            "hi": "अगली गुम जानकारी एकत्र करने के लिए एक उपयुक्त प्रश्न उत्पन्न करें। संवादात्मक और स्वाभाविक रहें।",
            "kn": "ಮುಂದಿನ ಕಾಣೆಯಾದ ಮಾಹಿತಿಯನ್ನು ಸಂಗ್ರಹಿಸಲು ಸೂಕ್ತವಾದ ಪ್ರಶ್ನೆಯನ್ನು ರಚಿಸಿ. ಸಂಭಾಷಣಾತ್ಮಕ ಮತ್ತು ಸ್ವಾಭಾವಿಕವಾಗಿರಿ.",
            "fr": "Générez une question appropriée pour collecter la prochaine information manquante. Soyez conversationnel et naturel."
        }
        
        instruction = lang_instruction.get(lang_manager.current_language, lang_instruction["en"])
        
        return f"""Based on the conversation so far, the candidate has provided:
{json.dumps(collected_info, indent=2)}

Missing information: {', '.join(missing_info)}

{instruction}"""
    
    @staticmethod
    def get_technical_questions(lang_manager, tech_stack: List[str], years_experience: int):
        """Get technical questions prompt in current language"""
        tech_stack_str = ", ".join(tech_stack)
        
        lang_instruction = {
            "en": f"""Generate 3-5 technical questions for a candidate with the following tech stack:
{tech_stack_str}

The candidate has {years_experience} years of experience.

Generate questions that:
1. Are appropriate for their experience level
2. Cover different aspects of their declared technologies
3. Are specific and practical
4. Can assess real-world knowledge

Format: Return as a JSON array of questions.""",
            
            "de": f"""Generieren Sie 3-5 technische Fragen für einen Kandidaten mit folgendem Technologie-Stack:
{tech_stack_str}

Der Kandidat hat {years_experience} Jahre Erfahrung.

Generieren Sie Fragen, die:
1. Für sein Erfahrungsniveau angemessen sind
2. Verschiedene Aspekte seiner deklarierten Technologien abdecken
3. Spezifisch und praktisch sind
4. Reales Wissen bewerten können

Format: Als JSON-Array von Fragen zurückgeben.""",
            
            "hi": f"""निम्नलिखित तकनीकी स्टैक वाले उम्मीदवार के लिए 3-5 तकनीकी प्रश्न उत्पन्न करें:
{tech_stack_str}

उम्मीदवार के पास {years_experience} वर्षों का अनुभव है।

ऐसे प्रश्न उत्पन्न करें जो:
1. उनके अनुभव स्तर के लिए उपयुक्त हों
2. उनकी घोषित तकनीकों के विभिन्न पहलुओं को कवर करें
3. विशिष्ट और व्यावहारिक हों
4. वास्तविक दुनिया के ज्ञान का आकलन कर सकें

प्रारूप: प्रश्नों के JSON सरणी के रूप में वापस करें।""",
            
            "kn": f"""ಈ ಕೆಳಗಿನ ತಂತ್ರಜ್ಞಾನ ಸ್ಟ್ಯಾಕ್ ಹೊಂದಿರುವ ಅಭ್ಯರ್ಥಿಗಾಗಿ 3-5 ತಾಂತ್ರಿಕ ಪ್ರಶ್ನೆಗಳನ್ನು ರಚಿಸಿ:
{tech_stack_str}

ಅಭ್ಯರ್ಥಿಯು {years_experience} ವರ್ಷಗಳ ಅನುಭವವನ್ನು ಹೊಂದಿದ್ದಾರೆ.

ಈ ಕೆಳಗಿನ ಪ್ರಶ್ನೆಗಳನ್ನು ರಚಿಸಿ:
1. ಅವರ ಅನುಭವದ ಮಟ್ಟಕ್ಕೆ ಸೂಕ್ತವಾಗಿದೆ
2. ಅವರ ಘೋಷಿತ ತಂತ್ರಜ್ಞಾನಗಳ ವಿವಿಧ ಅಂಶಗಳನ್ನು ಒಳಗೊಂಡಿದೆ
3. ನಿರ್ದಿಷ್ಟ ಮತ್ತು ಪ್ರಾಯೋಗಿಕವಾಗಿದೆ
4. ನೈಜ-ಪ್ರಪಂಚದ ಜ್ಞಾನವನ್ನು ಮೌಲ್ಯಮಾಪನ ಮಾಡಬಹುದು

ಸ್ವರೂಪ: ಪ್ರಶ್ನೆಗಳ JSON ಶ್ರೇಣಿಯಾಗಿ ಹಿಂತಿರುಗಿಸಿ.""",
            
            "fr": f"""Générez 3-5 questions techniques pour un candidat avec le stack technique suivant :
{tech_stack_str}

Le candidat a {years_experience} ans d'expérience.

Générez des questions qui :
1. Sont appropriées à leur niveau d'expérience
2. Couvrent différents aspects de leurs technologies déclarées
3. Sont spécifiques et pratiques
4. Peuvent évaluer les connaissances du monde réel

Format : Retourner sous forme de tableau JSON de questions."""
        }
        
        return lang_instruction.get(lang_manager.current_language, lang_instruction["en"])

# Voice Manager with improved cleanup
class VoiceManager:
    """Manage voice interactions"""
    
    def __init__(self, enabled: bool = True):
        self.enabled = enabled and VOICE_AVAILABLE
        self.voice_service = None
        
        if self.enabled:
            try:
                self.voice_service = VoiceService()
                logger.info("Voice service initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize voice service: {e}")
                self.enabled = False
    
    def speak(self, text: str, wait: bool = False):
        """Speak text if voice is enabled"""
        if self.enabled and self.voice_service:
            try:
                logger.info(f"Speaking text: {text[:50]}...")
                self.voice_service.speak(text)
                if wait:
                    # Add timeout to prevent infinite waiting
                    timeout = time.time() + 30  # 30 second timeout
                    while self.voice_service.is_speaking and time.time() < timeout:
                        time.sleep(0.1)
            except Exception as e:
                logger.error(f"Error speaking text: {e}")
    
    def cleanup(self):
        """Clean up voice resources with timeout protection"""
        if self.voice_service:
            try:
                # Stop any ongoing speech first
                if hasattr(self.voice_service, 'is_speaking'):
                    self.voice_service.is_speaking = False
                
                # Add a timeout for cleanup
                def cleanup_with_timeout():
                    try:
                        self.voice_service.cleanup()
                    except:
                        pass
                
                # Run cleanup in a thread with timeout
                cleanup_thread = threading.Thread(target=cleanup_with_timeout)
                cleanup_thread.daemon = True
                cleanup_thread.start()
                cleanup_thread.join(timeout=2.0)  # 2 second timeout
                
                if cleanup_thread.is_alive():
                    logger.warning("Voice cleanup timed out")
                
            except Exception as e:
                logger.error(f"Error cleaning up voice service: {e}")
            finally:
                self.voice_service = None
                self.enabled = False

# LLM Integration
class LLMHandler:
    """Handle interactions with the language model"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
    
    def generate_response(self, messages: List[Dict], temperature: float = 0.7) -> str:
        """Generate a response from the LLM"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=config.MAX_TOKENS
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            lang_manager = get_language_manager()
            return lang_manager.get("error_processing")
    
    def extract_json(self, text: str) -> Optional[Dict]:
        """Extract JSON from LLM response"""
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return None
        except json.JSONDecodeError:
            return None

# Conversation Handler with Language Support
class ConversationHandler:
    """Manage the conversation flow with language support"""
    
    def __init__(self, llm_handler: LLMHandler):
        self.llm = llm_handler
        self.lang_manager = get_language_manager()
        self.end_keywords = ['exit', 'quit', 'stop', 'bye', 'goodbye', 'cancel']
    
    def should_end_conversation(self, message: str) -> bool:
        """Check if conversation should end"""
        return any(keyword in message.lower() for keyword in self.end_keywords)
    
    def extract_candidate_info(self, message: str, current_info: CandidateInfo) -> CandidateInfo:
        """Extract information from user message with improved extraction"""
        
        # First, try to extract email using regex for common email patterns
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, message)
        if email_match and not current_info.email:
            current_info.email = email_match.group()
            logger.info(f"Extracted email via regex: {current_info.email}")
        
        # Check for phone numbers using regex
        phone_pattern = r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,5}[-\s\.]?[0-9]{1,5}'
        phone_match = re.search(phone_pattern, message)
        if phone_match and not current_info.phone and len(phone_match.group()) >= 10:
            current_info.phone = phone_match.group()
            logger.info(f"Extracted phone via regex: {current_info.phone}")
        
        # Check for years of experience
        years_pattern = r'(\d+)\s*(?:years?|yrs?)'
        years_match = re.search(years_pattern, message.lower())
        if years_match and current_info.years_experience is None:
            try:
                current_info.years_experience = int(years_match.group(1))
                logger.info(f"Extracted years via regex: {current_info.years_experience}")
            except ValueError:
                pass
        
        # Simple name detection - if we're expecting a name and get a simple text response
        if not current_info.full_name and len(message.split()) <= 3:
            # Check if it looks like a name (only letters and spaces, no special chars except apostrophe/hyphen)
            name_pattern = r"^[A-Za-z\s\-']+$"
            if re.match(name_pattern, message.strip()):
                # Don't trigger position extraction for simple names
                potential_name = message.strip()
                # Check it's not a common position keyword by itself
                position_keywords = ['tester', 'developer', 'engineer', 'analyst', 'manager', 'designer',
                                   'architect', 'consultant', 'specialist', 'lead', 'programmer',
                                   'administrator', 'devops', 'qa', 'scientist', 'intern', 'associate']
                if potential_name.lower() not in position_keywords:
                    current_info.full_name = potential_name
                    logger.info(f"Extracted name via pattern: {current_info.full_name}")
        
        # Simple location detection - if we're expecting a location and get a simple text response
        if not current_info.current_location and len(message.split()) <= 3:
            # Check if it looks like a location (only letters, spaces, and common location chars)
            location_pattern = r"^[A-Za-z\s\-,\.]+$"
            if re.match(location_pattern, message.strip()):
                potential_location = message.strip()
                # Don't extract if it's a known position keyword
                position_keywords = ['tester', 'developer', 'engineer', 'analyst', 'manager', 'designer',
                                   'architect', 'consultant', 'specialist', 'lead', 'programmer',
                                   'administrator', 'devops', 'qa', 'scientist', 'intern', 'associate']
                # Also check it's not a simple name that was already extracted
                if (potential_location.lower() not in position_keywords and 
                    potential_location != current_info.full_name):
                    # If we need a location (other fields are mostly filled), accept any reasonable text
                    missing_fields = []
                    if not current_info.full_name: missing_fields.append("name")
                    if not current_info.email: missing_fields.append("email") 
                    if not current_info.phone: missing_fields.append("phone")
                    if current_info.years_experience is None: missing_fields.append("experience")
                    if not current_info.desired_positions: missing_fields.append("positions")
                    if not current_info.tech_stack: missing_fields.append("tech")
                    
                    # If we only need location (or location + 1 other field), accept this as location
                    if len(missing_fields) <= 1:
                        current_info.current_location = potential_location
                        logger.info(f"Extracted location via pattern: {current_info.current_location}")
        
        # Now use LLM for more complex extraction
        prompt = PromptTemplates.get_info_extraction(self.lang_manager, message)
        
        messages = [
            {"role": "system", "content": PromptTemplates.get_system_prompt(self.lang_manager)},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.generate_response(messages, temperature=0.3)
        logger.info(f"LLM extraction response: {response}")
        
        extracted = self.llm.extract_json(response)
        
        if extracted:
            logger.info(f"Extracted data: {extracted}")
            
            # Update candidate info with extracted data
            if extracted.get('full_name') and not current_info.full_name:
                current_info.full_name = extracted['full_name']
            
            # Only update email if we didn't already extract it via regex
            if extracted.get('email') and not current_info.email:   
                current_info.email = extracted['email']
            
            # Only update phone if we didn't already extract it via regex
            if extracted.get('phone') and not current_info.phone:
                current_info.phone = extracted['phone']
            
            # Only update years if we didn't already extract it via regex
            if extracted.get('years_experience') is not None and current_info.years_experience is None:
                try:
                    current_info.years_experience = int(extracted['years_experience'])
                except (ValueError, TypeError):
                    pass
            
            if extracted.get('desired_positions'):
                positions = extracted['desired_positions']
                if isinstance(positions, list):
                    # Avoid duplicates
                    existing_lower = [p.lower() for p in current_info.desired_positions]
                    for pos in positions:
                        if pos.lower() not in existing_lower:
                            current_info.desired_positions.append(pos)
                else:
                    if positions.lower() not in [p.lower() for p in current_info.desired_positions]:
                        current_info.desired_positions.append(positions)
            
            if extracted.get('current_location') and not current_info.current_location:
                current_info.current_location = extracted['current_location']
            
            if extracted.get('tech_stack'):
                tech = extracted['tech_stack']
                if isinstance(tech, list):
                    # Convert to lowercase to check for duplicates
                    existing_lower = [t.lower() for t in current_info.tech_stack]
                    for item in tech:
                        if item.lower() not in existing_lower:
                            current_info.tech_stack.append(item)
                else:
                    if tech.lower() not in [t.lower() for t in current_info.tech_stack]:
                        current_info.tech_stack.append(tech)
        
        # Quick position extraction fallback - ONLY if no positions found AND message contains position keywords
        if (not current_info.desired_positions or len(current_info.desired_positions) == 0) and not current_info.full_name:
            # List of position-related keywords
            position_indicators = [
                'tester', 'developer', 'engineer', 'analyst', 'manager', 'designer',
                'architect', 'consultant', 'specialist', 'lead', 'programmer',
                'administrator', 'devops', 'qa', 'scientist', 'intern', 'associate'
            ]
            
            # Use word boundaries for exact matching
            message_lower = message.lower()
            for indicator in position_indicators:
                # Check for exact word match, not substring
                pattern = r'\b' + re.escape(indicator) + r'\b'
                if re.search(pattern, message_lower):
                    # Found a position-related word, use the full message as position
                    position_to_add = message.strip()
                    if position_to_add and len(position_to_add) < 50:
                        current_info.desired_positions.append(position_to_add)
                        logger.info(f"Extracted position via fallback: {position_to_add}")
                    break
        
        # Log current state for debugging
        logger.info(f"Current candidate info: {asdict(current_info)}")
        
        return current_info
    
    def get_missing_info(self, candidate_info: CandidateInfo) -> List[str]:
        """Identify missing information"""
        missing = []
        if not candidate_info.full_name:
            missing.append("full name")
        if not candidate_info.email:
            missing.append("email address")
        if not candidate_info.phone:
            missing.append("phone number")
        if candidate_info.years_experience is None:
            missing.append("years of experience")
        if not candidate_info.desired_positions:
            missing.append("desired position(s)")
        if not candidate_info.current_location:
            missing.append("current location")
        if not candidate_info.tech_stack:
            missing.append("tech stack")
        return missing
    
    def generate_next_question(self, candidate_info: CandidateInfo) -> str:
        """Generate the next question based on missing information"""
        missing = self.get_missing_info(candidate_info)
        if not missing:
            return None
        
        # For simple cases, use predefined questions
        if len(missing) == 1:
            return self.lang_manager.format_next_question(missing[0])
        
        # For complex cases, use LLM
        collected = {
            "full_name": candidate_info.full_name,
            "email": candidate_info.email,
            "phone": candidate_info.phone,
            "years_experience": candidate_info.years_experience,
            "desired_positions": candidate_info.desired_positions,
            "current_location": candidate_info.current_location,
            "tech_stack": candidate_info.tech_stack
        }
        
        prompt = PromptTemplates.get_next_question(self.lang_manager, collected, missing)
        
        messages = [
            {"role": "system", "content": PromptTemplates.get_system_prompt(self.lang_manager)},
            {"role": "user", "content": prompt}
        ]
        
        return self.llm.generate_response(messages)
    
    def generate_technical_questions(self, candidate_info: CandidateInfo) -> List[str]:
        """Generate technical questions based on tech stack"""
        prompt = PromptTemplates.get_technical_questions(
            self.lang_manager,
            candidate_info.tech_stack,
            candidate_info.years_experience
        )
        
        messages = [
            {"role": "system", "content": PromptTemplates.get_system_prompt(self.lang_manager)},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.generate_response(messages, temperature=0.5)
        questions = self.llm.extract_json(response)
        
        if isinstance(questions, list):
            return questions
        elif isinstance(questions, dict) and 'questions' in questions:
            return questions['questions']
        else:
            # Fallback questions
            return [
                f"Can you describe your experience with {candidate_info.tech_stack[0] if candidate_info.tech_stack else 'your primary technology'}?",
                "What's the most challenging technical problem you've solved recently?",
                "How do you stay updated with new technologies in your field?"
            ]
    
    def generate_farewell(self) -> str:
        """Generate farewell message"""
        return self.lang_manager.get("farewell")

# Reset conversation function
def reset_conversation():
    """Safely reset the conversation and all session state"""
    try:
        # 1. Clean up voice resources with timeout
        if 'voice_manager' in st.session_state and st.session_state.voice_manager:
            try:
                # Set a flag to prevent any ongoing speech
                if hasattr(st.session_state.voice_manager, 'voice_service'):
                    st.session_state.voice_manager.voice_service.is_speaking = False
                
                # Clean up resources
                st.session_state.voice_manager.cleanup()
            except Exception as e:
                logger.warning(f"Voice cleanup error (non-critical): {e}")
        
        # 2. Close database connections if any
        if 'db_manager' in st.session_state and st.session_state.db_manager:
            try:
                # If your DatabaseManager has a close method, call it
                if hasattr(st.session_state.db_manager, 'close'):
                    st.session_state.db_manager.close()
            except Exception as e:
                logger.warning(f"Database cleanup error (non-critical): {e}")
        
        # 3. Clear session state completely
        st.session_state.clear()
        
    except Exception as e:
        logger.error(f"Error during reset: {e}")
        # Even if there's an error, try to clear session state
        try:
            st.session_state.clear()
        except:
            pass
    
    # 4. Force a complete page reload
    st.rerun()

# Streamlit UI
def init_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'candidate_info' not in st.session_state:
        st.session_state.candidate_info = CandidateInfo()
    if 'phase' not in st.session_state:
        st.session_state.phase = 'greeting'  # greeting, info_gathering, technical_questions, completed
    if 'technical_questions' not in st.session_state:
        st.session_state.technical_questions = []
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False
    if 'voice_manager' not in st.session_state:
        st.session_state.voice_manager = None
    if 'voice_greeted' not in st.session_state:
        st.session_state.voice_greeted = False
    # Add this line to persist voice enabled state
    if 'voice_enabled' not in st.session_state:
        st.session_state.voice_enabled = config.ENABLE_VOICE
    # Add language state
    if 'selected_language' not in st.session_state:
        st.session_state.selected_language = 'en'
    # Add language change tracking
    if 'previous_language' not in st.session_state:
        st.session_state.previous_language = 'en'
    # Add this to track if language was initialized
    if 'language_initialized' not in st.session_state:
        st.session_state.language_initialized = False
    # Add selectbox counter for forcing widget refresh
    if 'selectbox_counter' not in st.session_state:
        st.session_state.selectbox_counter = 0
    
    # Initialize database and session
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = DatabaseManager()
    if 'session_id' not in st.session_state:
        st.session_state.session_id = generate_session_id()
    if 'candidate_id' not in st.session_state:
        st.session_state.candidate_id = None
    if 'last_technical_answer' not in st.session_state:
        st.session_state.last_technical_answer = None
    if 'pending_update' not in st.session_state:
        st.session_state.pending_update = False
    if 'update_field' not in st.session_state:
        st.session_state.update_field = None

def save_candidate_to_db():
    """Save current candidate info to database"""
    try:
        candidate_id = st.session_state.db_manager.create_or_update_candidate(
            st.session_state.session_id,
            st.session_state.candidate_info
        )
        st.session_state.candidate_id = candidate_id
        return candidate_id
    except Exception as e:
        logger.error(f"Failed to save candidate to database: {e}")
        return None

def save_message_to_db(role: str, content: str):
    """Save conversation message to database"""
    try:
        if st.session_state.candidate_id:
            st.session_state.db_manager.save_conversation_log(
                st.session_state.candidate_id,
                role,
                content
            )
    except Exception as e:
        logger.error(f"Failed to save message to database: {e}")

def display_chat_history():
    """Display chat history"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def calculate_progress(candidate_info: CandidateInfo) -> float:
    """Calculate completion progress"""
    fields = [
        candidate_info.full_name,
        candidate_info.email,
        candidate_info.phone,
        candidate_info.years_experience is not None,
        len(candidate_info.desired_positions) > 0,
        candidate_info.current_location,
        len(candidate_info.tech_stack) > 0
    ]
    completed = sum(1 for field in fields if field)
    return (completed / len(fields)) * 100

def main():
    """Main application"""
    st.set_page_config(
        page_title="TalentScout Hiring Assistant",
        page_icon="🤖",
        layout="centered"
    )
    
    # Apply minimal color-changing theme
    apply_minimal_color_changing_theme()
    
    # Initialize session state
    init_session_state()
    
    # Get language manager
    lang_manager = get_language_manager()
    
    # Check if language has already been set for this session
    if 'language_initialized' not in st.session_state:
        lang_manager.set_language(st.session_state.selected_language)
        st.session_state.language_initialized = True
    
    # Header with minimal design
    create_minimal_header(lang_manager.get("app_title"), lang_manager.get("app_subtitle"))
    
    # Initialize voice manager based on session state
    if VOICE_AVAILABLE and st.session_state.voice_enabled and st.session_state.voice_manager is None:
        st.session_state.voice_manager = VoiceManager(enabled=True)
    
    # Sidebar with minimal design
    with st.sidebar:
        st.markdown(f"### {lang_manager.get('about')}")
        create_glass_card(lang_manager.get("about_text"))
        
        # Language selector
        st.markdown("---")
        st.markdown(f"### {lang_manager.get('select_language')}")
        languages = lang_manager.get_supported_languages()
        
        # Create language options
        language_options = {f"{lang['flag']} {lang['name']}": lang['code'] for lang in languages}
        current_language_display = f"{lang_manager.get_language_flag()} {lang_manager.get_language_name()}"
        
        # Create a unique key for the selectbox to prevent glitching
        selectbox_key = f"lang_select_{st.session_state.get('selectbox_counter', 0)}"
        
        selected_language_display = st.selectbox(
            "",
            options=list(language_options.keys()),
            index=list(language_options.values()).index(st.session_state.selected_language),
            label_visibility="collapsed",
            key=selectbox_key  # Unique key prevents widget conflicts
        )
        
        new_language = language_options[selected_language_display]
        
        # If language changed, show options instead of immediate reset
        if new_language != st.session_state.selected_language:
            if st.session_state.conversation_started and len(st.session_state.messages) > 1:
                st.warning(f"⚠️ Changing language will update the interface.")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Continue", type="primary", use_container_width=True):
                        st.session_state.selected_language = new_language
                        st.session_state.previous_language = lang_manager.current_language
                        lang_manager.set_language(new_language)
                        # Increment selectbox counter to force new key
                        st.session_state.selectbox_counter = st.session_state.get('selectbox_counter', 0) + 1
                        st.rerun()
                with col2:
                    if st.button("Start Fresh", type="secondary", use_container_width=True):
                        st.session_state.selected_language = new_language
                        lang_manager.set_language(new_language)
                        reset_conversation()
            else:
                # No conversation started, just switch smoothly
                st.session_state.selected_language = new_language
                st.session_state.previous_language = lang_manager.current_language
                lang_manager.set_language(new_language)
                # Increment selectbox counter to force new key
                st.session_state.selectbox_counter = st.session_state.get('selectbox_counter', 0) + 1
                st.rerun()
        
        # Voice control toggle
        if VOICE_AVAILABLE:
            # Use session state for checkbox
            voice_enabled = st.checkbox(
                f"🔊 {lang_manager.get('enable_voice')}", 
                value=st.session_state.voice_enabled,
                key="voice_checkbox",
                help=lang_manager.get("enable_voice")
            )
            
            # Update session state when checkbox changes
            if voice_enabled != st.session_state.voice_enabled:
                st.session_state.voice_enabled = voice_enabled
                
                # Initialize or update voice manager
                if voice_enabled:
                    if st.session_state.voice_manager is None:
                        st.session_state.voice_manager = VoiceManager(enabled=True)
                    else:
                        st.session_state.voice_manager.enabled = True
                else:
                    if st.session_state.voice_manager:
                        st.session_state.voice_manager.enabled = False
        
        # Reset button with better implementation
        st.markdown("---")  # Add separator
        if st.button(f"🔄 {lang_manager.get('reset_conversation')}", type="secondary", use_container_width=True):
            reset_conversation()
        
        # Debug info section
        if st.checkbox(lang_manager.get("show_debug_info")):
            st.markdown("---")
            st.markdown(f"### {lang_manager.get('collected_data')}")
            info = st.session_state.candidate_info
            debug_text = f"""
**{lang_manager.get('name')}:** {info.full_name or lang_manager.get('not_collected')}
**{lang_manager.get('email')}:** {info.email or lang_manager.get('not_collected')}
**{lang_manager.get('phone')}:** {info.phone or lang_manager.get('not_collected')}
**{lang_manager.get('experience')}:** {str(info.years_experience) + ' ' + lang_manager.get('years') if info.years_experience is not None else lang_manager.get('not_collected')}
**{lang_manager.get('positions')}:** {', '.join(info.desired_positions) if info.desired_positions else lang_manager.get('not_collected')}
**{lang_manager.get('location')}:** {info.current_location or lang_manager.get('not_collected')}
**{lang_manager.get('tech_stack')}:** {', '.join(info.tech_stack) if info.tech_stack else lang_manager.get('not_collected')}
**{lang_manager.get('phase')}:** {st.session_state.phase}
**Language:** {lang_manager.current_language}
**{lang_manager.get('voice_enabled')}:** {st.session_state.voice_enabled if VOICE_AVAILABLE else lang_manager.get('not_available')}
**{lang_manager.get('voice_manager')}:** {lang_manager.get('initialized') if st.session_state.voice_manager else lang_manager.get('not_initialized')}
**{lang_manager.get('session_id')}:** {st.session_state.session_id[:8]}...
**{lang_manager.get('candidate_id')}:** {st.session_state.candidate_id or lang_manager.get('not_saved_yet')}
            """
            st.markdown(debug_text)
    
    # Check if API key is configured
    if not config.OPENAI_API_KEY:
        st.error("⚠️ OpenAI API key not found!")
        
        with st.expander("📖 Setup Instructions"):
            st.markdown("""
            ### For Streamlit Cloud:
            1. Go to your app settings
            2. Click on 'Secrets' in the left menu
            3. Add your OpenAI API key:
            ```toml
            OPENAI_API_KEY = "your-api-key-here"
            ```
            
            ### For Local Development:
            1. Create a `.env` file in your project root
            2. Add your OpenAI API key:
            ```
            OPENAI_API_KEY=your-api-key-here
            ```
            
            ### For Other Platforms:
            Set the `OPENAI_API_KEY` environment variable in your platform's dashboard.
            """)
        
        st.stop()
    
    # Initialize handlers
    llm_handler = LLMHandler(config.OPENAI_API_KEY)
    conversation_handler = ConversationHandler(llm_handler)
    # Update conversation handler's language manager
    conversation_handler.lang_manager = lang_manager
    
    # Show progress bar if in info gathering phase
    if st.session_state.phase in ['info_gathering', 'technical_questions'] and st.session_state.candidate_info.full_name:
        progress = calculate_progress(st.session_state.candidate_info)
        # Pass candidate_info to show detailed field completion
        create_minimal_progress(progress, segments=10, candidate_info=st.session_state.candidate_info)
    
    # Start conversation with greeting
    if not st.session_state.conversation_started:
        greeting = PromptTemplates.get_greeting(lang_manager)
        st.session_state.messages.append({
            "role": "assistant",
            "content": greeting
        })
        st.session_state.conversation_started = True
        # Save greeting to database
        save_message_to_db("assistant", greeting)
    
    # Display chat history
    display_chat_history()
    
    # Speak greeting if not already done
    if st.session_state.conversation_started and not st.session_state.voice_greeted and st.session_state.voice_manager and st.session_state.voice_enabled:
        st.session_state.voice_manager.speak(PromptTemplates.get_greeting(lang_manager))
        st.session_state.voice_greeted = True
    
    # Save technical answer if there was one from previous interaction
    if st.session_state.last_technical_answer and st.session_state.candidate_id:
        try:
            st.session_state.db_manager.save_technical_answer(
                st.session_state.candidate_id,
                st.session_state.current_question_index - 1,
                st.session_state.last_technical_answer
            )
            st.session_state.last_technical_answer = None
        except Exception as e:
            logger.error(f"Failed to save technical answer: {e}")
    
    # User input
    if prompt := st.chat_input(lang_manager.get("type_message")):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        save_message_to_db("user", prompt)
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # If in technical questions phase, save the answer (unless it's an update request)
        if st.session_state.phase == 'technical_questions' and st.session_state.candidate_id:
            # Check if this is an update request
            update_keywords = ['update', 'change', 'modify', 'correct', 'edit']
            info_keywords = ['location', 'email', 'phone', 'name', 'position', 'tech stack']
            
            is_update_request = (any(keyword in prompt.lower() for keyword in update_keywords) and 
                               any(keyword in prompt.lower() for keyword in info_keywords))
            
            # Don't save as technical answer if it's an update request or we're in update mode
            if not is_update_request and not getattr(st.session_state, 'pending_update', False):
                st.session_state.last_technical_answer = prompt
        
        # Check for end keywords
        if conversation_handler.should_end_conversation(prompt):
            farewell = conversation_handler.generate_farewell()
            st.session_state.messages.append({"role": "assistant", "content": farewell})
            save_message_to_db("assistant", farewell)
            with st.chat_message("assistant"):
                st.markdown(farewell)
            # Speak farewell if voice is enabled
            if st.session_state.voice_manager and st.session_state.voice_enabled:
                st.session_state.voice_manager.speak(farewell)
            st.session_state.phase = 'completed'
            st.stop()
        
        # Process based on current phase
        with st.chat_message("assistant"):
            with st.spinner(lang_manager.get("thinking")):
                if st.session_state.phase == 'greeting' or st.session_state.phase == 'info_gathering':
                    # Extract information from user message
                    st.session_state.candidate_info = conversation_handler.extract_candidate_info(
                        prompt, 
                        st.session_state.candidate_info
                    )
                    
                    # Save candidate info to database
                    save_candidate_to_db()
                    
                    # Check if all information is collected
                    if st.session_state.candidate_info.is_complete():
                        # Transition to technical questions
                        st.session_state.phase = 'technical_questions'
                        st.session_state.technical_questions = conversation_handler.generate_technical_questions(
                            st.session_state.candidate_info
                        )
                        
                        # Save technical questions to database
                        if st.session_state.candidate_id:
                            try:
                                st.session_state.db_manager.save_technical_questions(
                                    st.session_state.candidate_id,
                                    st.session_state.technical_questions
                                )
                            except Exception as e:
                                logger.error(f"Failed to save technical questions: {e}")
                        
                        # Generate technical intro
                        response = lang_manager.format_tech_intro(
                            st.session_state.candidate_info.full_name,
                            st.session_state.candidate_info.tech_stack
                        )
                        response += f"\n\n**{lang_manager.format_question(1, len(st.session_state.technical_questions))}**\n{st.session_state.technical_questions[0]}"
                        
                        st.session_state.current_question_index = 0
                    else:
                        # Ask for missing information
                        response = conversation_handler.generate_next_question(st.session_state.candidate_info)
                        st.session_state.phase = 'info_gathering'
                    
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    save_message_to_db("assistant", response)
                    
                    # Speak the response if voice is enabled
                    if st.session_state.voice_manager and st.session_state.voice_enabled:
                        st.session_state.voice_manager.speak(response)
                
                elif st.session_state.phase == 'technical_questions':
                    # Check if user wants to update information
                    update_keywords = ['update', 'change', 'modify', 'correct', 'edit']
                    info_keywords = ['location', 'email', 'phone', 'name', 'position', 'tech stack']
                    
                    wants_to_update = any(keyword in prompt.lower() for keyword in update_keywords)
                    mentions_info = any(keyword in prompt.lower() for keyword in info_keywords)
                    
                    if wants_to_update and mentions_info:
                        # Handle information update request
                        response = lang_manager.get("update_request")
                        
                        # Set a flag to process the next message as an update
                        st.session_state.pending_update = True
                        st.session_state.update_field = None
                        
                        # Try to identify what they want to update
                        if 'location' in prompt.lower():
                            st.session_state.update_field = 'location'
                            response = lang_manager.get("update_location")
                        elif 'email' in prompt.lower():
                            st.session_state.update_field = 'email'
                            response = lang_manager.get("update_email")
                        elif 'phone' in prompt.lower():
                            st.session_state.update_field = 'phone'
                            response = lang_manager.get("update_phone")
                            
                    elif hasattr(st.session_state, 'pending_update') and st.session_state.pending_update:
                        # Process the update
                        st.session_state.pending_update = False
                        
                        # Extract and update the information
                        updated_info = conversation_handler.extract_candidate_info(prompt, st.session_state.candidate_info)
                        
                        # If we know which field to update specifically
                        if hasattr(st.session_state, 'update_field') and st.session_state.update_field:
                            if st.session_state.update_field == 'location':
                                st.session_state.candidate_info.current_location = prompt.strip()
                            elif st.session_state.update_field == 'email':
                                email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', prompt)
                                if email_match:
                                    st.session_state.candidate_info.email = email_match.group()
                            elif st.session_state.update_field == 'phone':
                                phone_match = re.search(r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,5}[-\s\.]?[0-9]{1,5}', prompt)
                                if phone_match and len(phone_match.group()) >= 10:
                                    st.session_state.candidate_info.phone = phone_match.group()
                        else:
                            # General update based on extraction
                            st.session_state.candidate_info = updated_info
                        
                        # Save updated info to database
                        save_candidate_to_db()
                        
                        # Resume technical questions
                        response = f"""{lang_manager.get("update_confirmed")}

**{lang_manager.format_question(st.session_state.current_question_index + 1, len(st.session_state.technical_questions))}**
{st.session_state.technical_questions[st.session_state.current_question_index]}"""
                        
                        st.session_state.update_field = None
                        
                    else:
                        # Normal technical question flow - save the answer and move to next
                        st.session_state.current_question_index += 1
                        
                        if st.session_state.current_question_index < len(st.session_state.technical_questions):
                            response = f"""{lang_manager.get("thank_you_answer")}

**{lang_manager.format_question(st.session_state.current_question_index + 1, len(st.session_state.technical_questions))}**
{st.session_state.technical_questions[st.session_state.current_question_index]}"""
                        else:
                            # All questions answered
                            st.session_state.phase = 'completed'
                            response = conversation_handler.generate_farewell()
                            
                            # Display candidate summary in a glass card
                            info = st.session_state.candidate_info
                            
                            summary_content = f"""
### 👤 {lang_manager.get("personal_info")}
**{lang_manager.get("name")}:** {info.full_name}  
**{lang_manager.get("email")}:** {info.email}  
**{lang_manager.get("phone")}:** {info.phone}  
**{lang_manager.get("location")}:** {info.current_location}

### 💼 {lang_manager.get("professional_details")}
**{lang_manager
