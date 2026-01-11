import discord
from discord import app_commands
import google.genai as genai
import os
import asyncio
import aiohttp
import json
import re
from datetime import datetime, timedelta, UTC
from dotenv import load_dotenv
from prompts import build_prompt
from language_support import detect_language, create_multilingual_prompt, get_language_flag, LANGUAGE_NAMES

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Configure Gemini with the new API
client_genai = genai.Client(api_key=GEMINI_API_KEY)

# Store active reminders (in production, use a database)
active_reminders = {}

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

def load_knowledge():
    with open("knowledge_base.txt", "r", encoding="utf-8") as f:
        return f.read()

@tree.command(name="ask", description="Ask any question in any language - I can help with anything!")
async def ask(interaction: discord.Interaction, question: str, language: str = None):
    try:
        await interaction.response.defer()
    except discord.errors.NotFound:
        # Interaction already expired, can't respond
        return

    try:
        # Use manual language override if provided, otherwise detect
        if language and language.lower() in ['en', 'english']:
            detected_lang, lang_name = 'en', 'English'
        elif language:
            # Try to find the language code from the provided language
            lang_lower = language.lower()
            detected_lang = None
            for code, name in LANGUAGE_NAMES.items():
                if lang_lower == code or lang_lower == name.lower():
                    detected_lang, lang_name = code, name
                    break
            
            if not detected_lang:
                detected_lang, lang_name = detect_language(question)
        else:
            # Auto-detect the language of the question
            detected_lang, lang_name = detect_language(question)
        
        flag = get_language_flag(detected_lang)
        
        print(f"Detected language: {lang_name} ({detected_lang}) for question: {question}")
        
        knowledge = load_knowledge()
        
        # Use multilingual prompt instead of the original build_prompt
        prompt = create_multilingual_prompt(question, knowledge, detected_lang, lang_name)

        # Generate response using Gemini
        response = client_genai.models.generate_content(
            model='gemini-2.5-flash',
            contents=[{'parts': [{'text': prompt}]}]
        )
        
        answer = response.candidates[0].content.parts[0].text
        
        # Add language indicator to the response
        if detected_lang != 'en':
            answer = f"{flag} **Responding in {lang_name}**\n\n{answer}"
        
        # Discord has a 2000 character limit for messages
        if len(answer) > 2000:
            answer = answer[:1997] + "..."
            
        try:
            await interaction.followup.send(answer)
        except discord.errors.NotFound:
            # Interaction expired, can't send followup
            print("Interaction expired before sending response")
        
    except Exception as e:
        error_msg = str(e)
        print(f"Full error: {e}")
        
        try:
            if "quota" in error_msg.lower() or "limit" in error_msg.lower():
                await interaction.followup.send("❌ **API Quota Exceeded**\n\nThe Gemini API quota has been exceeded. Please check your usage at https://aistudio.google.com/")
            elif "api_key" in error_msg.lower() or "401" in error_msg:
                await interaction.followup.send("❌ **API Key Error**\n\nInvalid or missing Gemini API key. Please check your .env file.")
            else:
                await interaction.followup.send(f"❌ **Error**\n\nSomething went wrong: {error_msg}")
        except discord.errors.NotFound:
            # Interaction expired, can't send error message
            print("Interaction expired before sending error message")

@tree.command(name="languages", description="Show supported languages")
async def languages(interaction: discord.Interaction):
    try:
        await interaction.response.defer()
    except discord.errors.NotFound:
        return

    try:
        from language_support import LANGUAGE_NAMES, get_language_flag
        
        # Create a nice formatted list of supported languages
        lang_list = []
        for code, name in list(LANGUAGE_NAMES.items())[:20]:  # Show first 20 languages
            flag = get_language_flag(code)
            lang_list.append(f"{flag} **{name}** (`{code}`)")
        
        more_count = len(LANGUAGE_NAMES) - 20
        
        embed = discord.Embed(
            title="🌍 Supported Languages",
            description=f"I can understand and respond in **{len(LANGUAGE_NAMES)}+ languages**!\n\n" + 
                       "\n".join(lang_list) + 
                       f"\n\n*...and {more_count} more languages!*\n\n" +
                       "💡 **Just ask your question in any language and I'll respond in the same language!**",
            color=0x00ff00
        )
        
        embed.set_footer(text="Language detection is automatic - no setup required!")
        
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        await interaction.followup.send(f"❌ Error showing languages: {str(e)}")

