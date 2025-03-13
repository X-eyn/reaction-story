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
    Convert an emoji to a descriptive text that can be used in the story generation.
    Uses a combination of predefined mappings and Unicode character analysis.
    
    Args:
        emoji (str): The emoji to convert
        
    Returns:
        str: Descriptive text for the emoji, or None if not found
    """
    # Create reverse mapping from emoji to keyword (use existing predefined keywords)
    emoji_to_keyword = {v: k for k, v in EMOJI_KEYWORDS.items()}
    
    # Check if emoji exists in our mapping
    if emoji in emoji_to_keyword:
        return emoji_to_keyword[emoji]
    
    # Handle Discord custom emojis (format: <:name:id>)
    custom_emoji_match = re.match(r'<:(.+):\d+>', emoji)
    if custom_emoji_match:
        # Extract the name of the custom emoji, replace underscores with spaces
        return custom_emoji_match.group(1).replace('_', ' ')
    
    # Try unicode emoji description approach - get the Unicode name which usually has descriptive text
    try:
        import unicodedata
        
        # Split the emoji (might be multiple Unicode characters)
        for char in emoji:
            try:
                # Get the Unicode name - often descriptive
                name = unicodedata.name(char).lower()
                
                # Clean up the name - remove 'emoji' suffix and convert to a simple description
                if "emoji" in name:
                    name = name.replace("emoji", "").strip()
                
                # Replace underscores and dashes with spaces
                name = name.replace("_", " ").replace("-", " ")
                
                # If it's a "face" emoji, simplify
                if "face" in name:
                    emotion_words = ["happy", "sad", "angry", "surprised", 
                                    "scared", "laughing", "crying", "winking",
                                    "thinking", "confused", "tired", "sleeping",
                                    "cool", "nerdy", "sick", "injured", "dead",
                                    "shocked", "crazy", "silly", "love", "kiss"]
                    
                    for emotion in emotion_words:
                        if emotion in name:
                            return emotion
                
                # Remove common prefixes from Unicode names
                prefixes_to_remove = ["face with", "face", "person", "building", "house", "flag"]
                for prefix in prefixes_to_remove:
                    if name.startswith(prefix):
                        name = name[len(prefix):].strip()
                
                # Special handling for letter/symbol emojis (like 🅰️, 🅱️, etc.)
                if "letter" in name or "symbol" in name:
                    continue
                
                # If we found a valid description, return it
                if name and len(name) > 1:
                    return name.strip()
                
            except (ValueError, TypeError):
                continue
    except ImportError:
        pass
    
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
        "🐺": "wolf", "🦊": "fox", "🐉": "dragon", "🦁": "lion",
        "🌟": "star", "🌈": "rainbow", "🌊": "wave", "🌪️": "tornado",
        "🏰": "castle", "⚔️": "sword", "🛡️": "shield", "🧙": "wizard",
        "🔮": "crystal ball", "📜": "scroll", "🧪": "potion", "💎": "gem",
        "🔫": "gun", "💣": "bomb", "🧨": "dynamite", "🪓": "axe",
        "🏹": "bow", "🗡️": "dagger", "🪄": "wand", "🧬": "dna",
        "👑": "crown", "👸": "princess", "🤴": "prince", "👻": "ghost",
        "💀": "skull", "☠️": "death", "👹": "monster", "👺": "goblin",
        "🧙‍♂️": "wizard", "🧙‍♀️": "witch", "🧚": "fairy", "🧜": "mermaid",
        "🐲": "dragon", "🦄": "unicorn", "🦇": "bat", "🦂": "scorpion"
    }
    
    if emoji in special_emojis:
        return special_emojis[emoji]
    
    # Try to match emoji partially (for emoji variations)
    for known_emoji, keyword in emoji_to_keyword.items():
        if emoji in known_emoji or known_emoji in emoji:
            return keyword
    
    # Generic emoji category detection
    emoji_categories = {
        "😀": "emotion", "🐶": "animal", "🍎": "food", "🏠": "place",
        "🚗": "vehicle", "👕": "clothing", "💻": "technology", "🎮": "entertainment",
        "🏆": "achievement", "🌈": "phenomenon", "🔮": "mystical object",
        "🌿": "plant", "🌋": "natural disaster", "🏛️": "building", "🎭": "performance",
        "⚽": "sport", "🔧": "tool", "🎁": "gift", "💍": "jewelry", "🎨": "art"
    }
    
    # Try to match by first character to identify category
    if emoji and len(emoji) > 0:
        first_char = emoji[0]
        for category_emoji, category in emoji_categories.items():
            if first_char == category_emoji[0]:
                return category
    
    # Last resort - if it's a single character, just use a simple description
    if len(emoji) == 1:
        try:
            # Use the most basic category or just "symbol" as fallback
            return "mysterious symbol"
        except:
            pass
    
    # If nothing else works, at least make an attempt with a generic description
    return "mysterious element"
