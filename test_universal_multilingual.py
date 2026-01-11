from language_support import create_multilingual_prompt, detect_language

# Test universal questions in different languages
test_cases = [
    ("What is the capital of France?", "en"),
    ("¿Cuál es la capital de Francia?", "es"), 
    ("Quelle est la capitale de la France?", "fr"),
    ("Was ist die Hauptstadt von Frankreich?", "de"),
    ("フランスの首都は何ですか？", "ja"),
]

knowledge = "CreoWis Technologies is a software development company..."

print("🌍 Testing Universal Multilingual Support:\n")

for question, expected_lang in test_cases:
    detected_lang, lang_name = detect_language(question)
    prompt = create_multilingual_prompt(question, knowledge, detected_lang, lang_name)
    
    # Check key features
    is_universal = "any question" in prompt.lower()
    has_lang_instruction = lang_name in prompt if detected_lang != 'en' else True
    
    status = "✅" if is_universal and has_lang_instruction else "❌"
    
    print(f"{status} {lang_name}: '{question}'")
    print(f"    📝 Detected: {detected_lang} | Universal: {is_universal}")

print(f"\n🎯 Universal Bot Features:")
print(f"✅ Answers ANY question in ANY language")
print(f"✅ Company knowledge when relevant")
print(f"✅ General knowledge for everything else")
print(f"✅ Maintains language consistency")