@tree.command(name="help", description="Show all available commands and how to use the bot")
async def help_command(interaction: discord.Interaction):
    try:
        await interaction.response.defer()
    except discord.errors.NotFound:
        return

    try:
        embed = discord.Embed(
            title="🤖 CreoBot - Universal AI Assistant",
            description="I'm your intelligent AI assistant powered by Google Gemini! I can answer any question you have.",
            color=0x0099ff
        )
        
        embed.add_field(
            name="📝 `/ask [question] [language]`",
            value="Ask **any question** in **any language**\n"
                  "• General: `/ask What is the capital of France?`\n"
                  "• Company: `/ask What are the office hours?`\n"
                  "• Tech: `/ask How does React work?`\n"
                  "• Force English: `/ask [question] language:English`",
            inline=False
        )
        
        embed.add_field(
            name="📊 `/poll [question] [options] [duration]`",
            value="Create a multi-option poll with voting\n"
                  "• Example: `/poll question:\"Favorite color?\" options:\"Red, Blue, Green\" duration:60`\n"
                  "• Duration in minutes (10-1440)",
            inline=False
        )
        
        embed.add_field(
            name="⚡ `/quickpoll [question] [duration]`",
            value="Create a simple Yes/No poll\n"
                  "• Example: `/quickpoll question:\"Should we order pizza?\" duration:30`\n"
                  "• Perfect for quick decisions",
            inline=False
        )
        
        embed.add_field(
            name="🌤️ `/weather [city] [unit]`",
            value="Get current weather information\n"
                  "• Example: `/weather city:\"New York\" unit:celsius`\n"
                  "• Units: celsius, fahrenheit (default: celsius)",
            inline=False
        )
        
        embed.add_field(
            name="⏰ `/remind [time] [message]`",
            value="Set a personal reminder\n"
                  "• Example: `/remind time:5m message:\"Check the server\"`\n"
                  "• Time: 5m, 2h, 30s, 1d (10s - 7 days)",
            inline=False
        )
        
        embed.add_field(
            name="👥 `/reminduser [user] [time] [message]`",
            value="Set a reminder for another user\n"
                  "• Example: `/reminduser user:@john time:30m message:\"Meeting\"`\n"
                  "• Great for team coordination",
            inline=False
        )
        
        embed.add_field(
            name="📝 `/reminders` • `/groupreminders` • 🗑️ `/cancel [id]`",
            value="Manage your reminders\n"
                  "• `/reminders` - Your personal reminders\n"
                  "• `/groupreminders` - Reminders you set for others\n"
                  "• `/cancel reminder_id` - Cancel any reminder",
            inline=False
        )
        
        embed.add_field(
            name="🧪 `/testreminder [message]`",
            value="Test reminder delivery (troubleshooting)\n"
                  "• Example: `/testreminder message:\"Test notification\"`\n"
                  "• Sends immediately to check if notifications work",
            inline=False
        )
        
        embed.add_field(
            name="🌍 `/languages`",
            value="View all 70+ supported languages\n"
                  "• Automatic language detection\n"
                  "• Responses in your native language",
            inline=False
        )
        
        embed.add_field(
            name="📊 `/stats`",
            value="View bot statistics and performance\n"
                  "• Response times\n"
                  "• Popular questions",
            inline=False
        )
        
        embed.add_field(
            name="ℹ️ `/info`",
            value="Get information about the bot\n"
                  "• Version and features\n"
                  "• Technical details",
            inline=False
        )
        
        embed.add_field(
            name="🎯 **Features**",
            value="✅ Multi-language support (70+ languages)\n"
                  "✅ AI-powered responses to ANY question\n"
                  "✅ Interactive polls & voting system\n"
                  "✅ Real-time weather information\n"
                  "✅ Personal & group reminder system\n"
                  "✅ Company knowledge integration\n"
                  "✅ General knowledge & tech support\n"
                  "✅ Fast response times\n"
                  "✅ Automatic language detection",
            inline=False
        )
        
        embed.set_footer(text="💡 Tip: Ask me anything - from company info to general knowledge!")
        embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
        
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        await interaction.followup.send(f"❌ Error showing help: {str(e)}")

@tree.command(name="info", description="Get information about the bot")
async def info(interaction: discord.Interaction):
    try:
        await interaction.response.defer()
    except discord.errors.NotFound:
        return

    try:
        embed = discord.Embed(
            title="🤖 CreoBot Information",
            color=0x00ff00
        )
        
        embed.add_field(
            name="🧠 AI Model",
            value="Google Gemini 2.5 Flash",
            inline=True
        )
        
        embed.add_field(
            name="🌍 Languages",
            value="70+ Supported",
            inline=True
        )
        
        embed.add_field(
            name="⚡ Response Time",
            value="< 3 seconds",
            inline=True
        )
        
        embed.add_field(
            name="🔧 Version",
            value="2.0.0 - Multi-Language",
            inline=True
        )
        
        embed.add_field(
            name="📅 Last Updated",
            value="January 2026",
            inline=True
        )
        
        embed.add_field(
            name="🏆 Features",
            value="Universal AI + Polls + Weather + Reminders",
            inline=True
        )
        
        embed.add_field(
            name="💻 Technology Stack",
            value="• Python 3.12\n• Discord.py\n• Google GenAI\n• Language Detection\n• Interactive Polling System\n• OpenWeatherMap API\n• Async Reminder System",
            inline=False
        )
        
        embed.set_footer(text="Built to answer any question in any language")
        
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        await interaction.followup.send(f"❌ Error showing info: {str(e)}")

@tree.command(name="stats", description="View bot usage statistics")
async def stats(interaction: discord.Interaction):
    try:
        await interaction.response.defer()
    except discord.errors.NotFound:
        return

    try:
        # Get basic stats (you can expand this with actual tracking)
        import psutil
        import time
        
        # Bot uptime (simplified)
        uptime = "Online and Ready"
        
        # Memory usage
        memory_usage = psutil.virtual_memory().percent
        
        embed = discord.Embed(
            title="📊 Bot Statistics",
            color=0xff9900
        )
        
        embed.add_field(
            name="🟢 Status",
            value=uptime,
            inline=True
        )
        
        embed.add_field(
            name="💾 Memory Usage",
            value=f"{memory_usage:.1f}%",
            inline=True
        )
        
        embed.add_field(
            name="🌍 Languages Detected Today",
            value="Multiple",
            inline=True
        )
        
        embed.add_field(
            name="⚡ Average Response Time",
            value="< 2 seconds",
            inline=True
        )
        
        embed.add_field(
            name="🤖 AI Model",
            value="Gemini 2.5 Flash",
            inline=True
        )
        
        embed.add_field(
            name="📈 Performance",
            value="Optimal",
            inline=True
        )
        
        embed.set_footer(text="Statistics updated in real-time")
        
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        await interaction.followup.send(f"❌ Error showing stats: {str(e)}")

