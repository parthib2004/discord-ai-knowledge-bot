"""
CreoBot Weather System Examples
===============================

This file shows examples of how the new weather system works.
"""

# Example weather commands users can run:

WEATHER_EXAMPLES = [
    {
        "command": "/weather",
        "city": "New York",
        "unit": "celsius",
        "description": "Get weather in Celsius (default)"
    },
    {
        "command": "/weather", 
        "city": "London",
        "unit": "fahrenheit",
        "description": "Get weather in Fahrenheit"
    },
    {
        "command": "/weather",
        "city": "Tokyo",
        "unit": "c",
        "description": "Short form for Celsius"
    },
    {
        "command": "/weather",
        "city": "Paris",
        "unit": "f",
        "description": "Short form for Fahrenheit"
    },
    {
        "command": "/weather",
        "city": "San Francisco",
        "description": "Default unit (Celsius)"
    }
]

def print_examples():
    print("🌤️  CreoBot Weather System Examples\n")
    print("=" * 50)
    
    for i, example in enumerate(WEATHER_EXAMPLES, 1):
        print(f"\n{i}. {example['description']}")
        print(f"   City: {example['city']}")
        
        if 'unit' in example:
            print(f"   Unit: {example['unit']}")
            full_cmd = f"/weather city:\"{example['city']}\" unit:{example['unit']}"
        else:
            print(f"   Unit: celsius (default)")
            full_cmd = f"/weather city:\"{example['city']}\""
        
        print(f"   Full Command: {full_cmd}")
    
    print(f"\n{'=' * 50}")
    print("🌤️ Weather Features:")
    print("✅ Current weather conditions")
    print("✅ Temperature (Celsius/Fahrenheit)")
    print("✅ Feels like temperature")
    print("✅ Humidity and pressure")
    print("✅ Wind speed and direction")
    print("✅ Visibility information")
    print("✅ Sunrise/sunset times")
    print("✅ Weather emojis (☀️🌧️❄️⛈️)")
    print("✅ Beautiful embed display")
    print("✅ Error handling for invalid cities")
    
    print(f"\n🔧 Setup Required:")
    print("1. Get free API key from: https://openweathermap.org/api")
    print("2. Add WEATHER_API_KEY=your_key_here to .env file")
    print("3. Install aiohttp: pip install aiohttp>=3.8.0")
    
    print(f"\n💡 Usage Tips:")
    print("• Use full city names for best results")
    print("• Include country for common city names (e.g., 'Paris, France')")
    print("• Both 'celsius'/'c' and 'fahrenheit'/'f' work")
    print("• Default unit is Celsius if not specified")

if __name__ == "__main__":
    print_examples()