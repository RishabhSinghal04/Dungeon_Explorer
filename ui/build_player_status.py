from typing import Optional

from characters import Player
from core.interfaces import IWeapon
from ui.emoji import EMOJIS


def build_player_status(player: Player) -> str:
    weapon: Optional[IWeapon] = player.get_equipped_weapon()
    weapon_name: str = weapon.name if weapon else "No"
    return (
        f"{player.name}: {EMOJIS.get("weapon", None)}  Weapon Equipped: {weapon_name}"
        f" | {EMOJIS.get("health", None)}  Health Points: {player.get_health_points()}"
        f" | {EMOJIS.get("coin", None)}  Cash: {player.cash.get_balance()}"
    )