@tree.command(name="poll", description="Create a poll with multiple options")
async def create_poll(interaction: discord.Interaction, question: str, options: str, duration: int = 60):
    try:
        await interaction.response.defer()
    except discord.errors.NotFound:
        return

    try:
        # Parse options (comma-separated)
        option_list = [opt.strip() for opt in options.split(',') if opt.strip()]
        
        # Validate input
        if len(option_list) < 2:
            await interaction.followup.send("❌ **Error**: You need at least 2 options for a poll!\n\nExample: `/poll question:\"What's your favorite color?\" options:\"Red, Blue, Green\"`")
            return
        
        if len(option_list) > 10:
            await interaction.followup.send("❌ **Error**: Maximum 10 options allowed per poll.")
            return
        
        if duration < 10 or duration > 1440:  # 10 seconds to 24 hours
            await interaction.followup.send("❌ **Error**: Duration must be between 10 seconds and 1440 minutes (24 hours).")
            return
        
        # Emoji numbers for options
        number_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        
        # Create poll embed
        embed = discord.Embed(
            title="📊 Poll",
            description=f"**{question}**",
            color=0x00ff00,
            timestamp=discord.utils.utcnow()
        )
        
        # Add options to embed
        options_text = ""
        for i, option in enumerate(option_list):
            options_text += f"{number_emojis[i]} {option}\n"
        
        embed.add_field(
            name="Options:",
            value=options_text,
            inline=False
        )
        
        embed.add_field(
            name="⏱️ Duration:",
            value=f"{duration} minutes",
            inline=True
        )
        
        embed.add_field(
            name="👤 Created by:",
            value=interaction.user.mention,
            inline=True
        )
        
        embed.set_footer(text="React with the corresponding emoji to vote!")
        
        # Send poll message
        poll_message = await interaction.followup.send(embed=embed)
        
        # Add reaction emojis
        for i in range(len(option_list)):
            await poll_message.add_reaction(number_emojis[i])
        
        # Store poll data for later results
        poll_data = {
            'question': question,
            'options': option_list,
            'creator': interaction.user.id,
            'channel': interaction.channel.id,
            'message_id': poll_message.id,
            'duration': duration,
            'emojis': number_emojis[:len(option_list)]
        }
        
        # Schedule poll end (simplified - in production you'd use a database)
        import asyncio
        asyncio.create_task(end_poll_after_duration(poll_data, duration * 60))
        
    except Exception as e:
        await interaction.followup.send(f"❌ **Error creating poll**: {str(e)}")

async def end_poll_after_duration(poll_data, duration_seconds):
    """End poll after specified duration"""
    await asyncio.sleep(duration_seconds)
    
    try:
        channel = client.get_channel(poll_data['channel'])
        if not channel:
            return
            
        message = await channel.fetch_message(poll_data['message_id'])
        if not message:
            return
        
        # Count votes from reactions
        results = {}
        total_votes = 0
        
        for reaction in message.reactions:
            if str(reaction.emoji) in poll_data['emojis']:
                emoji_index = poll_data['emojis'].index(str(reaction.emoji))
                option = poll_data['options'][emoji_index]
                vote_count = reaction.count - 1  # Subtract bot's reaction
                results[option] = vote_count
                total_votes += vote_count
        
        # Create results embed
        embed = discord.Embed(
            title="📊 Poll Results",
            description=f"**{poll_data['question']}**",
            color=0xff9900,
            timestamp=discord.utils.utcnow()
        )
        
        if total_votes == 0:
            embed.add_field(
                name="Results:",
                value="No votes were cast 😢",
                inline=False
            )
        else:
            results_text = ""
            sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
            
            for i, (option, votes) in enumerate(sorted_results):
                percentage = (votes / total_votes * 100) if total_votes > 0 else 0
                bar_length = int(percentage / 10)
                bar = "█" * bar_length + "░" * (10 - bar_length)
                
                medal = ""
                if i == 0 and votes > 0:
                    medal = "🥇 "
                elif i == 1 and votes > 0:
                    medal = "🥈 "
                elif i == 2 and votes > 0:
                    medal = "🥉 "
                
                results_text += f"{medal}**{option}**\n{bar} {votes} votes ({percentage:.1f}%)\n\n"
            
            embed.add_field(
                name="Final Results:",
                value=results_text,
                inline=False
            )
        
        embed.add_field(
            name="📈 Total Votes:",
            value=str(total_votes),
            inline=True
        )
        
        embed.set_footer(text="Poll has ended!")
        
        await channel.send(embed=embed)
        
    except Exception as e:
        print(f"Error ending poll: {e}")

