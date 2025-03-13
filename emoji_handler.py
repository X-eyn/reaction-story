import re

# Dictionary mapping keywords to appropriate emojis
EMOJI_KEYWORDS = {
    # Elements & Nature
    "fire": "🔥", "water": "💧", "earth": "🌍", "air": "💨", 
    "forest": "🌳", "tree": "🌲", "mountain": "⛰️", "river": "🏞️",
    "ocean": "🌊", "sea": "🐚", "beach": "🏖️", "sun": "☀️", 
    "moon": "🌙", "star": "⭐", "sky": "🌌", "cloud": "☁️", 
    "rain": "🌧️", "snow": "❄️", "lightning": "⚡", "thunder": "⛈️",
    
    # Movement & Action
    "run": "🏃", "walk": "🚶", "jump": "⬆️", "climb": "🧗", 
    "swim": "🏊", "fly": "✈️", "hide": "🙈", "fight": "👊",
    "attack": "⚔️", "defend": "🛡️", "escape": "🚪", "retreat": "↩️",
    "shoot": "🔫", "throw": "🤾", "catch": "🧤", "build": "🔨",
    
    # Directions & Navigation
    "left": "⬅️", "right": "➡️", "up": "⬆️", "down": "⬇️",
    "forward": "⏩", "backward": "⏪", "north": "⬆️", "south": "⬇️",
    "east": "➡️", "west": "⬅️", "map": "🗺️", "compass": "🧭",
    
    # Objects & Tools
    "key": "🔑", "lock": "🔒", "door": "🚪", "light": "💡", 
    "book": "📚", "scroll": "📜", "potion": "🧪", "bag": "👝",
    "gold": "💰", "money": "💵", "treasure": "💎", "sword": "🗡️",
    "weapon": "🔪", "bow": "🏹", "shield": "🛡️", "armor": "🦺",
    "wand": "🪄", "staff": "🪄", "orb": "🔮", "crystal": "💎",
    
    # Creatures & Characters
    "monster": "👹", "dragon": "🐉", "ghost": "👻", "alien": "👽",
    "robot": "🤖", "pirate": "🏴‍☠️", "knight": "🛡️", "wizard": "🧙‍♂️",
    "warrior": "⚔️", "beast": "🐺", "demon": "😈", "angel": "😇",
    "king": "👑", "queen": "👸", "prince": "🤴", "princess": "👸",
    
    # Emotions & States
    "happy": "😄", "sad": "😢", "angry": "😠", "scared": "😱",
    "calm": "😌", "confused": "😕", "love": "❤️", "hate": "💔",
    "sleep": "😴", "awake": "👁️", "sick": "🤒", "heal": "💊",
    "alive": "💓", "dead": "💀", "poison": "☠️", "curse": "🧿",
    
    # Settings & Locations
    "castle": "🏰", "village": "🏘️", "city": "🏙️", "house": "🏠",
    "cave": "🕳️", "dungeon": "🔐", "temple": "🏛️", "tower": "🗼",
    "ship": "🚢", "boat": "⛵", "plane": "✈️", "space": "🚀",
    "island": "🏝️", "volcano": "🌋", "desert": "🏜️", "jungle": "🌴",
    
    # Time & Weather
    "day": "🌞", "night": "🌃", "dawn": "🌅", "dusk": "🌇",
    "time": "⏰", "hour": "🕓", "minute": "⏱️", "second": "⏲️",
    "season": "🍂", "spring": "🌱", "summer": "☀️", "autumn": "🍁",
    "winter": "❄️", "storm": "🌩️", "fog": "🌫️", "wind": "🌬️",
    
    # Communication & Magic
    "talk": "💬", "speak": "🗣️", "listen": "👂", "whisper": "🤫",
    "shout": "📢", "spell": "✨", "magic": "🔮", "enchant": "🪄",
    "curse": "👿", "bless": "🙏", "ritual": "📿", "summon": "🧿",
    
    # Miscellaneous
    "wait": "⏳", "hurry": "⚡", "secret": "🤫", "open": "📭",
    "search": "🔍", "find": "🔎", "steal": "🥷", "give": "🎁",
    "yes": "✅", "no": "❌", "maybe": "❓", "help": "🆘",
    "danger": "⚠️", "safe": "🔒", "trap": "⚠️", "trick": "🎭"
}

# Default emojis if no keywords match
DEFAULT_EMOJIS = ["🅰️", "🅱️"]

def get_relevant_emojis(option_a, option_b):
    """
    Get relevant emojis for the two options based on keywords
    
    Args:
        option_a (str): The text for option A
        option_b (str): The text for option B
        
    Returns:
        tuple: Two emojis (emoji_a, emoji_b) for the options
    """
    emoji_a = None
    emoji_b = None
    
    # Process option A - check entire option text first
    option_a_lower = option_a.lower()
    for keyword, emoji in EMOJI_KEYWORDS.items():
        if keyword in option_a_lower and not emoji_a:
            emoji_a = EMOJI_KEYWORDS[keyword]
            break
    
    # If no match found, try with individual words
    if not emoji_a:
        words_a = re.findall(r'\b\w+\b', option_a_lower)
        for word in words_a:
            if word in EMOJI_KEYWORDS and not emoji_a:
                emoji_a = EMOJI_KEYWORDS[word]
                break
    
    # Process option B - check entire option text first
    option_b_lower = option_b.lower()
    for keyword, emoji in EMOJI_KEYWORDS.items():
        if keyword in option_b_lower and not emoji_b:
            emoji_b = EMOJI_KEYWORDS[keyword]
            break
    
    # If no match found, try with individual words
    if not emoji_b:
        words_b = re.findall(r'\b\w+\b', option_b_lower)
        for word in words_b:
            if word in EMOJI_KEYWORDS and not emoji_b:
                emoji_b = EMOJI_KEYWORDS[word]
                break
    
    # If we couldn't find relevant emojis or both options have the same emoji
    if not emoji_a or not emoji_b or emoji_a == emoji_b:
        # Try to fallback to more contextual emojis
        if "axe" in option_a_lower or "weapon" in option_a_lower:
            emoji_a = "🪓"
        elif "grab" in option_a_lower or "take" in option_a_lower:
            emoji_a = "👊"
        elif "door" in option_a_lower:
            emoji_a = "🚪"
        elif "window" in option_a_lower:
            emoji_a = "🪟"
        
        if "cable" in option_b_lower or "wire" in option_b_lower:
            emoji_b = "⚡"
        elif "door" in option_b_lower:
            emoji_b = "🚪"
        elif "barricade" in option_b_lower or "block" in option_b_lower:
            emoji_b = "🛑"
    
    # If we still have duplicates or missing emojis, use default
    if not emoji_a or not emoji_b or emoji_a == emoji_b:
        return DEFAULT_EMOJIS
    
    return emoji_a, emoji_b
