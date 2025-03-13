import discord
import asyncio
import json
import os
import re
from dotenv import load_dotenv
from discord.ext import commands
from gemini_api import generate_text
from emoji_handler import get_relevant_emojis
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
        "Follow these formatting rules:\n"
        "1. Use rich, descriptive language with proper paragraph breaks for readability\n"
        "2. Create atmosphere through sensory details and environmental descriptions\n"
        "3. Use occasional bold or italic text for emphasis on important elements\n"
        "4. End with exactly two distinct choices labeled as:\n\n"
        "**A)** [first option] - Make this option distinct and meaningful\n"
        "**B)** [second option] - Make this option clearly different from option A\n\n"
        "Ensure the options present a meaningful choice with different possible outcomes."
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
    
    if reaction_a:
        async for user in reaction_a.users():
            if user != bot.user:
                voters_a.append(user)
    
    if reaction_b:
        async for user in reaction_b.users():
            if user != bot.user:
                voters_b.append(user)
    
    # Determine winning option
    if len(voters_a) + len(voters_b) == 0:
        await ctx.send("No one voted. The story ends here...")
        if channel_id in story_history:
            del story_history[channel_id]
        return
    
    if len(voters_a) > len(voters_b):
        winning_option = f"**A)** {option_a}"
        winning_emoji = emoji_a
        winning_voters = voters_a
    else:
        winning_option = f"**B)** {option_b}"
        winning_emoji = emoji_b
        winning_voters = voters_b
    
    # Award karma to users who voted for the winning option
    for user in winning_voters:
        user_id = str(user.id)
        karma[user_id] = karma.get(user_id, 0) + 1
    
    # Add chosen option to history
    if channel_id in story_history and story_history[channel_id]:
        story_history[channel_id][-1]["chosen_option"] = winning_option
    
    # Create full story context for AI
    full_context = ""
    for segment in story_history[channel_id]:
        full_context += segment["narrative"] + "\n\n"
        if segment["chosen_option"]:
            full_context += f"**The group chose: {segment['chosen_option']}**\n\n"
    
    # Generate next part of the story with improved formatting instructions
    prompt = (
        f"{full_context}\n\n"
        "Continue the story based on the chosen option, following these formatting rules:\n"
        "1. Use rich, descriptive language with proper paragraph breaks for readability\n"
        "2. Build on previous events with dramatic tension and atmosphere\n"
        "3. Use occasional bold or italic text for emphasis on important elements\n"
        "4. End with exactly two distinct choices labeled as:\n\n"
        "**A)** [first option] - Make this option distinct and meaningful\n"
        "**B)** [second option] - Make this option clearly different from option A\n\n"
        "Ensure the options present a meaningful choice with different possible outcomes."
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