@tree.command(name="quickpoll", description="Create a simple Yes/No poll")
async def quick_poll(interaction: discord.Interaction, question: str, duration: int = 30):
    try:
        await interaction.response.defer()
    except discord.errors.NotFound:
        return

    try:
        if duration < 10 or duration > 1440:
            await interaction.followup.send("❌ **Error**: Duration must be between 10 seconds and 1440 minutes (24 hours).")
            return
        
        embed = discord.Embed(
            title="⚡ Quick Poll",
            description=f"**{question}**",
            color=0x0099ff,
            timestamp=discord.utils.utcnow()
        )
        
        embed.add_field(
            name="Options:",
            value="✅ Yes\n❌ No",
            inline=False
        )
        
        embed.add_field(
            name="⏱️ Duration:",
            value=f"{duration} minutes",
            inline=True
        )
        
        embed.add_field(
            name="👤 Created by:",
            value=interaction.user.mention,
            inline=True
        )
        
        embed.set_footer(text="React with ✅ for Yes or ❌ for No!")
        
        poll_message = await interaction.followup.send(embed=embed)
        
        # Add reactions
        await poll_message.add_reaction("✅")
        await poll_message.add_reaction("❌")
        
        # Schedule poll end
        poll_data = {
            'question': question,
            'options': ['Yes', 'No'],
            'creator': interaction.user.id,
            'channel': interaction.channel.id,
            'message_id': poll_message.id,
            'duration': duration,
            'emojis': ['✅', '❌']
        }
        
        import asyncio
        asyncio.create_task(end_poll_after_duration(poll_data, duration * 60))
        
    except Exception as e:
        await interaction.followup.send(f"❌ **Error creating quick poll**: {str(e)}")

async def get_weather_data(city):
    """Fetch weather data from OpenWeatherMap API"""
    if not WEATHER_API_KEY or WEATHER_API_KEY == "your_openweathermap_api_key_here":
        return None, "Weather API key not configured. Please add WEATHER_API_KEY to your .env file."
    
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': WEATHER_API_KEY,
        'units': 'metric'  # Use Celsius
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data, None
                elif response.status == 404:
                    return None, f"City '{city}' not found. Please check the spelling and try again."
                else:
                    return None, f"Weather service error (Status: {response.status})"
    except Exception as e:
        return None, f"Failed to fetch weather data: {str(e)}"

def get_weather_emoji(weather_main, weather_id):
    """Get appropriate emoji for weather condition"""
    weather_main = weather_main.lower()
    
    # Thunderstorm
    if 200 <= weather_id <= 232:
        return "⛈️"
    # Drizzle
    elif 300 <= weather_id <= 321:
        return "🌦️"
    # Rain
    elif 500 <= weather_id <= 531:
        return "🌧️"
    # Snow
    elif 600 <= weather_id <= 622:
        return "❄️"
    # Atmosphere (fog, haze, etc.)
    elif 700 <= weather_id <= 781:
        return "🌫️"
    # Clear
    elif weather_id == 800:
        return "☀️"
    # Clouds
    elif 801 <= weather_id <= 804:
        return "☁️"
    else:
        return "🌤️"

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit"""
    return (celsius * 9/5) + 32

@tree.command(name="weather", description="Get current weather information for any city")
async def weather(interaction: discord.Interaction, city: str, unit: str = "celsius"):
    try:
        await interaction.response.defer()
    except discord.errors.NotFound:
        return

    try:
        # Validate unit parameter
        unit = unit.lower()
        if unit not in ['celsius', 'fahrenheit', 'c', 'f']:
            await interaction.followup.send("❌ **Error**: Unit must be 'celsius', 'fahrenheit', 'c', or 'f'")
            return
        
        # Fetch weather data
        weather_data, error = await get_weather_data(city)
        
        if error:
            await interaction.followup.send(f"❌ **Weather Error**: {error}")
            return
        
        if not weather_data:
            await interaction.followup.send("❌ **Error**: Unable to fetch weather data")
            return
        
        # Extract weather information
        main = weather_data['main']
        weather = weather_data['weather'][0]
        wind = weather_data.get('wind', {})
        sys_data = weather_data['sys']
        
        # Temperature conversion
        temp_c = main['temp']
        feels_like_c = main['feels_like']
        
        if unit in ['fahrenheit', 'f']:
            temp = f"{celsius_to_fahrenheit(temp_c):.1f}°F"
            feels_like = f"{celsius_to_fahrenheit(feels_like_c):.1f}°F"
            unit_symbol = "°F"
        else:
            temp = f"{temp_c:.1f}°C"
            feels_like = f"{feels_like_c:.1f}°C"
            unit_symbol = "°C"
        
        # Get weather emoji
        weather_emoji = get_weather_emoji(weather['main'], weather['id'])
        
        # Create weather embed
        embed = discord.Embed(
            title=f"{weather_emoji} Weather in {weather_data['name']}, {sys_data['country']}",
            description=f"**{weather['description'].title()}**",
            color=0x87CEEB,  # Sky blue
            timestamp=datetime.now(UTC)
        )
        
        # Main weather info
        embed.add_field(
            name="🌡️ Temperature",
            value=f"**{temp}**\nFeels like {feels_like}",
            inline=True
        )
        
        embed.add_field(
            name="💧 Humidity",
            value=f"{main['humidity']}%",
            inline=True
        )
        
        embed.add_field(
            name="🔽 Pressure",
            value=f"{main['pressure']} hPa",
            inline=True
        )
        
        # Wind information
        if wind:
            wind_speed = wind.get('speed', 0)
            wind_deg = wind.get('deg', 0)
            
            # Convert wind direction to compass
            directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                         "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
            direction = directions[int((wind_deg + 11.25) / 22.5) % 16]
            
            embed.add_field(
                name="💨 Wind",
                value=f"{wind_speed} m/s {direction}",
                inline=True
            )
        
        # Temperature range
        if 'temp_min' in main and 'temp_max' in main:
            if unit in ['fahrenheit', 'f']:
                temp_min = f"{celsius_to_fahrenheit(main['temp_min']):.1f}°F"
                temp_max = f"{celsius_to_fahrenheit(main['temp_max']):.1f}°F"
            else:
                temp_min = f"{main['temp_min']:.1f}°C"
                temp_max = f"{main['temp_max']:.1f}°C"
            
            embed.add_field(
                name="📊 Range",
                value=f"{temp_min} - {temp_max}",
                inline=True
            )
        
        # Visibility (if available)
        if 'visibility' in weather_data:
            visibility_km = weather_data['visibility'] / 1000
            embed.add_field(
                name="👁️ Visibility",
                value=f"{visibility_km:.1f} km",
                inline=True
            )
        
        # Sunrise/Sunset
        if 'sunrise' in sys_data and 'sunset' in sys_data:
            sunrise = datetime.fromtimestamp(sys_data['sunrise']).strftime('%H:%M')
            sunset = datetime.fromtimestamp(sys_data['sunset']).strftime('%H:%M')
            embed.add_field(
                name="🌅 Sun Times",
                value=f"Rise: {sunrise}\nSet: {sunset}",
                inline=True
            )
        
        embed.set_footer(text="Data from OpenWeatherMap • Times in local timezone")
        
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        await interaction.followup.send(f"❌ **Error**: {str(e)}")

def parse_time_input(time_str):
    """Parse various time input formats into seconds"""
    time_str = time_str.lower().strip()
    
    # Pattern for number + unit (e.g., "5m", "2h", "30s")
    pattern = r'^(\d+)\s*(s|sec|second|seconds|m|min|minute|minutes|h|hr|hour|hours|d|day|days)$'
    match = re.match(pattern, time_str)
    
    if match:
        number = int(match.group(1))
        unit = match.group(2)
        
        # Convert to seconds
        if unit in ['s', 'sec', 'second', 'seconds']:
            return number
        elif unit in ['m', 'min', 'minute', 'minutes']:
            return number * 60
        elif unit in ['h', 'hr', 'hour', 'hours']:
            return number * 3600
        elif unit in ['d', 'day', 'days']:
            return number * 86400
    
    # Try to parse as just minutes if it's a plain number
    try:
        minutes = int(time_str)
        if 1 <= minutes <= 10080:  # 1 minute to 1 week
            return minutes * 60
    except ValueError:
        pass
    
    return None

def format_time_remaining(seconds):
    """Format seconds into human-readable time"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m"
    elif seconds < 86400:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        if minutes > 0:
            return f"{hours}h {minutes}m"
        return f"{hours}h"
    else:
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        if hours > 0:
            return f"{days}d {hours}h"
        return f"{days}d"

