# 🌤️ CreoBot Weather System

## Overview
CreoBot now includes a comprehensive weather information system that provides real-time weather data for any city worldwide using the OpenWeatherMap API.

## Setup Required

### 1. Get API Key
1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Free tier includes 1,000 calls/day (more than enough for most Discord servers)

### 2. Configure Environment
Add your API key to the `.env` file:
```
WEATHER_API_KEY=your_openweathermap_api_key_here
```

### 3. Install Dependencies
The bot automatically installs `aiohttp` for API requests:
```bash
pip install aiohttp>=3.8.0
```

## Command Usage

### `/weather` - Get Weather Information

**Syntax:**
```
/weather city:"City Name" unit:celsius
```

**Parameters:**
- `city` (required): Name of the city
- `unit` (optional): Temperature unit - `celsius`, `fahrenheit`, `c`, or `f` (default: celsius)

**Examples:**
```
/weather city:"New York"
/weather city:"London" unit:fahrenheit
/weather city:"Tokyo" unit:c
/weather city:"Paris, France" unit:f
```

## Weather Information Provided

### 🌡️ Temperature Data
- **Current Temperature**: Real-time temperature
- **Feels Like**: Apparent temperature considering humidity and wind
- **Temperature Range**: Daily min/max temperatures
- **Unit Conversion**: Automatic Celsius ↔ Fahrenheit conversion

### 🌦️ Weather Conditions
- **Description**: Clear description of current conditions
- **Weather Emoji**: Visual representation (☀️🌧️❄️⛈️☁️🌫️)
- **Weather ID**: Detailed condition classification

### 💨 Environmental Data
- **Humidity**: Relative humidity percentage
- **Pressure**: Atmospheric pressure in hPa
- **Wind**: Speed (m/s) and direction (compass)
- **Visibility**: How far you can see (when available)

### 🌅 Sun Information
- **Sunrise Time**: Local sunrise time
- **Sunset Time**: Local sunset time
- **Timezone**: Automatically adjusted to local time

## Weather Emojis

The bot uses contextual emojis based on weather conditions:

| Condition | Emoji | Weather ID Range |
|-----------|-------|------------------|
| Thunderstorm | ⛈️ | 200-232 |
| Drizzle | 🌦️ | 300-321 |
| Rain | 🌧️ | 500-531 |
| Snow | ❄️ | 600-622 |
| Fog/Haze | 🌫️ | 700-781 |
| Clear Sky | ☀️ | 800 |
| Clouds | ☁️ | 801-804 |
| Default | 🌤️ | Other |

## Example Output

```
⛈️ Weather in New York, US
Thunderstorms

🌡️ Temperature: 22.5°C
   Feels like 25.1°C

💧 Humidity: 78%
🔽 Pressure: 1013 hPa
💨 Wind: 5.2 m/s NW

📊 Range: 18.3°C - 26.7°C
👁️ Visibility: 10.0 km

🌅 Sun Times:
   Rise: 06:24
   Set: 19:47

Data from OpenWeatherMap • Times in local timezone
```

## Error Handling

The system provides helpful error messages for:

### City Not Found
```
❌ Weather Error: City 'Atlantis' not found. Please check the spelling and try again.
```

### API Key Issues
```
❌ Weather Error: Weather API key not configured. Please add WEATHER_API_KEY to your .env file.
```

### Invalid Units
```
❌ Error: Unit must be 'celsius', 'fahrenheit', 'c', or 'f'
```

### Service Errors
```
❌ Weather Error: Weather service error (Status: 429)
```

## Usage Tips

### 🎯 Best Practices
1. **Use Full City Names**: "San Francisco" instead of "SF"
2. **Include Country**: "Paris, France" vs "Paris, Texas"
3. **Check Spelling**: The API is sensitive to typos
4. **Use Common Names**: Official city names work best

### 🌍 International Support
- **Global Coverage**: Works for cities worldwide
- **Multiple Languages**: City names in local languages often work
- **Country Codes**: Use ISO country codes when needed

### ⚡ Performance
- **Fast Response**: Typically responds in 1-2 seconds
- **Cached Data**: OpenWeatherMap updates every 10 minutes
- **Rate Limits**: 1,000 calls/day on free tier

## Integration with Other Features

### 🤖 AI Assistant Integration
Users can also ask weather questions through the AI assistant:
```
/ask What's the weather like in Tokyo?
/ask Should I bring an umbrella in London today?
```

### 🗳️ Weather Polls
Create weather-related polls:
```
/poll question:"What's your favorite weather?" options:"Sunny, Rainy, Snowy, Cloudy"
```

## Troubleshooting

### Common Issues

1. **"API key not configured"**
   - Check your `.env` file has `WEATHER_API_KEY=your_key`
   - Restart the bot after adding the key

2. **"City not found"**
   - Check spelling and try full city name
   - Include country: "London, UK" vs "London, Canada"

3. **"Service error"**
   - Check your API key is valid
   - Verify you haven't exceeded rate limits

### Testing Your Setup
```
/weather city:"London" unit:celsius
```

If this works, your weather system is properly configured!

## Future Enhancements

Potential features for future versions:
- Weather forecasts (3-5 days)
- Weather alerts and notifications
- Weather maps and radar
- Historical weather data
- Weather-based recommendations
- Multiple city comparisons

---

**Ready to check the weather?** Try your first weather command:
```
/weather city:"Your City Name"
```