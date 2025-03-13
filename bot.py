import discord
import asyncio
import json
import os
import re
from dotenv import load_dotenv
from discord.ext import commands
from gemini_api import generate_text
from emoji_handler import get_relevant_emojis, emoji_to_text
from message_handler import split_message

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Set up intents for reactions
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

# Initialize bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Karma tracking dictionary
karma = {}

# Story history for active channels
story_history = {}

# Voting duration in seconds
VOTING_DURATION = 60

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='roleplay')
async def roleplay(ctx, *, theme=None):
    """Start a new roleplay scenario with the specified theme"""
    if not theme:
        await ctx.send("Please provide a theme for the roleplay. Example: `!roleplay space adventure`")
        return
    
    # Initialize story history for this channel
    channel_id = str(ctx.channel.id)
    story_history[channel_id] = []
    
    # Generate initial scenario with improved formatting instructions
    prompt = (
        "You are an expert storyteller creating an immersive, dramatic roleplay scenario. "
        f"Generate an engaging opening scenario for a roleplay about: {theme}.\n\n"
        "Follow these formatting and narrative guidelines:\n"
        "1. **Scene Setting**: Begin with *italic text* for atmospheric descriptions that engage the senses. "
        "Describe the environment, time of day, and initial mood.\n"
        "2. **Character Introduction**: Use **bold text** for character names when first introduced.\n"
        "3. **Narrative Structure**: Build tension gradually using proper paragraph breaks for pacing.\n"
        "4. **Dialogue**: Format dialogue with quotation marks and include emotional cues, e.g., \"*I won't go in there,*\" he whispered, voice trembling.\n"
        "5. **Important Objects/Clues**: When introducing key items or information, use *italic emphasis*.\n"
        "6. **Action Sequences**: Use short, punchy sentences for action. Create intensity with pacing.\n"
        "7. **End Choices**: Conclude with two distinct, meaningful choices formatted as:\n\n"
        "**A)** [first option] - Make this option distinct and consequential\n"
        "**B)** [second option] - Make this option clearly different with its own potential outcomes\n\n"
        "Ensure your storytelling creates a sense of immersion, urgency, and emotional investment."
    )
    
    try:
        initial_response = await generate_text(prompt)
        
        # Check if response has the expected format with bold markdown
        option_pattern = r'\*\*A\)\*\*(.*?)(?:\n|$).*?\*\*B\)\*\*(.*?)(?:\n|$)'
        options_match = re.search(option_pattern, initial_response, re.DOTALL)
        
        if options_match:
            option_a = options_match.group(1).strip()
            option_b = options_match.group(2).strip()
        else:
            # Try alternate pattern without bold formatting
            alt_pattern = r'A\)(.*?)(?:\n|$).*?B\)(.*?)(?:\n|$)'
            alt_match = re.search(alt_pattern, initial_response, re.DOTALL)
            
            if alt_match:
                option_a = alt_match.group(1).strip()
                option_b = alt_match.group(2).strip()
                
                # Add proper formatting if the AI didn't use it
                narrative_parts = initial_response.split('A)')
                if len(narrative_parts) > 1:
                    narrative = narrative_parts[0].strip()
                    options_part = 'A)' + narrative_parts[1]
                    formatted_options = options_part.replace('A)', '**A)**').replace('B)', '**B)**')
                    initial_response = f"{narrative}\n\n{formatted_options}"
            else:
                # Fallback if AI didn't format options correctly
                split_text = initial_response.split('\n\n')
                narrative = '\n\n'.join(split_text[:-1]) if len(split_text) > 1 else initial_response
                option_a = "Continue cautiously"
                option_b = "Take a risk"
                initial_response = f"{narrative}\n\n**A)** {option_a}\n**B)** {option_b}"
        
        # If theme includes "secret", assign secret role to command invoker
        if "secret" in theme.lower():
            secret_roles = ["Traitor", "Spy", "Double Agent", "Saboteur", "Impostor"]
            import random
            secret_role = random.choice(secret_roles)
            try:
                await ctx.author.send(f"Your secret role in this scenario: **{secret_role}**.\nOnly you know this!")
            except discord.Forbidden:
                pass  # User has DMs closed
        
        # Add initial scenario to history
        story_history[channel_id].append({"narrative": initial_response, "chosen_option": None})
        
        # Split long messages if needed
        messages = split_message(initial_response)
        sent_messages = []
        for message in messages:
            sent_message = await ctx.send(message)
            sent_messages.append(sent_message)
        
        # Add reactions based on the options
        last_message = sent_messages[-1]
        emoji_a, emoji_b = get_relevant_emojis(option_a, option_b)
        await last_message.add_reaction(emoji_a)
        await last_message.add_reaction(emoji_b)
        
        # Wait for votes
        await asyncio.sleep(VOTING_DURATION)
        
        # Continue the story with voting
        await continue_story(ctx, last_message, emoji_a, emoji_b, option_a, option_b)
        
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

