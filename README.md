"TalentScout Hiring Assistant " 🤖
An intelligent AI-powered conversational screening tool that revolutionizes the initial candidate interview process through natural language processing and automated assessments.


🌟 Project Overview
TalentScout Hiring Assistant is a sophisticated AI-driven recruitment tool that automates the initial candidate screening process. Built with Streamlit and powered by OpenAI's GPT-3.5, it conducts natural conversations with candidates, extracting relevant information and assessing technical skills through dynamically generated questions.

Why TalentScout?
Traditional screening processes are time-consuming and often inconsistent. TalentScout addresses these challenges by:

Automating Initial Screenings: Save 80% of recruiter time on initial candidate assessments
Ensuring Consistency: Every candidate gets the same professional experience
24/7 Availability: Candidates can complete screenings at their convenience
Data-Driven Insights: All conversations are recorded and analyzable

✨ Features
Core Capabilities
- Natural Language Processing
Conversational AI that understands context and intent
Multi-turn dialogue management
Intelligent information extraction from unstructured text
-  Smart Data Collection
Automatic parsing of contact information
Experience and skill extraction
Location and position preference detection
- Dynamic Assessment
Technical questions tailored to candidate's tech stack
Experience-appropriate difficulty levels
Real-time question generation
- Comprehensive Data Management
SQLite database for all candidate information
Full conversation logging
Export capabilities (JSON/CSV)

Additional Features
🔊 Voice Integration: Optional text-to-speech for accessibility
📈 Admin Dashboard: Complete candidate management interface
🎨 Modern UI/UX: Animated, responsive design with glassmorphism effects
🔄 Real-time Updates: Candidates can correct information during conversation
📱 Mobile Responsive: Works seamlessly on all devices

🎥 Demo
Candidate Experience
🤖: Welcome aboard! I am Talent Scout. Thank you for taking the time to speak with me today.
    To begin, could you please tell me your full name?

👤: Hi, I'm Sarah Johnson

🤖: Nice to meet you, Sarah! Could you please share your email address?

👤: Sure, it's sarah.johnson@techcorp.com

🤖: Thank you! What's the best phone number to reach you?

[... conversation continues ...]
Admin Dashboard Preview
📊 TalentScout Admin Dashboard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Summary Metrics:
├── Total Candidates: 156
├── Avg. Experience: 4.5 years
├── Completed Profiles: 142
└── Today's Candidates: 12

Recent Candidates:
┌─────────────────┬──────────────┬────────────┬───────────┐
│ Name            │ Email        │ Experience │ Location  │
├─────────────────┼──────────────┼────────────┼───────────┤
│ Sarah Johnson   │ sarah@...    │ 5 years    │ New York  │
│ Mike Chen       │ mike@...     │ 3 years    │ San Jose  │
└─────────────────┴──────────────┴────────────┴───────────┘

# Setting up Development Environment
# Create a Virtual Environment:
python -m venv venv


### Activate the environment:
Windows: .\venv\Scripts\activate
Linux/Mac: source venv/bin/activate

### Install required dependencies:
pip install -r requirements.txt

# pyttsx3 (Text-to-Speech)
pip install pyttsx3
pip install SpeechRecognition

# All voice-related dependencies
pip install pyttsx3 SpeechRecognition pyaudio

### Configure environment:
cp .env.example .env

### Start the main application:
streamlit run app.py --server.port 8501

### Run the admin dashboard:
streamlit run admin.py --server.port 8502

# Export to JSON
db.export_to_json("export.json")





🛠️ Technical Details
Architecture Overview
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Frontend                       │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │   Chat UI   │  │ Progress Bar │  │  Voice Toggle   │   │
│  └──────┬──────┘  └──────────────┘  └─────────────────┘   │
└─────────┼───────────────────────────────────────────────────┘
          │
┌─────────▼───────────────────────────────────────────────────┐
│                    Application Layer                         │
│  ┌─────────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Conversation    │  │ Information  │  │   Question   │  │
│  │   Handler       │  │  Extractor   │  │  Generator   │  │
│  └────────┬────────┘  └──────┬───────┘  └──────┬───────┘  │
└───────────┼──────────────────┼──────────────────┼──────────┘
            │                  │                  │
┌───────────▼──────────────────▼──────────────────▼──────────┐
│                      LLM Integration                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              OpenAI GPT-3.5 API                      │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
            │
┌───────────▼─────────────────────────────────────────────────┐
│                    Data Persistence                          │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐    │
│  │   SQLite     │  │ Session Mgmt │  │ Export Engine  │    │
│  │   Database   │  │              │  │                │    │
│  └──────────────┘  └──────────────┘  └────────────────┘    │
└─────────────────────────────────────────────────────────────┘


# Core Architecture 
Core Architecture 
The application follows a modular architecture with clear separation of concerns:

Main Application (app.py): Streamlit-based conversational interface
Database Layer (database.py): SQLite persistence with comprehensive data models
Admin Interface (admin.py): Dashboard for viewing and exporting candidate data
UI Components (live_UI.py): Custom theming with glassmorphism effects
Internationalization (translations.py): Multi-language support (EN, DE, HI, KN, FR)
Voice Service (voice_service.py): Optional TTS/STT capabilities


