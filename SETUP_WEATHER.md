# 🚀 Quick Weather Setup Guide

## Step 1: Get Free API Key
1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Click "Sign Up" (it's free!)
3. Verify your email
4. Go to "API Keys" in your dashboard
5. Copy your API key

## Step 2: Add to Environment
Open your `.env` file and add:
```
WEATHER_API_KEY=paste_your_api_key_here
```

## Step 3: Install Dependencies
Run this command:
```bash
pip install aiohttp>=3.8.0
```

## Step 4: Restart Bot
Restart your bot to load the new API key.

## Step 5: Test It!
Try this command in Discord:
```
/weather city:"London"
```

## ✅ That's it!
Your weather system is now ready to use!

### Example Commands:
```
/weather city:"New York" unit:fahrenheit
/weather city:"Tokyo" unit:celsius
/weather city:"Paris, France"
```

### Need Help?
- Check the full [WEATHER_GUIDE.md](WEATHER_GUIDE.md) for detailed documentation
- Make sure your API key is correct
- Try different city names if one doesn't work