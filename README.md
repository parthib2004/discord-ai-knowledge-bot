# Discord AI Knowledge Bot

A Discord bot that answers company-related questions using Google's Gemini AI and a custom knowledge base.

## Features

- 🤖 AI-powered responses using Google Gemini
- 🌍 **Multi-language support** - Ask in any language, get responses in the same language
- 📚 Custom knowledge base integration
- ⚡ Fast slash command interface
- 🔒 Secure environment variable configuration
- 🎯 Automatic language detection (70+ languages supported)

## Setup

### Prerequisites
- Python 3.12+
- Discord Bot Token
- Google Gemini API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd discord-ai-knowledge-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your tokens:
   ```
   DISCORD_TOKEN=your_discord_token_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Update knowledge base**
   Edit `knowledge_base.txt` with your company information

5. **Run the bot**
   ```bash
   python bot.py
   ```

## Getting API Keys

### Discord Bot Token
1. Go to https://discord.com/developers/applications
2. Create a new application
3. Go to "Bot" section
4. Copy the token

### Gemini API Key
1. Go to https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Create API Key
4. Copy the key

## Deployment

This bot is ready for deployment on platforms like Railway, Render, or Heroku.

### Railway Deployment
1. Push code to GitHub
2. Connect Railway to your GitHub repo
3. Add environment variables in Railway dashboard
4. Deploy!

## Usage

### Basic Commands
Use the `/ask` command in Discord:
```
/ask What are the company office hours?
```

### Multi-Language Support 🌍
Ask questions in **any language** and get responses in the same language:

```
/ask ¿Cuáles son las horas de oficina?          (Spanish)
/ask Quelles sont les heures de bureau?        (French) 
/ask Wie sind die Bürozeiten?                  (German)
/ask オフィスの営業時間は何時ですか？                (Japanese)
/ask Каковы часы работы офиса?                  (Russian)
```

### View Supported Languages
```
/languages
```
Shows all 70+ supported languages with flags and codes.

## Files

- `bot.py` - Main bot code
- `prompts.py` - AI prompt templates
- `knowledge_base.txt` - Company knowledge base
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template