async def send_reminder(user_id, channel_id, message, reminder_id):
    """Send the reminder message"""
    try:
        print(f"🔔 Attempting to send reminder {reminder_id} to user {user_id} in channel {channel_id}")
        
        channel = client.get_channel(channel_id)
        if not channel:
            print(f"❌ Channel {channel_id} not found for reminder {reminder_id}")
            return
        
        # Try to get user from cache first, then fetch if not found
        user = client.get_user(user_id)
        if not user:
            try:
                user = await client.fetch_user(user_id)
                print(f"✅ User {user_id} fetched from Discord API")
            except discord.NotFound:
                print(f"❌ User {user_id} not found on Discord for reminder {reminder_id}")
                return
            except discord.HTTPException as e:
                print(f"❌ Error fetching user {user_id}: {e}")
                return
        
        # Get reminder data to check if it's a group reminder
        reminder_data = active_reminders.get(reminder_id, {})
        is_group_reminder = reminder_data.get('is_group_reminder', False)
        creator_id = reminder_data.get('creator_id')
        
        embed = discord.Embed(
            title="⏰ Reminder",
            description=f"**{message}**",
            color=0xff6b6b,
            timestamp=datetime.now(UTC)
        )
        
        embed.add_field(
            name="👤 For:",
            value=user.mention,
            inline=True
        )
        
        # If it's a group reminder, show who set it
        if is_group_reminder and creator_id:
            creator = client.get_user(creator_id)
            if not creator:
                try:
                    creator = await client.fetch_user(creator_id)
                except:
                    creator = None
            
            if creator:
                embed.add_field(
                    name="👨‍💼 Set by:",
                    value=creator.mention,
                    inline=True
                )
        
        embed.set_footer(text=f"Reminder ID: {reminder_id}")
        
        # Send the reminder message
        reminder_message = await channel.send(f"{user.mention}", embed=embed)
        print(f"✅ Reminder {reminder_id} sent successfully! Message ID: {reminder_message.id}")
        
        # Remove from active reminders
        if reminder_id in active_reminders:
            del active_reminders[reminder_id]
            print(f"🗑️ Reminder {reminder_id} removed from active reminders")
            
    except discord.Forbidden:
        print(f"❌ No permission to send reminder {reminder_id} in channel {channel_id}")
    except discord.HTTPException as e:
        print(f"❌ HTTP error sending reminder {reminder_id}: {e}")
    except Exception as e:
        print(f"❌ Error sending reminder {reminder_id}: {e}")

