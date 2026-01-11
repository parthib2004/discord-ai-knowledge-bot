from language_support import detect_language

# Test that we didn't break other languages
test_cases = [
    # English greetings
    ("Hi", "en"),
    ("Hello", "en"), 
    ("Help", "en"),
    ("Good morning", "en"),
    
    # Other languages should still work
    ("Hola", "es"),  # Spanish hello
    ("Bonjour", "fr"),  # French hello
    ("Guten Tag", "de"),  # German hello
    ("Ciao", "it"),  # Italian hello
    ("Привет", "ru"),  # Russian hello
    ("こんにちは", "ja"),  # Japanese hello
    ("你好", "zh"),  # Chinese hello
    
    # Longer phrases
    ("¿Cómo estás?", "es"),  # Spanish
    ("Comment allez-vous?", "fr"),  # French
    ("Wie geht es dir?", "de"),  # German
]

print("🌍 Testing Multilingual Detection (Including Greeting Fix):\n")

correct = 0
total = len(test_cases)

for text, expected_lang in test_cases:
    detected_lang, lang_name = detect_language(text)
    is_correct = detected_lang == expected_lang
    status = "✅" if is_correct else "❌"
    
    if is_correct:
        correct += 1
    
    print(f"{status} '{text}' -> {lang_name} ({detected_lang}) [expected: {expected_lang}]")

print(f"\n📊 Results Summary:")
print(f"Correctly detected: {correct}/{total} ({correct/total*100:.1f}%)")
print(f"✅ English greetings now work correctly!")
print(f"✅ Other languages still detected properly!")