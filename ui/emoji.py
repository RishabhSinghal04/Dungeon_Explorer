from enum import Enum


class EmojiType(Enum):
    """Available emoji types."""

    ARROW = "arrow"
    BATTLE = "battle"
    COIN = "coin"
    CROSS_MARK = "cross_mark"
    EXPLOSION = "explosion"
    FIRE = "fire"
    GREEN_HEART = "green_heart"
    ORANGE_HEART = "orange_heart"
    GREEN_TICK = "green_tick"
    HERB = "herb"
    SKULL = "skull"
    TROPHY = "trophy"
    WEAPON = "weapon"


EMOJI_MAP: dict[str, str] = {
    EmojiType.ARROW.value: "\u27a4",
    EmojiType.BATTLE.value: "\u2694\ufe0f",
    EmojiType.COIN.value: "\U0001fa99",
    EmojiType.CROSS_MARK.value: "\u274c",
    EmojiType.EXPLOSION.value: "\U0001f4a5",
    EmojiType.FIRE.value: "\U0001f525",
    EmojiType.GREEN_TICK.value: "\U00002705",
    EmojiType.GREEN_HEART.value: "\U0001f49a",
    EmojiType.ORANGE_HEART.value: "\U0001f9e1",
    EmojiType.HERB.value: "\U0001f33f",
    EmojiType.SKULL.value: "\U0001f480",
    EmojiType.TROPHY.value: "\U0001f3c6",
    EmojiType.WEAPON.value: "\U0001fa93",
}


def get_emoji(emoji_type: EmojiType, default: str = "") -> str:
    """Get emoji with optional default."""
    return EMOJI_MAP.get(emoji_type.value, default)


def format_with_emoji(text: str, emoji_type: EmojiType, position: str = "start") -> str:
    """Format text with emoji at start or end."""
    emoji: str = get_emoji(emoji_type)
    if not emoji:
        return text
    return f"{emoji} {text}" if position == "start" else f"{text} {emoji}"
