import discord
from discord import app_commands
import google.genai as genai
import os
from dotenv import load_dotenv
from prompts import build_prompt

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

@tree.command(name="ask", description="Ask company-related questions")
async def ask(interaction: discord.Interaction, question: str):
    try:
        await interaction.response.defer()
    except discord.errors.NotFound:
        # Interaction already expired, can't respond
        return

    try:
        knowledge = load_knowledge()
        prompt = build_prompt(question, knowledge)

        # Use the correct model name from the available models
        response = client_genai.models.generate_content(
            model='gemini-2.5-flash',
            contents=[{'parts': [{'text': prompt}]}]
        )
        
        answer = response.candidates[0].content.parts[0].text
        
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

@client.event
async def on_ready():
    await tree.sync()
    print(f"✅ Bot logged in as {client.user}")

client.run(DISCORD_TOKEN)