from typing import Optional

from core.interfaces import IPlayer, IOutputHandler, IWeapon

from ui.emoji import EmojiType, format_with_emoji


def show_player_status(player: IPlayer, output_handler: IOutputHandler) -> None:
    output_handler.display("\n" + build_player_status(player))


def build_player_status(player: IPlayer) -> str:
    weapon: Optional[IWeapon] = player.get_equipped_weapon()
    weapon_part: str = (
        weapon.display_name() if weapon else format_with_emoji("", EmojiType.CROSS_MARK)
    )

    health_points: int = player.health_points
    max_health: int = player.max_health_points

    health_emoji: EmojiType = (
        EmojiType.GREEN_HEART
        if max_health // 2 < health_points
        else EmojiType.ORANGE_HEART
    )
    status_parts: list[str] = [
        f"{player.name}: ",
        format_with_emoji(f"Weapon Equipped: {weapon_part} | ", EmojiType.WEAPON),
        format_with_emoji(f"Health Points: {health_points} | ", health_emoji),
        format_with_emoji(f"Cash: {player.cash.get_balance()}", EmojiType.COIN),
    ]

    return "".join(status_parts)
