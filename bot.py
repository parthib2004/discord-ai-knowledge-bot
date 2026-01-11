import discord
from discord import app_commands
import google.genai as genai
import os
from dotenv import load_dotenv
from prompts import build_prompt
from language_support import detect_language, create_multilingual_prompt, get_language_flag

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini with the new API
client_genai = genai.Client(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

def load_knowledge():
    with open("knowledge_base.txt", "r", encoding="utf-8") as f:
        return f.read()

@tree.command(name="ask", description="Ask company-related questions in any language")
async def ask(interaction: discord.Interaction, question: str):
    try:
        await interaction.response.defer()
    except discord.errors.NotFound:
        # Interaction already expired, can't respond
        return

    try:
        # Detect the language of the question
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

@client.event
async def on_ready():
    await tree.sync()
    print(f"✅ Bot logged in as {client.user}")

client.run(DISCORD_TOKEN)