@tree.command(name="remind", description="Set a reminder for yourself")
async def remind_me(interaction: discord.Interaction, time: str, message: str):
    try:
        await interaction.response.defer()
    except discord.errors.NotFound:
        return

    try:
        # Parse the time input
        seconds = parse_time_input(time)
        
        if seconds is None:
            await interaction.followup.send(
                "❌ **Invalid Time Format**\n\n"
                "**Valid formats:**\n"
                "• `5m` or `5 minutes`\n"
                "• `2h` or `2 hours`\n"
                "• `30s` or `30 seconds`\n"
                "• `1d` or `1 day`\n"
                "• `120` (plain number = minutes)\n\n"
                "**Examples:**\n"
                "• `/remind time:5m message:\"Check the server\"`\n"
                "• `/remind time:2h message:\"Team meeting\"`"
            )
            return
        
        # Validate time range (10 seconds to 7 days)
        if seconds < 10:
            await interaction.followup.send("❌ **Error**: Minimum reminder time is 10 seconds.")
            return
        
        if seconds > 604800:  # 7 days
            await interaction.followup.send("❌ **Error**: Maximum reminder time is 7 days.")
            return
        
        # Generate unique reminder ID
        import uuid
        reminder_id = str(uuid.uuid4())[:8]
        
        # Store reminder data
        reminder_data = {
            'user_id': interaction.user.id,
            'channel_id': interaction.channel.id,
            'message': message,
            'created_at': datetime.now(UTC),
            'duration_seconds': seconds
        }
        
        active_reminders[reminder_id] = reminder_data
        
        # Schedule the reminder
        asyncio.create_task(schedule_reminder(reminder_id, seconds))
        
        # Create confirmation embed
        embed = discord.Embed(
            title="✅ Reminder Set",
            description=f"**{message}**",
            color=0x00ff00,
            timestamp=datetime.now(UTC)
        )
        
        embed.add_field(
            name="⏱️ Time:",
            value=format_time_remaining(seconds),
            inline=True
        )
        
        embed.add_field(
            name="📍 Channel:",
            value=interaction.channel.mention,
            inline=True
        )
        
        embed.add_field(
            name="🆔 ID:",
            value=f"`{reminder_id}`",
            inline=True
        )
        
        embed.set_footer(text="Use /reminders to view all your active reminders")
        
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        await interaction.followup.send(f"❌ **Error setting reminder**: {str(e)}")

async def schedule_reminder(reminder_id, delay_seconds):
    """Schedule a reminder to be sent after delay"""
    print(f"⏰ Scheduling reminder {reminder_id} for {delay_seconds} seconds")
    await asyncio.sleep(delay_seconds)
    
    print(f"⏰ Time's up! Processing reminder {reminder_id}")
    
    if reminder_id in active_reminders:
        reminder_data = active_reminders[reminder_id]
        print(f"📋 Reminder data found for {reminder_id}: user={reminder_data['user_id']}, channel={reminder_data['channel_id']}")
        await send_reminder(
            reminder_data['user_id'],
            reminder_data['channel_id'],
            reminder_data['message'],
            reminder_id
        )
    else:
        print(f"❌ Reminder {reminder_id} not found in active reminders when trying to send")

@tree.command(name="reminders", description="View your active reminders")
async def view_reminders(interaction: discord.Interaction):
    try:
        await interaction.response.defer()
    except discord.errors.NotFound:
        return

    try:
        user_reminders = []
        current_time = datetime.now(UTC)
        
        # Find user's reminders
        for reminder_id, data in active_reminders.items():
            if data['user_id'] == interaction.user.id:
                # Calculate remaining time
                elapsed = (current_time - data['created_at']).total_seconds()
                remaining = max(0, data['duration_seconds'] - elapsed)
                
                if remaining > 0:
                    user_reminders.append({
                        'id': reminder_id,
                        'message': data['message'],
                        'remaining': remaining,
                        'channel_id': data['channel_id']
                    })
        
        if not user_reminders:
            embed = discord.Embed(
                title="📝 Your Reminders",
                description="You have no active reminders.",
                color=0x95a5a6
            )
            embed.add_field(
                name="💡 Create a Reminder",
                value="Use `/remind time:5m message:\"Your reminder\"`",
                inline=False
            )
        else:
            embed = discord.Embed(
                title="📝 Your Active Reminders",
                description=f"You have {len(user_reminders)} active reminder(s)",
                color=0x3498db,
                timestamp=datetime.now(UTC)
            )
            
            for i, reminder in enumerate(user_reminders[:10], 1):  # Show max 10
                channel = client.get_channel(reminder['channel_id'])
                channel_name = channel.name if channel else "Unknown"
                
                embed.add_field(
                    name=f"⏰ Reminder {i}",
                    value=f"**Message:** {reminder['message'][:50]}{'...' if len(reminder['message']) > 50 else ''}\n"
                          f"**Time Left:** {format_time_remaining(int(reminder['remaining']))}\n"
                          f"**Channel:** #{channel_name}\n"
                          f"**ID:** `{reminder['id']}`",
                    inline=False
                )
            
            if len(user_reminders) > 10:
                embed.add_field(
                    name="📊 Note",
                    value=f"Showing first 10 of {len(user_reminders)} reminders",
                    inline=False
                )
        
        embed.set_footer(text="Use /cancel reminder_id to cancel a reminder")
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        await interaction.followup.send(f"❌ **Error**: {str(e)}")

