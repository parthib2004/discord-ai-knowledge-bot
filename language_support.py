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
    """Detect the language of the input text"""
    try:
        detected_lang = detect(text)
        return detected_lang, LANGUAGE_NAMES.get(detected_lang, detected_lang)
    except:
        return 'en', 'English'  # Default to English if detection fails

def create_multilingual_prompt(question, knowledge, detected_lang, lang_name):
    """Create a prompt that instructs the AI to respond in the detected language"""
    
    if detected_lang == 'en':
        # English prompt (original)
        return f"""You are a helpful company assistant. Use the following company knowledge to answer the user's question accurately and helpfully.

Company Knowledge:
{knowledge}

User Question: {question}

Instructions:
- Answer based on the company knowledge provided
- If the information isn't in the knowledge base, say so politely
- Be professional and helpful
- Keep responses concise but informative"""
    
    else:
        # Multi-language prompt
        return f"""You are a helpful company assistant. Use the following company knowledge to answer the user's question accurately and helpfully.

Company Knowledge:
{knowledge}

User Question: {question}

IMPORTANT INSTRUCTIONS:
- The user asked their question in {lang_name} ({detected_lang})
- You MUST respond in {lang_name} ({detected_lang}) - the same language as the user's question
- Answer based on the company knowledge provided
- If the information isn't in the knowledge base, say so politely in {lang_name}
- Be professional and helpful
- Keep responses concise but informative
- Maintain the same language throughout your entire response

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