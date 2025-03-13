# Discord Reaction Roleplay Bot

An interactive Discord bot that creates dynamic, branching story experiences with Google's Gemini 2.0 API. Users participate by voting on story choices with emoji reactions, shaping the narrative in real time.

## Features

- **Dynamic Story Generation**: Uses Google Gemini 2.0 to generate coherent and context-aware plot developments
- **Context-Aware Reaction Options**: Assigns thematic emojis to story choices based on keywords
- **Multiple Message Splitting**: Automatically splits long messages to avoid Discord's character limit
- **Preserving Story History**: Maintains a running log of the story to reference in future AI prompts
- **Vote Tallying & Karma System**: Awards karma points to users who vote for the winning option
- **Secret Roles**: Optionally assigns hidden roles to participants in secret-themed scenarios
- **Error Handling & Fallbacks**: Provides fallback options if the AI's output doesn't conform to expected formats

## Setup

1. **Prerequisites**
   - Python 3.8 or higher
   - Discord Bot Token
   - Google Gemini API Key

2. **Installation**
   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/reaction-story.git
   cd reaction-story

   # Create and activate a virtual environment (recommended)
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configuration**
   - The `.env` file should contain your Discord Bot Token and Gemini API Key:
     ```
     DISCORD_BOT_TOKEN=your_discord_bot_token
     GEMINI_API_KEY=your_gemini_api_key
     ```

4. **Run the Bot**
   ```bash
   python bot.py
   ```

## Usage

### Commands

- **`!roleplay [theme]`**: Start a new roleplay scenario with the specified theme
  Example: `!roleplay space adventure`

- **`!karma [@user]`**: Check karma points for yourself or another user
  Example: `!karma` or `!karma @username`

### Participation

1. Once a roleplay scenario is started, the bot will present an initial scenario with two options
2. Users can vote by clicking on the emoji reactions
3. After 60 seconds, the bot tallies the votes and continues the story based on the winning option
4. This process repeats until no one votes or the scenario naturally concludes

### Secret Roles

- If the roleplay theme includes the word "secret", the command initiator will receive a DM with a secret role
- This adds an extra layer of intrigue and roleplay opportunities

## Notes

- The bot uses the Gemini 1.5 Flash model for optimal performance and speed
- Each story segment is stored in memory, enabling the AI to maintain context
- You can adjust the voting duration in the `bot.py` file by changing the `VOTING_DURATION` variable

## License

This project is licensed under the MIT License - see the LICENSE file for details.