@tree.command(name="cancel", description="Cancel a reminder by ID")
async def cancel_reminder(interaction: discord.Interaction, reminder_id: str):
    try:
        await interaction.response.defer()
    except discord.errors.NotFound:
        return

    try:
        reminder_id = reminder_id.strip()
        
        # Check if reminder exists
        if reminder_id not in active_reminders:
            await interaction.followup.send(f"❌ **Error**: Reminder `{reminder_id}` not found.")
            return
        
        reminder_data = active_reminders[reminder_id]
        is_group_reminder = reminder_data.get('is_group_reminder', False)
        
        # Check permissions
        can_cancel = False
        cancel_reason = ""
        
        if is_group_reminder:
            # For group reminders, allow both creator and target to cancel
            if reminder_data.get('creator_id') == interaction.user.id:
                can_cancel = True
                cancel_reason = "creator"
            elif reminder_data['user_id'] == interaction.user.id:
                can_cancel = True
                cancel_reason = "target"
        else:
            # For personal reminders, only the user can cancel
            if reminder_data['user_id'] == interaction.user.id:
                can_cancel = True
                cancel_reason = "owner"
        
        if not can_cancel:
            await interaction.followup.send("❌ **Error**: You can only cancel your own reminders or reminders set for you.")
            return
        
        # Cancel the reminder
        del active_reminders[reminder_id]
        
        # Create appropriate embed based on reminder type
        if is_group_reminder:
            embed = discord.Embed(
                title="🗑️ Group Reminder Cancelled",
                description=f"**{reminder_data['message']}**",
                color=0xe74c3c,
                timestamp=datetime.now(UTC)
            )
            
            target_user = client.get_user(reminder_data['user_id'])
            creator_user = client.get_user(reminder_data.get('creator_id'))
            
            embed.add_field(
                name="👤 Was for:",
                value=target_user.mention if target_user else "Unknown User",
                inline=True
            )
            
            if creator_user:
                embed.add_field(
                    name="👨‍💼 Set by:",
                    value=creator_user.mention,
                    inline=True
                )
            
            embed.add_field(
                name="🗑️ Cancelled by:",
                value=f"{interaction.user.mention} ({cancel_reason})",
                inline=True
            )
        else:
            embed = discord.Embed(
                title="🗑️ Reminder Cancelled",
                description=f"**{reminder_data['message']}**",
                color=0xe74c3c,
                timestamp=datetime.now(UTC)
            )
        
        embed.add_field(
            name="🆔 Cancelled ID:",
            value=f"`{reminder_id}`",
            inline=False
        )
        
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        await interaction.followup.send(f"❌ **Error**: {str(e)}")

@tree.command(name="reminduser", description="Set a reminder for another user")
async def remind_user(interaction: discord.Interaction, user: discord.Member, time: str, message: str):
    try:
        await interaction.response.defer()
    except discord.errors.NotFound:
        return

    try:
        # Parse the time input
        seconds = parse_time_input(time)
        
        if seconds is None:
            await interaction.followup.send(
                "❌ **Invalid Time Format**\n\n"
                "**Valid formats:**\n"
                "• `5m` or `5 minutes`\n"
                "• `2h` or `2 hours`\n"
                "• `30s` or `30 seconds`\n"
                "• `1d` or `1 day`\n"
                "• `120` (plain number = minutes)\n\n"
                "**Examples:**\n"
                "• `/reminduser user:@john time:5m message:\"Check the server\"`\n"
                "• `/reminduser user:@sarah time:2h message:\"Team meeting\"`"
            )
            return
        
        # Validate time range (10 seconds to 7 days)
        if seconds < 10:
            await interaction.followup.send("❌ **Error**: Minimum reminder time is 10 seconds.")
            return
        
        if seconds > 604800:  # 7 days
            await interaction.followup.send("❌ **Error**: Maximum reminder time is 7 days.")
            return
        
        # Check if user is trying to remind themselves
        if user.id == interaction.user.id:
            await interaction.followup.send("💡 **Tip**: Use `/remind` to set reminders for yourself!")
            return
        
        # Check if user is a bot
        if user.bot:
            await interaction.followup.send("❌ **Error**: Cannot set reminders for bots.")
            return
        
        # Generate unique reminder ID
        import uuid
        reminder_id = str(uuid.uuid4())[:8]
        
        # Store reminder data
        reminder_data = {
            'user_id': user.id,  # Who gets the reminder
            'creator_id': interaction.user.id,  # Who created it
            'channel_id': interaction.channel.id,
            'message': message,
            'created_at': datetime.now(UTC),
            'duration_seconds': seconds,
            'is_group_reminder': True
        }
        
        active_reminders[reminder_id] = reminder_data
        
        # Schedule the reminder
        asyncio.create_task(schedule_reminder(reminder_id, seconds))
        
        # Create confirmation embed
        embed = discord.Embed(
            title="✅ Group Reminder Set",
            description=f"**{message}**",
            color=0x00ff00,
            timestamp=datetime.now(UTC)
        )
        
        embed.add_field(
            name="👤 For:",
            value=user.mention,
            inline=True
        )
        
        embed.add_field(
            name="⏱️ Time:",
            value=format_time_remaining(seconds),
            inline=True
        )
        
        embed.add_field(
            name="📍 Channel:",
            value=interaction.channel.mention,
            inline=True
        )
        
        embed.add_field(
            name="👨‍💼 Set by:",
            value=interaction.user.mention,
            inline=True
        )
        
        embed.add_field(
            name="🆔 ID:",
            value=f"`{reminder_id}`",
            inline=True
        )
        
        embed.set_footer(text="The user will be notified when the reminder triggers")
        
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        await interaction.followup.send(f"❌ **Error setting group reminder**: {str(e)}")