📁 Project Structure
Hiring Claude/
│
├── app.py                 # Main application entry point
├── admin.py              # Admin dashboard
├── database.py           # Database operations
├── live_UI.py            # UI components and styling
├── voice_service.py      # Text-to-speech integration
├── setup.py              # Automated setup script
├── requirements.txt      # Python dependencies
├── config.yaml           # Advanced configuration
├── .env.example          # Environment template
├── .gitignore            # Git ignore rules
│── .translations.py      #MultiLanguage Integration
├── .talentscout.db       # database
│             
└── readme/              # readme file
⚙️ Configuration
Environment Variables (.env)
bash

# Required
OPENAI_API_KEY="your-api-key-here"

MODEL_NAME=gpt-3.5-turbo
llm:
  provider: "openai"
  model: "gpt-3.5-turbo"
  temperature:
    default: 0.7
    extraction: 0.3
    questions: 0.5



# Libraries & Technologies
Core Dependencies:

Streamlit: Web framework for the interactive UI
OpenAI API: GPT-3.5-turbo for conversational AI and information extraction
SQLite3: Lightweight database for persistent storage
pyttsx3: Text-to-speech synthesis
speech_recognition: Speech-to-text capabilities
pandas: Data manipulation for admin dashboard

Key Design Patterns:

Singleton Pattern: Language manager instance
State Management: Streamlit session state for conversation flow
Queue-based Threading: Voice service with worker threads
Dataclass Models: Type-safe candidate information structure

# Model Configuration
pythonMODEL_NAME: str = "gpt-3.5-turbo"
MAX_TOKENS: int = 500
TEMPERATURE: float = 0.7

# Prompt Design
The application uses sophisticated prompt engineering for two main tasks:
1. Information Extraction Prompt
pythondef get_info_extraction(self, lang_manager, message: str):
    return f"""{extraction_instruction}:
    - Full name (can be single name like "Helen", "John", or full names like "John Doe")
    - Email address
    - Phone number
    - Years of experience
    - Desired positions (including job titles like developer, tester, engineer...)
    - Current location (city, state, or country names)
    - Tech stack

    Important notes:
    - If the message is a simple name (1-3 words with only letters), extract it as full_name
    - Single names like "Helen", "Sarah", "John" should be recognized as full_name
    - If the user mentions any job role or position, extract it as desired_positions
    - Simple responses like "tester" or "software tester" should be recognized as desired positions
    - If the message is a single word or simple location name, extract it as current_location
    - Do NOT extract names as positions
    - Names should NOT be interpreted as job positions

    User message: "{message}"
    
    Return the extracted information in JSON format. If information is not present, use null.
    """
Key Design Decisions:

Clear disambiguation between names and job positions
Examples provided for edge cases
JSON output format for reliable parsing
Fallback regex patterns for common data (email, phone)

2. Technical Question Generation
pythondef get_technical_questions(self, lang_manager, tech_stack: List[str], years_experience: int):
    return f"""Generate 3-5 technical questions for a candidate with the following tech stack:
    {tech_stack_str}

    The candidate has {years_experience} years of experience.

    Generate questions that:
    1. Are appropriate for their experience level
    2. Cover different aspects of their declared technologies
    3. Are specific and practical
    4. Can assess real-world knowledge

    Format: Return as a JSON array of questions."""
Prompt Strategy:

Experience-aware question difficulty
Technology-specific focus
Practical, real-world scenarios
Structured JSON output

# Challenges & Solutions
1. Natural Language Understanding
Challenge: Distinguishing between names and job positions (e.g., "Tester" could be either)
Solution:

Multi-layered extraction approach:

Regex patterns for structured data (email, phone)
Context-aware LLM extraction
Position keyword detection
Simple name pattern matching



python# Check if it's a name pattern
name_pattern = r"^[A-Za-z\s\-']+$"
if re.match(name_pattern, message.strip()):
    position_keywords = ['tester', 'developer', 'engineer', ...]
    if potential_name.lower() not in position_keywords:
        current_info.full_name = potential_name

2. Voice Integration Stability
Challenge: TTS engine blocking main thread and causing UI freezes
Solution:

Queue-based worker thread for TTS
Timeout protection for cleanup
Graceful degradation when voice unavailable

pythondef cleanup_with_timeout():
    try:
        self.voice_service.cleanup()
    except:
        pass

cleanup_thread = threading.Thread(target=cleanup_with_timeout)
cleanup_thread.daemon = True
cleanup_thread.start()
cleanup_thread.join(timeout=2.0)  # 2 second timeout

3. Language Switching Mid-Conversation
Challenge: Maintaining conversation context when switching languages
Solution:

Warning dialog before language switch
Option to continue or start fresh
Selectbox counter to prevent widget glitching

pythonif new_language != st.session_state.selected_language:
    if st.session_state.conversation_started:
        st.warning("⚠️ Changing language will update the interface.")
        # Offer options to continue or start fresh


5. UI Responsiveness
Challenge: Complex glassmorphism effects potentially affecting performance
Solution:

CSS-only animations
Minimal JavaScript
Fallback themes for compatibility

python# Animated gradient background with Pinterest colors
background: linear-gradient(-45deg, #ffffff, #fff0f3, #ffe0e6, #ffd1d9, #ffffff);
background-size: 400% 400%;
animation: gradientShift 15s ease infinite;