async def continue_story(ctx, message, emoji_a, emoji_b, option_a, option_b):
    """Process votes and continue the story"""
    channel_id = str(ctx.channel.id)
    
    # Refresh message to get latest reactions
    message = await ctx.channel.fetch_message(message.id)
    
    # Count votes
    reaction_a = discord.utils.get(message.reactions, emoji=emoji_a)
    reaction_b = discord.utils.get(message.reactions, emoji=emoji_b)
    
    voters_a = []
    voters_b = []
    
    # Track custom emoji reactions from users
    custom_reactions = {}
    
    # Process all reactions on the message
    for reaction in message.reactions:
        # Skip the bot's own A/B option reactions
        if str(reaction.emoji) == str(emoji_a) or str(reaction.emoji) == str(emoji_b):
            if reaction.emoji == emoji_a:
                async for user in reaction.users():
                    if user != bot.user:
                        voters_a.append(user)
            elif reaction.emoji == emoji_b:
                async for user in reaction.users():
                    if user != bot.user:
                        voters_b.append(user)
        # Process custom user reactions
        else:
            users_for_emoji = []
            async for user in reaction.users():
                if user != bot.user:
                    users_for_emoji.append(user)
            
            if users_for_emoji:  # Only add emojis that users actually reacted with
                custom_reactions[str(reaction.emoji)] = users_for_emoji
    
    # Check if there are any votes or custom reactions
    total_interactions = len(voters_a) + len(voters_b) + sum(len(users) for users in custom_reactions.values())
    
    # End story only if there are no interactions at all
    if total_interactions == 0:
        await ctx.send("No one interacted with the story. The story ends here...")
        if channel_id in story_history:
            del story_history[channel_id]
        return
    
    # Determine winning option (if no votes for A or B, generate a neutral continuation)
    if len(voters_a) + len(voters_b) == 0:
        # No votes for main options, but custom reactions exist
        winning_option = "Neither option was chosen, but the story continues..."
        winning_emoji = "🔄"
        winning_voters = []
        
        # For story continuity, choose a random option
        import random
        if random.choice([True, False]):
            chosen_option = f"**A)** {option_a}"
        else:
            chosen_option = f"**B)** {option_b}"
    elif len(voters_a) > len(voters_b):
        winning_option = f"**A)** {option_a}"
        winning_emoji = emoji_a
        winning_voters = voters_a
        chosen_option = winning_option
    else:
        winning_option = f"**B)** {option_b}"
        winning_emoji = emoji_b
        winning_voters = voters_b
        chosen_option = winning_option
    
    # Award karma to users who voted for the winning option
    for user in winning_voters:
        user_id = str(user.id)
        karma[user_id] = karma.get(user_id, 0) + 1
    
    # Add chosen option to history
    if channel_id in story_history and story_history[channel_id]:
        story_history[channel_id][-1]["chosen_option"] = chosen_option
    
    # Create full story context for AI
    full_context = ""
    for segment in story_history[channel_id]:
        full_context += segment["narrative"] + "\n\n"
        if segment["chosen_option"]:
            full_context += f"**The group chose: {segment['chosen_option']}**\n\n"
    
    # Prepare custom elements text from user reactions
    custom_elements_text = ""
    if custom_reactions:
        custom_elements = []
        for emoji, users in custom_reactions.items():
            emoji_desc = emoji_to_text(emoji)
            if emoji_desc:
                custom_elements.append(f"{emoji_desc} (added by {len(users)} {'user' if len(users) == 1 else 'users'})")
        
        if custom_elements:
            custom_elements_text = "Additionally, incorporate these elements into the next part of the story in a meaningful way: " + ", ".join(custom_elements) + "."
    
    # Generate next part of the story with improved formatting instructions
    prompt = (
        f"{full_context}\n\n"
        "Continue the story based on the chosen option, following these advanced formatting guidelines:\n"
        "1. **Transition**: Begin with a brief *italic* summary connecting to the previous choice.\n"
        "2. **Consequences**: Detail the immediate effects of the choice using vivid sensory descriptions.\n"
        "3. **Character Development**: Use **bold** for character names and show emotional/physical reactions to events.\n"
        "4. **Dramatic Moments**: Emphasize key revelations or shocking moments with *italic* or **bold** formatting.\n"
        "5. **Environmental Changes**: Describe how the setting evolves or responds to the characters' actions.\n"
        "6. **Dialogue**: Format dialogue with quotation marks, including tone indicators, e.g., \"*We need to hurry,*\" she urged.\n"
        "7. **Pacing**: Vary paragraph length – short for tension, longer for description and reflection.\n"
    )
    
    # Add custom elements if any
    if custom_elements_text:
        prompt += f"\n8. **Special Elements**: {custom_elements_text}\n"
    
    prompt += (
        "\nEnd with exactly two distinct choices labeled as:\n\n"
        "**A)** [first option] - Make this option carry significant weight and consequences\n"
        "**B)** [second option] - Make this option provide a completely different direction\n\n"
        "Ensure each choice creates a meaningful branch in the narrative and maintains emotional investment."
    )

    try:
        next_segment = await generate_text(prompt)
        
        # Check if response has the expected format with bold markdown
        option_pattern = r'\*\*A\)\*\*(.*?)(?:\n|$).*?\*\*B\)\*\*(.*?)(?:\n|$)'
        options_match = re.search(option_pattern, next_segment, re.DOTALL)
        
        if options_match:
            new_option_a = options_match.group(1).strip()
            new_option_b = options_match.group(2).strip()
        else:
            # Try alternate pattern without bold formatting
            alt_pattern = r'A\)(.*?)(?:\n|$).*?B\)(.*?)(?:\n|$)'
            alt_match = re.search(alt_pattern, next_segment, re.DOTALL)
            
            if alt_match:
                new_option_a = alt_match.group(1).strip()
                new_option_b = alt_match.group(2).strip()
                
                # Add proper formatting if the AI didn't use it
                narrative_parts = next_segment.split('A)')
                if len(narrative_parts) > 1:
                    narrative = narrative_parts[0].strip()
                    options_part = 'A)' + narrative_parts[1]
                    formatted_options = options_part.replace('A)', '**A)**').replace('B)', '**B)**')
                    next_segment = f"{narrative}\n\n{formatted_options}"
            else:
                # Fallback if AI didn't format options correctly
                split_text = next_segment.split('\n\n')
                narrative = '\n\n'.join(split_text[:-1]) if len(split_text) > 1 else next_segment
                new_option_a = "Continue cautiously"
                new_option_b = "Take a risk"
                next_segment = f"{narrative}\n\n**A)** {new_option_a}\n**B)** {new_option_b}"
        
        # Add to story history
        story_history[channel_id].append({"narrative": next_segment, "chosen_option": None})
        
        # Let users know which option won
        await ctx.send(f"Option {winning_emoji} won with {len(winning_voters)} votes!\n**{winning_option}**")
        
        # If there were custom reactions, acknowledge them
        if custom_reactions:
            custom_elements = [emoji_to_text(emoji) for emoji in custom_reactions.keys() if emoji_to_text(emoji)]
            if custom_elements:
                elements_text = ", ".join(custom_elements)
                await ctx.send(f"*The story will also incorporate: {elements_text}*")
        
        # Split and send the new story segment
        messages = split_message(next_segment)
        sent_messages = []
        for message in messages:
            sent_message = await ctx.send(message)
            sent_messages.append(sent_message)
        
        # Add reactions to the last message with NEW emojis based on the NEW options
        last_message = sent_messages[-1]
        new_emoji_a, new_emoji_b = get_relevant_emojis(new_option_a, new_option_b)
        await last_message.add_reaction(new_emoji_a)
        await last_message.add_reaction(new_emoji_b)
        
        # Wait for votes and continue the story with the NEW options and NEW emojis
        await asyncio.sleep(VOTING_DURATION)
        await continue_story(ctx, last_message, new_emoji_a, new_emoji_b, new_option_a, new_option_b)
        
    except Exception as e:
        await ctx.send(f"An error occurred while continuing the story: {str(e)}")
        if channel_id in story_history:
            del story_history[channel_id]

@bot.command(name='karma')
async def check_karma(ctx, member: discord.Member = None):
    """Check karma points for yourself or another user"""
    target = member or ctx.author
    user_id = str(target.id)
    points = karma.get(user_id, 0)
    
    await ctx.send(f"{target.display_name} has {points} karma points.")

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)
