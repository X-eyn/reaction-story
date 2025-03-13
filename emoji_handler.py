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
    
    # Use default emojis if no matches found
    if not emoji_a:
        emoji_a = DEFAULT_EMOJIS[0]
    if not emoji_b:
        emoji_b = DEFAULT_EMOJIS[1]
        
    return emoji_a, emoji_b

def emoji_to_text(emoji):
    """
    Convert an emoji to a descriptive text based on the EMOJI_KEYWORDS mapping
    
    Args:
        emoji (str): The emoji to convert
        
    Returns:
        str: Descriptive text for the emoji, or None if not found
    """
    # Create reverse mapping from emoji to keyword
    emoji_to_keyword = {v: k for k, v in EMOJI_KEYWORDS.items()}
    
    # Check if emoji exists in our mapping
    if emoji in emoji_to_keyword:
        return emoji_to_keyword[emoji]
    
    # Special handling for some common emojis not in our keyword list
    special_emojis = {
        "🔥": "fire", "💧": "water", "🌍": "earth", "💨": "air",
        "❤️": "love", "💕": "affection", "😂": "laughter", "😊": "happiness",
        "😢": "sadness", "😡": "anger", "😱": "fear", "🤔": "thinking",
        "👍": "approval", "👎": "disapproval", "👏": "applause", "🙏": "prayer",
        "💪": "strength", "🧠": "intelligence", "👁️": "vision", "👂": "hearing",
        "💰": "wealth", "⚡": "energy", "🎭": "deception", "🎯": "accuracy",
        "🎮": "game", "🎵": "music", "🎬": "movie", "📚": "knowledge",
        "🕰️": "time", "🧩": "puzzle", "🧪": "experiment", "🪄": "magic",
        "🦸": "hero", "🧟": "zombie", "👽": "alien", "🤖": "robot",
        "🐺": "wolf", "🦊": "fox", "🐉": "dragon", "🦁": "lion"
    }
    
    if emoji in special_emojis:
        return special_emojis[emoji]
    
    # Try to match emoji partially (for emoji variations)
    for known_emoji, keyword in emoji_to_keyword.items():
        if emoji in known_emoji or known_emoji in emoji:
            return keyword
            
    # Default fallback values for emojis we can't identify
    emoji_categories = {
        "😀": "emotion", "🐶": "animal", "🍎": "food", "🏠": "place",
        "🚗": "vehicle", "👕": "clothing", "💻": "technology", "🎮": "entertainment",
        "🏆": "achievement", "🌈": "phenomenon", "🔮": "mystical object"
    }
    
    # Try to match by first character to identify category
    if emoji and len(emoji) > 0:
        first_char = emoji[0]
        for category_emoji, category in emoji_categories.items():
            if first_char == category_emoji[0]:
                return category
    
    # If we can't identify the emoji, return None so it can be skipped
    return None
