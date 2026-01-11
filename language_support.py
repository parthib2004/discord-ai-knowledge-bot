from langdetect import detect, DetectorFactory
import google.genai as genai

# Set seed for consistent results
DetectorFactory.seed = 0

# Language mappings
LANGUAGE_NAMES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh': 'Chinese',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'tr': 'Turkish',
    'nl': 'Dutch',
    'sv': 'Swedish',
    'da': 'Danish',
    'no': 'Norwegian',
    'fi': 'Finnish',
    'pl': 'Polish',
    'cs': 'Czech',
    'hu': 'Hungarian',
    'ro': 'Romanian',
    'bg': 'Bulgarian',
    'hr': 'Croatian',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'et': 'Estonian',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'uk': 'Ukrainian',
    'be': 'Belarusian',
    'mk': 'Macedonian',
    'sq': 'Albanian',
    'sr': 'Serbian',
    'bs': 'Bosnian',
    'mt': 'Maltese',
    'cy': 'Welsh',
    'ga': 'Irish',
    'is': 'Icelandic',
    'th': 'Thai',
    'vi': 'Vietnamese',
    'id': 'Indonesian',
    'ms': 'Malay',
    'tl': 'Filipino',
    'sw': 'Swahili',
    'af': 'Afrikaans',
    'ca': 'Catalan',
    'eu': 'Basque',
    'gl': 'Galician',
    'he': 'Hebrew',
    'fa': 'Persian',
    'ur': 'Urdu',
    'bn': 'Bengali',
    'ta': 'Tamil',
    'te': 'Telugu',
    'ml': 'Malayalam',
    'kn': 'Kannada',
    'gu': 'Gujarati',
    'pa': 'Punjabi',
    'ne': 'Nepali',
    'si': 'Sinhala',
    'my': 'Myanmar',
    'km': 'Khmer',
    'lo': 'Lao',
    'ka': 'Georgian',
    'am': 'Amharic',
    'so': 'Somali',
    'zu': 'Zulu',
    'xh': 'Xhosa',
    'yo': 'Yoruba',
    'ig': 'Igbo',
    'ha': 'Hausa'
}

def detect_language(text):
    """Detect the language of the input text with improved English detection"""
    try:
        # Common English greetings and phrases that should always be treated as English
        english_greetings = [
            'hi', 'hello', 'hey', 'help', 'thanks', 'thank you', 'yes', 'no', 
            'ok', 'okay', 'sure', 'please', 'sorry', 'excuse me', 'good morning',
            'good afternoon', 'good evening', 'good night', 'goodbye', 'bye',
            'how are you', 'nice to meet you', 'see you later'
        ]
        
        text_lower = text.lower().strip()
        
        # Check if the text is a common English greeting/phrase
        if text_lower in english_greetings:
            return 'en', 'English'
        
        # Check if text starts with common English greetings
        for greeting in english_greetings:
            if text_lower.startswith(greeting):
                return 'en', 'English'
        
        from langdetect import detect_langs
        
        # Get confidence scores for all detected languages
        lang_probs = detect_langs(text)
        
        # Get the most likely language
        detected_lang = lang_probs[0].lang
        confidence = lang_probs[0].prob
        
        # If confidence is low (< 0.7) or text is very short, default to English
        if confidence < 0.7 or len(text.split()) < 3:
            # Check if English is in the top 2 detected languages
            for lang_prob in lang_probs[:2]:
                if lang_prob.lang == 'en':
                    return 'en', 'English'
            
            # If no English detected but confidence is low, still default to English
            if confidence < 0.5:
                return 'en', 'English'
        
        # Additional check: if detected as Finnish but contains common English words
        if detected_lang == 'fi':
            english_indicators = ['the', 'and', 'or', 'is', 'are', 'was', 'were', 'have', 'has', 'had', 'will', 'would', 'can', 'could', 'should', 'what', 'how', 'when', 'where', 'why', 'who']
            english_word_count = sum(1 for word in english_indicators if word in text_lower)
            
            if english_word_count >= 2:  # If 2+ common English words found
                return 'en', 'English'
        
        return detected_lang, LANGUAGE_NAMES.get(detected_lang, detected_lang)
        
    except Exception as e:
        print(f"Language detection error: {e}")
        return 'en', 'English'  # Default to English if detection fails

def create_multilingual_prompt(question, knowledge, detected_lang, lang_name):
    """Create a prompt that instructs the AI to respond in the detected language"""
    
    if detected_lang == 'en':
        # English prompt - now answers any question
        return f"""You are CreoBot, a helpful AI assistant for CreoWis Technologies. You can answer any question the user asks.

Company Knowledge (use when relevant):
{knowledge}

User Question: {question}

Instructions:
- Answer any question the user asks to the best of your ability
- If the question is about CreoWis Technologies, use the company knowledge provided
- For general questions, use your knowledge to provide helpful answers
- Be professional, friendly, and helpful
- Keep responses concise but informative
- If you don't know something, say so honestly"""
    
    else:
        # Multi-language prompt - now answers any question
        return f"""You are CreoBot, a helpful AI assistant for CreoWis Technologies. You can answer any question the user asks.

Company Knowledge (use when relevant):
{knowledge}

User Question: {question}

IMPORTANT INSTRUCTIONS:
- The user asked their question in {lang_name} ({detected_lang})
- You MUST respond in {lang_name} ({detected_lang}) - the same language as the user's question
- Answer any question the user asks to the best of your ability
- If the question is about CreoWis Technologies, use the company knowledge provided
- For general questions, use your knowledge to provide helpful answers in {lang_name}
- Be professional, friendly, and helpful
- Keep responses concise but informative
- Maintain the same language throughout your entire response
- If you don't know something, say so honestly in {lang_name}

Example response format in {lang_name}:
[Your answer should be entirely in {lang_name}]"""

def get_language_flag(lang_code):
    """Get flag emoji for language"""
    flag_map = {
        'en': '🇺🇸', 'es': '🇪🇸', 'fr': '🇫🇷', 'de': '🇩🇪', 'it': '🇮🇹',
        'pt': '🇵🇹', 'ru': '🇷🇺', 'ja': '🇯🇵', 'ko': '🇰🇷', 'zh': '🇨🇳',
        'ar': '🇸🇦', 'hi': '🇮🇳', 'tr': '🇹🇷', 'nl': '🇳🇱', 'sv': '🇸🇪',
        'da': '🇩🇰', 'no': '🇳🇴', 'fi': '🇫🇮', 'pl': '🇵🇱', 'cs': '🇨🇿',
        'hu': '🇭🇺', 'ro': '🇷🇴', 'bg': '🇧🇬', 'hr': '🇭🇷', 'sk': '🇸🇰',
        'uk': '🇺🇦', 'th': '🇹🇭', 'vi': '🇻🇳', 'id': '🇮🇩', 'ms': '🇲🇾',
        'he': '🇮🇱', 'fa': '🇮🇷', 'bn': '🇧🇩', 'ta': '🇱🇰', 'ne': '🇳🇵'
    }
    return flag_map.get(lang_code, '🌐')