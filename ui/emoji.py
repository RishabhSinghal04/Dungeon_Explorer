EMOJIS: dict[str, str] = {
    "arrow": "\u27a4",
    "battle": "\u2694\ufe0f",
    "coin": "\U0001fa99",
    "cross_mark": "\u274c",
    "explosion": "\U0001f4a5",
    "fire": "\U0001f525",
    "health": "\u2764\ufe0f",
    "herb": "\U0001f33f",
    "skull": "\U0001f480",
    "trophy": "\U0001f3c6",
    "weapon": "\U0001fa93",
    "warning_sign": "\u26a0",
}


def get_emoji(key: str, default: str = "") -> str:
    """Get emoji by key with optional default."""
    return EMOJIS.get(key, default)


def format_with_emoji(text: str, emoji_key: str, position: str = "start") -> str:
    """Format text with emoji at start or end."""
    emoji: str = get_emoji(emoji_key)
    return f"{emoji}  {text}" if position == "start" else f"{text}  {emoji}"
