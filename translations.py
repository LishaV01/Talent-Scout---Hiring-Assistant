"""
Language Manager for TalentScout Hiring Assistant
Handles translations for English, German, Hindi, Kannada, and French
"""

from typing import Dict, List, Optional
import json
import logging

logger = logging.getLogger(__name__)

class LanguageManager:
    """Manage translations and language-specific content"""
    
    def __init__(self):
        self.translations = self._load_translations()
        self.supported_languages = list(self.translations.keys())
        self.current_language = "en"
    
    def _load_translations(self) -> Dict[str, Dict[str, str]]:
        """Load all translations"""
        return {
            "en": {
                # Language name
                "language_name": "English",
                "language_flag": "🇬🇧",
                
                # UI Elements
                "app_title": "TalentScout Hiring Assistant",
                "app_subtitle": "Intelligent Hiring Assistant",
                "about": "ABOUT",
                "about_text": "An intelligent assistant that screens candidates through conversational AI, gathering information and conducting technical assessments.",
                "enable_voice": "Enable Voice",
                "reset_conversation": "RESET CONVERSATION",
                "show_debug_info": "Show Debug Info",
                "collected_data": "COLLECTED DATA",
                "profile_completion": "Profile Completion",
                "candidate_summary": "CANDIDATE SUMMARY",
                "personal_info": "Personal Information",
                "professional_details": "Professional Details",
                "technical_skills": "Technical Skills",
                "screening_completed": "Screening completed at",
                "select_language": "Select Language",
                "type_message": "Type your message here...",
                "thinking": "Thinking...",
                "voice_enabled": "Voice Enabled",
                "voice_manager": "Voice Manager",
                "initialized": "Initialized",
                "not_initialized": "Not Initialized",
                "not_available": "Not Available",
                "configuration_required": "Configuration Required",
                "api_key_warning": "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable in your .env file.",
                
                # Field Labels
                "name": "Name",
                "email": "Email",
                "phone": "Phone",
                "experience": "Experience",
                "years": "years",
                "position": "Position",
                "positions": "Positions",
                "location": "Location",
                "tech_stack": "Tech Stack",
                "not_collected": "Not collected",
                "desired_position": "Desired Position",
                "phase": "Phase",
                "session_id": "Session ID",
                "candidate_id": "Candidate ID",
                "not_saved_yet": "Not saved yet",
                
                # Conversation Templates
                "greeting": "Welcome aboard! I am Talent Scout. Thank you for taking the time to speak with me today. I appreciate your interest in the position.\n\nTo begin, could you please tell me your full name?",
                "next_name": "Thank you for your interest! Could you please tell me your full name?",
                "next_email": "Great! Now, could you please share your email address?",
                "next_phone": "Thank you! What's the best phone number to reach you?",
                "next_experience": "How many years of professional experience do you have?",
                "next_position": "What position are you interested in applying for?",
                "next_location": "Where are you currently located?",
                "next_tech_stack": "What technologies are you proficient in? Please list your tech stack.",
                "tech_questions_intro": "Hello {name},\n\nThank you for taking the time to discuss your background and experience with me. I appreciate your interest in the position and your enthusiasm for the opportunity.\n\nBased on our conversation, it seems like you have a strong foundation in {tech_stack}. To better evaluate your skills, I will now ask you a few technical questions related to your tech stack. Your responses will help us assess your qualifications for the role more accurately.\n\nI will be asking questions tailored to your expertise to gauge your technical proficiency. Please feel free to provide detailed responses, and don't hesitate to ask for clarification if needed.\n\nLet's begin with the technical questions.",
                "question_format": "Question {current} of {total}:",
                "thank_you_answer": "Thank you for your answer!",
                "farewell": "Thank you for your time today. We will update you shortly about the next steps in the hiring process.",
                "update_request": "Of course! I can help you update your information. What would you like to update? Please provide the new information.",
                "update_location": "Sure! Please provide your current location.",
                "update_email": "Of course! Please provide your updated email address.",
                "update_phone": "No problem! Please provide your updated phone number.",
                "update_confirmed": "Thank you! I've updated your information. Let's continue with the technical questions.",
                
                # Error Messages
                "error_processing": "I apologize, but I'm having trouble processing your response. Could you please try again?",
                
                # System Prompt
                "system_prompt": """You are a professional and friendly hiring assistant for TalentScout, a recruitment agency specializing in technology placements. Your role is to:
1. Gather essential candidate information
2. Ask about their technical expertise
3. Generate relevant technical questions based on their tech stack
4. Maintain a professional yet conversational tone
5. Stay focused on the hiring process without deviating from the purpose

Always be polite, encouraging, and professional. If the candidate provides unclear information, ask for clarification."""
            },
            
            "de": {
                # Language name
                "language_name": "Deutsch",
                "language_flag": "🇩🇪",
                
                # UI Elements
                "app_title": "TalentScout Einstellungsassistent",
                "app_subtitle": "Intelligenter Einstellungsassistent",
                "about": "ÜBER",
                "about_text": "Ein intelligenter Assistent, der Kandidaten durch konversationelle KI überprüft, Informationen sammelt und technische Bewertungen durchführt.",
                "enable_voice": "Sprache aktivieren",
                "reset_conversation": "GESPRÄCH ZURÜCKSETZEN",
                "show_debug_info": "Debug-Info anzeigen",
                "collected_data": "GESAMMELTE DATEN",
                "profile_completion": "Profilvervollständigung",
                "candidate_summary": "KANDIDATENZUSAMMENFASSUNG",
                "personal_info": "Persönliche Informationen",
                "professional_details": "Berufliche Details",
                "technical_skills": "Technische Fähigkeiten",
                "screening_completed": "Überprüfung abgeschlossen am",
                "select_language": "Sprache auswählen",
                "type_message": "Geben Sie Ihre Nachricht hier ein...",
                "thinking": "Denke nach...",
                "voice_enabled": "Sprache aktiviert",
                "voice_manager": "Sprachmanager",
                "initialized": "Initialisiert",
                "not_initialized": "Nicht initialisiert",
                "not_available": "Nicht verfügbar",
                "configuration_required": "Konfiguration erforderlich",
                "api_key_warning": "OpenAI API-Schlüssel nicht gefunden. Bitte setzen Sie die Umgebungsvariable OPENAI_API_KEY in Ihrer .env-Datei.",
                
                # Field Labels
                "name": "Name",
                "email": "E-Mail",
                "phone": "Telefon",
                "experience": "Erfahrung",
                "years": "Jahre",
                "position": "Position",
                "positions": "Positionen",
                "location": "Standort",
                "tech_stack": "Technologie-Stack",
                "not_collected": "Nicht erfasst",
                "desired_position": "Gewünschte Position",
                "phase": "Phase",
                "session_id": "Sitzungs-ID",
                "candidate_id": "Kandidaten-ID",
                "not_saved_yet": "Noch nicht gespeichert",
                
                # Conversation Templates
                "greeting": "Willkommen an Bord! Ich bin Talent Scout. Vielen Dank, dass Sie sich heute die Zeit genommen haben, mit mir zu sprechen. Ich schätze Ihr Interesse an der Position.\n\nZu Beginn, könnten Sie mir bitte Ihren vollständigen Namen nennen?",
                "next_name": "Vielen Dank für Ihr Interesse! Könnten Sie mir bitte Ihren vollständigen Namen nennen?",
                "next_email": "Großartig! Könnten Sie mir jetzt bitte Ihre E-Mail-Adresse mitteilen?",
                "next_phone": "Danke! Unter welcher Telefonnummer sind Sie am besten erreichbar?",
                "next_experience": "Wie viele Jahre Berufserfahrung haben Sie?",
                "next_position": "Für welche Position interessieren Sie sich?",
                "next_location": "Wo befinden Sie sich derzeit?",
                "next_tech_stack": "Mit welchen Technologien sind Sie vertraut? Bitte listen Sie Ihren Technologie-Stack auf.",
                "tech_questions_intro": "Hallo {name},\n\nVielen Dank, dass Sie sich die Zeit genommen haben, Ihren Hintergrund und Ihre Erfahrung mit mir zu besprechen. Ich schätze Ihr Interesse an der Position und Ihre Begeisterung für die Gelegenheit.\n\nBasierend auf unserem Gespräch scheint es, als hätten Sie eine solide Grundlage in {tech_stack}. Um Ihre Fähigkeiten besser bewerten zu können, werde ich Ihnen nun einige technische Fragen zu Ihrem Technologie-Stack stellen. Ihre Antworten helfen uns, Ihre Qualifikationen für die Rolle genauer zu bewerten.\n\nIch werde Fragen stellen, die auf Ihre Expertise zugeschnitten sind, um Ihre technische Kompetenz zu beurteilen. Bitte zögern Sie nicht, ausführliche Antworten zu geben, und fragen Sie nach Klärung, wenn nötig.\n\nLassen Sie uns mit den technischen Fragen beginnen.",
                "question_format": "Frage {current} von {total}:",
                "thank_you_answer": "Vielen Dank für Ihre Antwort!",
                "farewell": "Vielen Dank für Ihre Zeit heute. Wir werden Sie in Kürze über die nächsten Schritte im Einstellungsprozess informieren.",
                "update_request": "Natürlich! Ich kann Ihnen helfen, Ihre Informationen zu aktualisieren. Was möchten Sie aktualisieren? Bitte geben Sie die neuen Informationen an.",
                "update_location": "Sicher! Bitte geben Sie Ihren aktuellen Standort an.",
                "update_email": "Natürlich! Bitte geben Sie Ihre aktualisierte E-Mail-Adresse an.",
                "update_phone": "Kein Problem! Bitte geben Sie Ihre aktualisierte Telefonnummer an.",
                "update_confirmed": "Danke! Ich habe Ihre Informationen aktualisiert. Lassen Sie uns mit den technischen Fragen fortfahren.",
                
                # Error Messages
                "error_processing": "Es tut mir leid, aber ich habe Schwierigkeiten, Ihre Antwort zu verarbeiten. Könnten Sie es bitte noch einmal versuchen?",
                
                # System Prompt
                "system_prompt": """Sie sind ein professioneller und freundlicher Einstellungsassistent für TalentScout, eine auf Technologie-Vermittlungen spezialisierte Personalagentur. Ihre Aufgabe ist es:
1. Wesentliche Kandidateninformationen zu sammeln
2. Nach ihrer technischen Expertise zu fragen
3. Relevante technische Fragen basierend auf ihrem Technologie-Stack zu generieren
4. Einen professionellen, aber gesprächigen Ton beizubehalten
5. Sich auf den Einstellungsprozess zu konzentrieren, ohne vom Zweck abzuweichen

Seien Sie immer höflich, ermutigend und professionell. Wenn der Kandidat unklare Informationen liefert, bitten Sie um Klärung. Antworten Sie auf Deutsch."""
            },
            
            "hi": {
                # Language name
                "language_name": "हिन्दी",
                "language_flag": "🇮🇳",
                
                # UI Elements
                "app_title": "टैलेंटस्काउट भर्ती सहायक",
                "app_subtitle": "बुद्धिमान भर्ती सहायक",
                "about": "बारे में",
                "about_text": "एक बुद्धिमान सहायक जो वार्तालाप AI के माध्यम से उम्मीदवारों की जांच करता है, जानकारी एकत्र करता है और तकनीकी मूल्यांकन करता है।",
                "enable_voice": "आवाज़ सक्षम करें",
                "reset_conversation": "बातचीत रीसेट करें",
                "show_debug_info": "डिबग जानकारी दिखाएं",
                "collected_data": "एकत्रित डेटा",
                "profile_completion": "प्रोफ़ाइल पूर्णता",
                "candidate_summary": "उम्मीदवार सारांश",
                "personal_info": "व्यक्तिगत जानकारी",
                "professional_details": "व्यावसायिक विवरण",
                "technical_skills": "तकनीकी कौशल",
                "screening_completed": "स्क्रीनिंग पूर्ण हुई",
                "select_language": "भाषा चुनें",
                "type_message": "अपना संदेश यहाँ टाइप करें...",
                "thinking": "सोच रहा हूँ...",
                "voice_enabled": "आवाज़ सक्षम",
                "voice_manager": "आवाज़ प्रबंधक",
                "initialized": "प्रारंभ किया गया",
                "not_initialized": "प्रारंभ नहीं किया गया",
                "not_available": "उपलब्ध नहीं",
                "configuration_required": "कॉन्फ़िगरेशन आवश्यक",
                "api_key_warning": "OpenAI API कुंजी नहीं मिली। कृपया अपनी .env फ़ाइल में OPENAI_API_KEY पर्यावरण चर सेट करें।",
                
                # Field Labels
                "name": "नाम",
                "email": "ईमेल",
                "phone": "फ़ोन",
                "experience": "अनुभव",
                "years": "वर्ष",
                "position": "पद",
                "positions": "पद",
                "location": "स्थान",
                "tech_stack": "तकनीकी स्टैक",
                "not_collected": "एकत्र नहीं किया गया",
                "desired_position": "वांछित पद",
                "phase": "चरण",
                "session_id": "सत्र आईडी",
                "candidate_id": "उम्मीदवार आईडी",
                "not_saved_yet": "अभी तक सहेजा नहीं गया",
                
                # Conversation Templates
                "greeting": "स्वागत है! मैं टैलेंट स्काउट हूं। आज मुझसे बात करने के लिए समय निकालने के लिए धन्यवाद। मैं इस पद में आपकी रुचि की सराहना करता हूं।\n\nशुरू करने के लिए, क्या आप कृपया मुझे अपना पूरा नाम बता सकते हैं?",
                "next_name": "आपकी रुचि के लिए धन्यवाद! क्या आप कृपया मुझे अपना पूरा नाम बता सकते हैं?",
                "next_email": "बहुत अच्छा! अब, क्या आप कृपया अपना ईमेल पता साझा कर सकते हैं?",
                "next_phone": "धन्यवाद! आपसे संपर्क करने के लिए सबसे अच्छा फोन नंबर क्या है?",
                "next_experience": "आपके पास कितने वर्षों का व्यावसायिक अनुभव है?",
                "next_position": "आप किस पद के लिए आवेदन करने में रुचि रखते हैं?",
                "next_location": "आप वर्तमान में कहाँ स्थित हैं?",
                "next_tech_stack": "आप किन तकनीकों में निपुण हैं? कृपया अपना तकनीकी स्टैक सूचीबद्ध करें।",
                "tech_questions_intro": "नमस्ते {name},\n\nअपनी पृष्ठभूमि और अनुभव पर मुझसे चर्चा करने के लिए समय निकालने के लिए धन्यवाद। मैं इस पद में आपकी रुचि और अवसर के लिए आपके उत्साह की सराहना करता हूं।\n\nहमारी बातचीत के आधार पर, ऐसा लगता है कि आपके पास {tech_stack} में एक मजबूत आधार है। आपके कौशल का बेहतर मूल्यांकन करने के लिए, मैं अब आपसे आपके तकनीकी स्टैक से संबंधित कुछ तकनीकी प्रश्न पूछूंगा। आपकी प्रतिक्रियाएं हमें भूमिका के लिए आपकी योग्यताओं का अधिक सटीक मूल्यांकन करने में मदद करेंगी।\n\nमैं आपकी तकनीकी दक्षता का आकलन करने के लिए आपकी विशेषज्ञता के अनुरूप प्रश्न पूछूंगा। कृपया विस्तृत उत्तर देने में संकोच न करें, और यदि आवश्यक हो तो स्पष्टीकरण के लिए पूछने में संकोच न करें।\n\nआइए तकनीकी प्रश्नों से शुरू करते हैं।",
                "question_format": "प्रश्न {current} का {total}:",
                "thank_you_answer": "आपके उत्तर के लिए धन्यवाद!",
                "farewell": "आज आपके समय के लिए धन्यवाद। हम आपको भर्ती प्रक्रिया में अगले चरणों के बारे में शीघ्र ही अपडेट करेंगे।",
                "update_request": "बिल्कुल! मैं आपकी जानकारी अपडेट करने में आपकी मदद कर सकता हूं। आप क्या अपडेट करना चाहेंगे? कृपया नई जानकारी प्रदान करें।",
                "update_location": "ज़रूर! कृपया अपना वर्तमान स्थान प्रदान करें।",
                "update_email": "बिल्कुल! कृपया अपना अपडेट किया गया ईमेल पता प्रदान करें।",
                "update_phone": "कोई समस्या नहीं! कृपया अपना अपडेट किया गया फोन नंबर प्रदान करें।",
                "update_confirmed": "धन्यवाद! मैंने आपकी जानकारी अपडेट कर दी है। आइए तकनीकी प्रश्नों को जारी रखें।",
                
                # Error Messages
                "error_processing": "मुझे खेद है, लेकिन मुझे आपकी प्रतिक्रिया को प्रोसेस करने में परेशानी हो रही है। क्या आप कृपया फिर से कोशिश कर सकते हैं?",
                
                # System Prompt
                "system_prompt": """आप TalentScout के लिए एक पेशेवर और मैत्रीपूर्ण भर्ती सहायक हैं, जो प्रौद्योगिकी प्लेसमेंट में विशेषज्ञता रखने वाली एक भर्ती एजेंसी है। आपकी भूमिका है:
1. आवश्यक उम्मीदवार जानकारी एकत्र करना
2. उनकी तकनीकी विशेषज्ञता के बारे में पूछना
3. उनके तकनीकी स्टैक के आधार पर प्रासंगिक तकनीकी प्रश्न उत्पन्न करना
4. एक पेशेवर लेकिन संवादात्मक स्वर बनाए रखना
5. उद्देश्य से विचलित हुए बिना भर्ती प्रक्रिया पर केंद्रित रहना

हमेशा विनम्र, उत्साहजनक और पेशेवर रहें। यदि उम्मीदवार अस्पष्ट जानकारी प्रदान करता है, तो स्पष्टीकरण के लिए पूछें। हिंदी में उत्तर दें।"""
            },
            
            "kn": {
                # Language name
                "language_name": "ಕನ್ನಡ",
                "language_flag": "🇮🇳",
                
                # UI Elements
                "app_title": "ಟ್ಯಾಲೆಂಟ್‌ಸ್ಕೌಟ್ ನೇಮಕಾತಿ ಸಹಾಯಕ",
                "app_subtitle": "ಬುದ್ಧಿವಂತ ನೇಮಕಾತಿ ಸಹಾಯಕ",
                "about": "ಬಗ್ಗೆ",
                "about_text": "ಸಂಭಾಷಣಾ AI ಮೂಲಕ ಅಭ್ಯರ್ಥಿಗಳನ್ನು ಪರೀಕ್ಷಿಸುವ, ಮಾಹಿತಿಯನ್ನು ಸಂಗ್ರಹಿಸುವ ಮತ್ತು ತಾಂತ್ರಿಕ ಮೌಲ್ಯಮಾಪನಗಳನ್ನು ನಡೆಸುವ ಬುದ್ಧಿವಂತ ಸಹಾಯಕ.",
                "enable_voice": "ಧ್ವನಿ ಸಕ್ರಿಯಗೊಳಿಸಿ",
                "reset_conversation": "ಸಂಭಾಷಣೆ ಮರುಹೊಂದಿಸಿ",
                "show_debug_info": "ಡೀಬಗ್ ಮಾಹಿತಿ ತೋರಿಸಿ",
                "collected_data": "ಸಂಗ್ರಹಿಸಿದ ಡೇಟಾ",
                "profile_completion": "ಪ್ರೊಫೈಲ್ ಪೂರ್ಣಗೊಳಿಸುವಿಕೆ",
                "candidate_summary": "ಅಭ್ಯರ್ಥಿ ಸಾರಾಂಶ",
                "personal_info": "ವೈಯಕ್ತಿಕ ಮಾಹಿತಿ",
                "professional_details": "ವೃತ್ತಿಪರ ವಿವರಗಳು",
                "technical_skills": "ತಾಂತ್ರಿಕ ಕೌಶಲ್ಯಗಳು",
                "screening_completed": "ಸ್ಕ್ರೀನಿಂಗ್ ಪೂರ್ಣಗೊಂಡಿದೆ",
                "select_language": "ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ",
                "type_message": "ನಿಮ್ಮ ಸಂದೇಶವನ್ನು ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ...",
                "thinking": "ಯೋಚಿಸುತ್ತಿದ್ದೇನೆ...",
                "voice_enabled": "ಧ್ವನಿ ಸಕ್ರಿಯವಾಗಿದೆ",
                "voice_manager": "ಧ್ವನಿ ನಿರ್ವಾಹಕ",
                "initialized": "ಪ್ರಾರಂಭಿಸಲಾಗಿದೆ",
                "not_initialized": "ಪ್ರಾರಂಭಿಸಲಾಗಿಲ್ಲ",
                "not_available": "ಲಭ್ಯವಿಲ್ಲ",
                "configuration_required": "ಕಾನ್ಫಿಗರೇಶನ್ ಅಗತ್ಯವಿದೆ",
                "api_key_warning": "OpenAI API ಕೀ ಕಂಡುಬಂದಿಲ್ಲ. ದಯವಿಟ್ಟು ನಿಮ್ಮ .env ಫೈಲ್‌ನಲ್ಲಿ OPENAI_API_KEY ಪರಿಸರ ವೇರಿಯಬಲ್ ಅನ್ನು ಹೊಂದಿಸಿ.",
                
                # Field Labels
                "name": "ಹೆಸರು",
                "email": "ಇಮೇಲ್",
                "phone": "ಫೋನ್",
                "experience": "ಅನುಭವ",
                "years": "ವರ್ಷಗಳು",
                "position": "ಸ್ಥಾನ",
                "positions": "ಸ್ಥಾನಗಳು",
                "location": "ಸ್ಥಳ",
                "tech_stack": "ತಂತ್ರಜ್ಞಾನ ಸ್ಟ್ಯಾಕ್",
                "not_collected": "ಸಂಗ್ರಹಿಸಲಾಗಿಲ್ಲ",
                "desired_position": "ಅಪೇಕ್ಷಿತ ಸ್ಥಾನ",
                "phase": "ಹಂತ",
                "session_id": "ಸೆಷನ್ ಐಡಿ",
                "candidate_id": "ಅಭ್ಯರ್ಥಿ ಐಡಿ",
                "not_saved_yet": "ಇನ್ನೂ ಉಳಿಸಲಾಗಿಲ್ಲ",
                
                # Conversation Templates
                "greeting": "ಸ್ವಾಗತ! ನಾನು ಟ್ಯಾಲೆಂಟ್ ಸ್ಕೌಟ್. ಇಂದು ನನ್ನೊಂದಿಗೆ ಮಾತನಾಡಲು ಸಮಯ ತೆಗೆದುಕೊಂಡಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. ಈ ಸ್ಥಾನದಲ್ಲಿ ನಿಮ್ಮ ಆಸಕ್ತಿಯನ್ನು ನಾನು ಶ್ಲಾಘಿಸುತ್ತೇನೆ.\n\nಪ್ರಾರಂಭಿಸಲು, ದಯವಿಟ್ಟು ನಿಮ್ಮ ಪೂರ್ಣ ಹೆಸರನ್ನು ಹೇಳಬಹುದೇ?",
                "next_name": "ನಿಮ್ಮ ಆಸಕ್ತಿಗೆ ಧನ್ಯವಾದಗಳು! ದಯವಿಟ್ಟು ನಿಮ್ಮ ಪೂರ್ಣ ಹೆಸರನ್ನು ಹೇಳಬಹುದೇ?",
                "next_email": "ಅದ್ಭುತ! ಈಗ, ದಯವಿಟ್ಟು ನಿಮ್ಮ ಇಮೇಲ್ ವಿಳಾಸವನ್ನು ಹಂಚಿಕೊಳ್ಳಬಹುದೇ?",
                "next_phone": "ಧನ್ಯವಾದಗಳು! ನಿಮ್ಮನ್ನು ತಲುಪಲು ಉತ್ತಮ ಫೋನ್ ಸಂಖ್ಯೆ ಯಾವುದು?",
                "next_experience": "ನೀವು ಎಷ್ಟು ವರ್ಷಗಳ ವೃತ್ತಿಪರ ಅನುಭವವನ್ನು ಹೊಂದಿದ್ದೀರಿ?",
                "next_position": "ನೀವು ಯಾವ ಸ್ಥಾನಕ್ಕೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಲು ಆಸಕ್ತಿ ಹೊಂದಿದ್ದೀರಿ?",
                "next_location": "ನೀವು ಪ್ರಸ್ತುತ ಎಲ್ಲಿದ್ದೀರಿ?",
                "next_tech_stack": "ನೀವು ಯಾವ ತಂತ್ರಜ್ಞಾನಗಳಲ್ಲಿ ಪ್ರವೀಣರಾಗಿದ್ದೀರಿ? ದಯವಿಟ್ಟು ನಿಮ್ಮ ತಂತ್ರಜ್ಞಾನ ಸ್ಟ್ಯಾಕ್ ಅನ್ನು ಪಟ್ಟಿ ಮಾಡಿ.",
                "tech_questions_intro": "ನಮಸ್ತೆ {name},\n\nನಿಮ್ಮ ಹಿನ್ನೆಲೆ ಮತ್ತು ಅನುಭವವನ್ನು ನನ್ನೊಂದಿಗೆ ಚರ್ಚಿಸಲು ಸಮಯ ತೆಗೆದುಕೊಂಡಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. ಈ ಸ್ಥಾನದಲ್ಲಿ ನಿಮ್ಮ ಆಸಕ್ತಿ ಮತ್ತು ಅವಕಾಶಕ್ಕಾಗಿ ನಿಮ್ಮ ಉತ್ಸಾಹವನ್ನು ನಾನು ಶ್ಲಾಘಿಸುತ್ತೇನೆ.\n\nನಮ್ಮ ಸಂಭಾಷಣೆಯ ಆಧಾರದ ಮೇಲೆ, ನೀವು {tech_stack} ನಲ್ಲಿ ಬಲವಾದ ಅಡಿಪಾಯವನ್ನು ಹೊಂದಿರುವಂತೆ ತೋರುತ್ತದೆ. ನಿಮ್ಮ ಕೌಶಲ್ಯಗಳನ್ನು ಉತ್ತಮವಾಗಿ ಮೌಲ್ಯಮಾಪನ ಮಾಡಲು, ನಾನು ಈಗ ನಿಮ್ಮ ತಂತ್ರಜ್ಞಾನ ಸ್ಟ್ಯಾಕ್‌ಗೆ ಸಂಬಂಧಿಸಿದ ಕೆಲವು ತಾಂತ್ರಿಕ ಪ್ರಶ್ನೆಗಳನ್ನು ಕೇಳುತ್ತೇನೆ. ನಿಮ್ಮ ಪ್ರತಿಕ್ರಿಯೆಗಳು ಪಾತ್ರಕ್ಕಾಗಿ ನಿಮ್ಮ ಅರ್ಹತೆಗಳನ್ನು ಹೆಚ್ಚು ನಿಖರವಾಗಿ ಮೌಲ್ಯಮಾಪನ ಮಾಡಲು ನಮಗೆ ಸಹಾಯ ಮಾಡುತ್ತದೆ.\n\nನಿಮ್ಮ ತಾಂತ್ರಿಕ ಪ್ರಾವೀಣ್ಯತೆಯನ್ನು ಅಳೆಯಲು ನಿಮ್ಮ ಪರಿಣತಿಗೆ ಅನುಗುಣವಾಗಿ ಪ್ರಶ್ನೆಗಳನ್ನು ಕೇಳುತ್ತೇನೆ. ದಯವಿಟ್ಟು ವಿವರವಾದ ಪ್ರತಿಕ್ರಿಯೆಗಳನ್ನು ನೀಡಲು ಹಿಂಜರಿಯಬೇಡಿ, ಮತ್ತು ಅಗತ್ಯವಿದ್ದರೆ ಸ್ಪಷ್ಟೀಕರಣಕ್ಕಾಗಿ ಕೇಳಲು ಹಿಂಜರಿಯಬೇಡಿ.\n\nತಾಂತ್ರಿಕ ಪ್ರಶ್ನೆಗಳೊಂದಿಗೆ ಪ್ರಾರಂಭಿಸೋಣ.",
                "question_format": "ಪ್ರಶ್ನೆ {current} ರಲ್ಲಿ {total}:",
                "thank_you_answer": "ನಿಮ್ಮ ಉತ್ತರಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು!",
                "farewell": "ಇಂದು ನಿಮ್ಮ ಸಮಯಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. ನೇಮಕಾತಿ ಪ್ರಕ್ರಿಯೆಯಲ್ಲಿ ಮುಂದಿನ ಹಂತಗಳ ಬಗ್ಗೆ ನಾವು ಶೀಘ್ರದಲ್ಲೇ ನಿಮಗೆ ಅಪ್‌ಡೇಟ್ ಮಾಡುತ್ತೇವೆ.",
                "update_request": "ಖಂಡಿತವಾಗಿ! ನಿಮ್ಮ ಮಾಹಿತಿಯನ್ನು ಅಪ್‌ಡೇಟ್ ಮಾಡಲು ನಾನು ನಿಮಗೆ ಸಹಾಯ ಮಾಡಬಹುದು. ನೀವು ಏನನ್ನು ಅಪ್‌ಡೇಟ್ ಮಾಡಲು ಬಯಸುತ್ತೀರಿ? ದಯವಿಟ್ಟು ಹೊಸ ಮಾಹಿತಿಯನ್ನು ಒದಗಿಸಿ.",
                "update_location": "ಖಚಿತವಾಗಿ! ದಯವಿಟ್ಟು ನಿಮ್ಮ ಪ್ರಸ್ತುತ ಸ್ಥಳವನ್ನು ಒದಗಿಸಿ.",
                "update_email": "ಖಂಡಿತವಾಗಿ! ದಯವಿಟ್ಟು ನಿಮ್ಮ ಅಪ್‌ಡೇಟ್ ಮಾಡಿದ ಇಮೇಲ್ ವಿಳಾಸವನ್ನು ಒದಗಿಸಿ.",
                "update_phone": "ಯಾವುದೇ ಸಮಸ್ಯೆ ಇಲ್ಲ! ದಯವಿಟ್ಟು ನಿಮ್ಮ ಅಪ್‌ಡೇಟ್ ಮಾಡಿದ ಫೋನ್ ಸಂಖ್ಯೆಯನ್ನು ಒದಗಿಸಿ.",
                "update_confirmed": "ಧನ್ಯವಾದಗಳು! ನಾನು ನಿಮ್ಮ ಮಾಹಿತಿಯನ್ನು ಅಪ್‌ಡೇಟ್ ಮಾಡಿದ್ದೇನೆ. ತಾಂತ್ರಿಕ ಪ್ರಶ್ನೆಗಳೊಂದಿಗೆ ಮುಂದುವರಿಯೋಣ.",
                
                # Error Messages
                "error_processing": "ಕ್ಷಮಿಸಿ, ಆದರೆ ನಿಮ್ಮ ಪ್ರತಿಕ್ರಿಯೆಯನ್ನು ಪ್ರಕ್ರಿಯೆಗೊಳಿಸಲು ನನಗೆ ತೊಂದರೆ ಆಗುತ್ತಿದೆ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಬಹುದೇ?",
                
                # System Prompt
                "system_prompt": """ನೀವು TalentScout ಗಾಗಿ ವೃತ್ತಿಪರ ಮತ್ತು ಸ್ನೇಹಪರ ನೇಮಕಾತಿ ಸಹಾಯಕರಾಗಿದ್ದೀರಿ, ತಂತ್ರಜ್ಞಾನ ನಿಯೋಜನೆಗಳಲ್ಲಿ ಪರಿಣತಿ ಹೊಂದಿರುವ ನೇಮಕಾತಿ ಏಜೆನ್ಸಿ. ನಿಮ್ಮ ಪಾತ್ರ:
1. ಅಗತ್ಯವಾದ ಅಭ್ಯರ್ಥಿ ಮಾಹಿತಿಯನ್ನು ಸಂಗ್ರಹಿಸುವುದು
2. ಅವರ ತಾಂತ್ರಿಕ ಪರಿಣತಿಯ ಬಗ್ಗೆ ಕೇಳುವುದು
3. ಅವರ ತಂತ್ರಜ್ಞಾನ ಸ್ಟ್ಯಾಕ್ ಆಧಾರದ ಮೇಲೆ ಸಂಬಂಧಿತ ತಾಂತ್ರಿಕ ಪ್ರಶ್ನೆಗಳನ್ನು ರಚಿಸುವುದು
4. ವೃತ್ತಿಪರ ಆದರೆ ಸಂಭಾಷಣಾ ಸ್ವರವನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳುವುದು
5. ಉದ್ದೇಶದಿಂದ ವಿಚಲಿತವಾಗದೆ ನೇಮಕಾತಿ ಪ್ರಕ್ರಿಯೆಯ ಮೇಲೆ ಕೇಂದ್ರೀಕರಿಸುವುದು

ಯಾವಾಗಲೂ ಸಭ್ಯ, ಉತ್ತೇಜಕ ಮತ್ತು ವೃತ್ತಿಪರರಾಗಿರಿ. ಅಭ್ಯರ್ಥಿಯು ಅಸ್ಪಷ್ಟ ಮಾಹಿತಿಯನ್ನು ಒದಗಿಸಿದರೆ, ಸ್ಪಷ್ಟೀಕರಣಕ್ಕಾಗಿ ಕೇಳಿ. ಕನ್ನಡದಲ್ಲಿ ಉತ್ತರಿಸಿ."""
            },
            
            "fr": {
                # Language name
                "language_name": "Français",
                "language_flag": "🇫🇷",
                
                # UI Elements
                "app_title": "Assistant de Recrutement TalentScout",
                "app_subtitle": "Assistant de Recrutement Intelligent",
                "about": "À PROPOS",
                "about_text": "Un assistant intelligent qui évalue les candidats grâce à l'IA conversationnelle, collecte des informations et effectue des évaluations techniques.",
                "enable_voice": "Activer la Voix",
                "reset_conversation": "RÉINITIALISER LA CONVERSATION",
                "show_debug_info": "Afficher les Infos de Débogage",
                "collected_data": "DONNÉES COLLECTÉES",
                "profile_completion": "Complétude du Profil",
                "candidate_summary": "RÉSUMÉ DU CANDIDAT",
                "personal_info": "Informations Personnelles",
                "professional_details": "Détails Professionnels",
                "technical_skills": "Compétences Techniques",
                "screening_completed": "Évaluation terminée le",
                "select_language": "Sélectionner la Langue",
                "type_message": "Tapez votre message ici...",
                "thinking": "Réflexion en cours...",
                "voice_enabled": "Voix Activée",
                "voice_manager": "Gestionnaire de Voix",
                "initialized": "Initialisé",
                "not_initialized": "Non Initialisé",
                "not_available": "Non Disponible",
                "configuration_required": "Configuration Requise",
                "api_key_warning": "Clé API OpenAI non trouvée. Veuillez définir la variable d'environnement OPENAI_API_KEY dans votre fichier .env.",
                
                # Field Labels
                "name": "Nom",
                "email": "Email",
                "phone": "Téléphone",
                "experience": "Expérience",
                "years": "ans",
                "position": "Poste",
                "positions": "Postes",
                "location": "Localisation",
                "tech_stack": "Stack Technique",
                "not_collected": "Non collecté",
                "desired_position": "Poste Souhaité",
                "phase": "Phase",
                "session_id": "ID de Session",
                "candidate_id": "ID du Candidat",
                "not_saved_yet": "Pas encore enregistré",
                
                # Conversation Templates
                "greeting": "Bienvenue à bord ! Je suis Talent Scout. Merci d'avoir pris le temps de me parler aujourd'hui. J'apprécie votre intérêt pour le poste.\n\nPour commencer, pourriez-vous me dire votre nom complet ?",
                "next_name": "Merci pour votre intérêt ! Pourriez-vous me dire votre nom complet ?",
                "next_email": "Parfait ! Maintenant, pourriez-vous partager votre adresse email ?",
                "next_phone": "Merci ! Quel est le meilleur numéro de téléphone pour vous joindre ?",
                "next_experience": "Combien d'années d'expérience professionnelle avez-vous ?",
                "next_position": "Pour quel poste souhaitez-vous postuler ?",
                "next_location": "Où êtes-vous actuellement situé ?",
                "next_tech_stack": "Dans quelles technologies êtes-vous compétent ? Veuillez lister votre stack technique.",
                "tech_questions_intro": "Bonjour {name},\n\nMerci d'avoir pris le temps de discuter de votre parcours et de votre expérience avec moi. J'apprécie votre intérêt pour le poste et votre enthousiasme pour cette opportunité.\n\nD'après notre conversation, il semble que vous ayez une base solide en {tech_stack}. Pour mieux évaluer vos compétences, je vais maintenant vous poser quelques questions techniques liées à votre stack technique. Vos réponses nous aideront à évaluer plus précisément vos qualifications pour le rôle.\n\nJe vais poser des questions adaptées à votre expertise pour évaluer votre compétence technique. N'hésitez pas à fournir des réponses détaillées, et n'hésitez pas à demander des éclaircissements si nécessaire.\n\nCommençons par les questions techniques.",
                "question_format": "Question {current} sur {total} :",
                "thank_you_answer": "Merci pour votre réponse !",
                "farewell": "Merci pour votre temps aujourd'hui. Nous vous informerons prochainement des prochaines étapes du processus de recrutement.",
                "update_request": "Bien sûr ! Je peux vous aider à mettre à jour vos informations. Que souhaitez-vous mettre à jour ? Veuillez fournir les nouvelles informations.",
                "update_location": "Bien sûr ! Veuillez indiquer votre localisation actuelle.",
                "update_email": "Bien sûr ! Veuillez fournir votre adresse email mise à jour.",
                "update_phone": "Pas de problème ! Veuillez fournir votre numéro de téléphone mis à jour.",
                "update_confirmed": "Merci ! J'ai mis à jour vos informations. Continuons avec les questions techniques.",
                
                # Error Messages
                "error_processing": "Je suis désolé, mais j'ai du mal à traiter votre réponse. Pourriez-vous réessayer ?",
                
                # System Prompt
                "system_prompt": """Vous êtes un assistant de recrutement professionnel et amical pour TalentScout, une agence de recrutement spécialisée dans les placements technologiques. Votre rôle est de :
1. Recueillir les informations essentielles du candidat
2. Interroger sur leur expertise technique
3. Générer des questions techniques pertinentes basées sur leur stack technique
4. Maintenir un ton professionnel mais conversationnel
5. Rester concentré sur le processus de recrutement sans dévier de l'objectif

Soyez toujours poli, encourageant et professionnel. Si le candidat fournit des informations peu claires, demandez des éclaircissements. Répondez en français."""
            }
        }
    
    def set_language(self, language_code: str) -> bool:
        """Set the current language"""
        if language_code in self.supported_languages:
            self.current_language = language_code
            logger.info(f"Language set to: {language_code}")
            return True
        logger.error(f"Unsupported language code: {language_code}")
        return False
    
    def get(self, key: str, default: str = "") -> str:
        """Get translation for a key in current language"""
        return self.translations.get(self.current_language, {}).get(key, default)
    
    def get_language_name(self, language_code: str = None) -> str:
        """Get the display name of a language"""
        lang = language_code or self.current_language
        return self.translations.get(lang, {}).get("language_name", lang.upper())
    
    def get_language_flag(self, language_code: str = None) -> str:
        """Get the flag emoji for a language"""
        lang = language_code or self.current_language
        return self.translations.get(lang, {}).get("language_flag", "🌐")
    
    def get_supported_languages(self) -> List[Dict[str, str]]:
        """Get list of supported languages with details"""
        return [
            {
                "code": code,
                "name": self.get_language_name(code),
                "flag": self.get_language_flag(code)
            }
            for code in self.supported_languages
        ]
    
    def format_greeting(self) -> str:
        """Get formatted greeting message"""
        return self.get("greeting")
    
    def format_next_question(self, field: str) -> str:
        """Get the next question based on missing field"""
        question_map = {
            "full name": "next_name",
            "email address": "next_email",
            "phone number": "next_phone",
            "years of experience": "next_experience",
            "desired position(s)": "next_position",
            "current location": "next_location",
            "tech stack": "next_tech_stack"
        }
        
        key = question_map.get(field, "next_name")
        return self.get(key)
    
    def format_tech_intro(self, name: str, tech_stack: List[str]) -> str:
        """Format technical questions introduction"""
        template = self.get("tech_questions_intro")
        tech_stack_str = ", ".join(tech_stack) if tech_stack else "your technologies"
        return template.format(name=name, tech_stack=tech_stack_str)
    
    def format_question(self, current: int, total: int) -> str:
        """Format question number"""
        template = self.get("question_format")
        return template.format(current=current, total=total)
    
    def get_field_label(self, field: str) -> str:
        """Get localized field label"""
        field_map = {
            "name": "name",
            "email": "email",
            "phone": "phone",
            "experience": "experience",
            "position": "position",
            "location": "location",
            "tech_stack": "tech_stack"
        }
        return self.get(field_map.get(field, field))
    
    def get_extraction_prompt(self, language_code: str = None) -> str:
        """Get extraction prompt for specific language"""
        lang = language_code or self.current_language
        
        # Language-specific extraction instructions
        extraction_instructions = {
            "en": "Extract the following information from the user's message if present",
            "de": "Extrahieren Sie die folgenden Informationen aus der Nachricht des Benutzers, falls vorhanden",
            "hi": "यदि उपस्थित हो तो उपयोगकर्ता के संदेश से निम्नलिखित जानकारी निकालें",
            "kn": "ಬಳಕೆದಾರರ ಸಂದೇಶದಿಂದ ಈ ಕೆಳಗಿನ ಮಾಹಿತಿಯನ್ನು ಹೊರತೆಗೆಯಿರಿ",
            "fr": "Extrayez les informations suivantes du message de l'utilisateur si présentes"
        }
        
        return extraction_instructions.get(lang, extraction_instructions["en"])

# Singleton instance
_language_manager = None

def get_language_manager() -> LanguageManager:
    """Get or create language manager instance"""
    global _language_manager
    if _language_manager is None:
        _language_manager = LanguageManager()
    return _language_manager