@tree.command(name="groupreminders", description="View reminders you've set for others")
async def view_group_reminders(interaction: discord.Interaction):
    try:
        await interaction.response.defer()
    except discord.errors.NotFound:
        return

    try:
        user_group_reminders = []
        current_time = datetime.now(UTC)
        
        # Find reminders created by this user for others
        for reminder_id, data in active_reminders.items():
            if (data.get('creator_id') == interaction.user.id and 
                data.get('is_group_reminder', False)):
                # Calculate remaining time
                elapsed = (current_time - data['created_at']).total_seconds()
                remaining = max(0, data['duration_seconds'] - elapsed)
                
                if remaining > 0:
                    target_user = client.get_user(data['user_id'])
                    user_group_reminders.append({
                        'id': reminder_id,
                        'message': data['message'],
                        'remaining': remaining,
                        'channel_id': data['channel_id'],
                        'target_user': target_user.display_name if target_user else "Unknown User"
                    })
        
        if not user_group_reminders:
            embed = discord.Embed(
                title="👥 Your Group Reminders",
                description="You haven't set any reminders for other users.",
                color=0x95a5a6
            )
            embed.add_field(
                name="💡 Create a Group Reminder",
                value="Use `/reminduser user:@someone time:5m message:\"Your reminder\"`",
                inline=False
            )
        else:
            embed = discord.Embed(
                title="👥 Your Group Reminders",
                description=f"You have {len(user_group_reminders)} active group reminder(s)",
                color=0x9b59b6,
                timestamp=datetime.now(UTC)
            )
            
            for i, reminder in enumerate(user_group_reminders[:10], 1):  # Show max 10
                channel = client.get_channel(reminder['channel_id'])
                channel_name = channel.name if channel else "Unknown"
                
                embed.add_field(
                    name=f"⏰ Group Reminder {i}",
                    value=f"**For:** {reminder['target_user']}\n"
                          f"**Message:** {reminder['message'][:50]}{'...' if len(reminder['message']) > 50 else ''}\n"
                          f"**Time Left:** {format_time_remaining(int(reminder['remaining']))}\n"
                          f"**Channel:** #{channel_name}\n"
                          f"**ID:** `{reminder['id']}`",
                    inline=False
                )
            
            if len(user_group_reminders) > 10:
                embed.add_field(
                    name="📊 Note",
                    value=f"Showing first 10 of {len(user_group_reminders)} group reminders",
                    inline=False
                )
        
        embed.set_footer(text="Use /cancel reminder_id to cancel a group reminder")
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        await interaction.followup.send(f"❌ **Error**: {str(e)}")

@tree.command(name="testreminder", description="Test reminder delivery (sends immediately)")
async def test_reminder(interaction: discord.Interaction, message: str = "Test reminder - checking delivery"):
    try:
        await interaction.response.defer()
    except discord.errors.NotFound:
        return

    try:
        # Create a test reminder that triggers immediately
        import uuid
        reminder_id = str(uuid.uuid4())[:8]
        
        # Store minimal reminder data for testing
        reminder_data = {
            'user_id': interaction.user.id,
            'channel_id': interaction.channel.id,
            'message': message,
            'created_at': datetime.now(UTC),
            'duration_seconds': 1,  # 1 second
            'is_group_reminder': False
        }
        
        active_reminders[reminder_id] = reminder_data
        
        # Send confirmation
        embed = discord.Embed(
            title="🧪 Test Reminder",
            description="Testing reminder delivery...",
            color=0xffa500,
            timestamp=datetime.now(UTC)
        )
        
        embed.add_field(
            name="📝 Test Message:",
            value=f"**{message}**",
            inline=False
        )
        
        embed.add_field(
            name="⏱️ Delivery:",
            value="Immediate (1 second)",
            inline=True
        )
        
        embed.add_field(
            name="📍 Channel:",
            value=interaction.channel.mention,
            inline=True
        )
        
        embed.add_field(
            name="🆔 Test ID:",
            value=f"`{reminder_id}`",
            inline=True
        )
        
        embed.set_footer(text="Check console logs for delivery status")
        
        await interaction.followup.send(embed=embed)
        
        # Schedule immediate delivery for testing
        asyncio.create_task(schedule_reminder(reminder_id, 1))
        
        print(f"🧪 Test reminder {reminder_id} scheduled for user {interaction.user.id} in channel {interaction.channel.id}")
        
    except Exception as e:
        await interaction.followup.send(f"❌ **Error creating test reminder**: {str(e)}")
        print(f"❌ Test reminder error: {e}")

@tree.command(name="sync", description="[Admin Only] Manually sync slash commands")
async def sync_commands(interaction: discord.Interaction):
    try:
        await interaction.response.defer()
    except discord.errors.NotFound:
        return

    try:
        # Only allow bot owner or admin to sync
        if not interaction.user.guild_permissions.administrator:
            await interaction.followup.send("❌ You need administrator permissions to use this command.")
            return
            
        synced = await tree.sync()
        await interaction.followup.send(f"✅ Successfully synced {len(synced)} commands!")
        
    except Exception as e:
        await interaction.followup.send(f"❌ Error syncing commands: {str(e)}")

@client.event
async def on_ready():
    try:
        synced = await tree.sync()
        print(f"✅ Bot logged in as {client.user}")
        print(f"🔄 Synced {len(synced)} command(s)")
        
        # List all synced commands
        for cmd in synced:
            print(f"   - /{cmd.name}: {cmd.description}")
            
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

client.run(DISCORD_TOKEN)
