# Discord Reaction Roleplay Bot

An interactive Discord bot that creates dynamic, branching story experiences with Google's Gemini 2.0 API. Users participate by voting on story choices with emoji reactions, shaping the narrative in real time.

## Features

### Core Functionality
- **Dynamic Storytelling**: Generates immersive, context-aware story scenarios using Google's Gemini 2.0 API
- **Branching Narratives**: Every decision shapes the flow of the story, creating unique adventures each time
- **Emoji Voting System**: Users vote with emoji reactions to determine the path of the story
- **Karma Tracking**: Users who vote for winning options earn karma points, encouraging participation

### Enhanced Features
- **Professional Formatting**: Stories are formatted with rich, descriptive language, proper paragraph breaks, and bold/italic text for emphasis
- **Custom Emoji Influence**: Users can add custom emoji reactions to influence elements in the next part of the story
  - Example: Adding a 🔥 emoji will incorporate fire elements into the next segment
  - Multiple users adding the same emoji increases its importance in the story
- **Secret Roles**: Add "secret" to your roleplay theme to receive a private DM with a secret role that only you know
- **Voting Duration**: The bot waits for a set time period to collect votes before moving the story forward

## Commands

- `!roleplay [theme]` - Start a new roleplay adventure with the specified theme
  - Example: `!roleplay space adventure` or `!roleplay zombie apocalypse secret`
  
- `!karma [@user]` - Check karma points for yourself or another user
  - Example: `!karma` or `!karma @username`

## Setup

1. Clone the repository
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Discord bot token and Gemini API key:
   ```
   DISCORD_BOT_TOKEN=your_discord_bot_token
   GEMINI_API_KEY=your_gemini_api_key
   ```
4. Run the bot:
   ```
   python bot.py
   ```

## User Interaction Guide

1. **Start a Story**: Use the `!roleplay` command with a theme of your choice
2. **Vote on Options**: React with the emoji corresponding to option A or option B
3. **Add Story Elements**: React with custom emojis to influence the next part of the story
4. **Continue the Adventure**: Each segment will present new choices, creating an ongoing narrative

## Requirements
- Python 3.8+
- Discord.py 2.0.0+
- Google Generative AI SDK
- A Discord bot token
- Google Gemini API key

## Notes

- The bot uses the Gemini 1.5 Flash model for optimal performance and speed
- Each story segment is stored in memory, enabling the AI to maintain context
- You can adjust the voting duration in the `bot.py` file by changing the `VOTING_DURATION` variable

## License

This project is licensed under the MIT License - see the LICENSE file for details.
