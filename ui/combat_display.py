from core.interfaces import IOutputHandler
from core.interfaces import IPlayer

from ui.show_player_status import show_player_status
from ui.emoji import EmojiType, format_with_emoji


class CombatDisplay:
    """Handles combat-related display messages."""

    def __init__(self, output_handler: IOutputHandler) -> None:
        self._output_handler: IOutputHandler = output_handler
        self._space: str = " " * 2

    def player_status(self, player: IPlayer) -> None:
        show_player_status(player, self._output_handler)

    def announce_battle(self, enemy_type: str) -> None:
        text: str = format_with_emoji(
            f"You are now facing an enemy({enemy_type})", EmojiType.BATTLE
        )
        self._output_handler.display(text)

    def show_no_weapon_equipped(self) -> None:
        text: str = format_with_emoji(
            "You cannot attack because no weapon is equipped.", EmojiType.CROSS_MARK
        )
        self._output_handler.display(text, self._space)

    def show_player_attack(self, weapon_name: str) -> None:
        message_parts: list[str] = [
            format_with_emoji(" ", EmojiType.ARROW),
            format_with_emoji(
                f"You attacked the enemy with your {weapon_name}.", EmojiType.EXPLOSION
            ),
        ]
        text: str = "".join(message_parts)
        self._output_handler.display(text, self._space)

    def show_enemy_attack(self) -> None:
        message_parts: list[str] = [
            format_with_emoji(" ", EmojiType.ARROW),
            format_with_emoji(f"Enemy attacked you.", EmojiType.FIRE),
        ]
        text: str = "".join(message_parts)
        self._output_handler.display(text)

    def show_victory(self, reward: float) -> None:
        message_parts: list[str] = [
            f"You defeated the enemy.{self._space}",
            format_with_emoji(f"Reward {reward}", EmojiType.COIN),
        ]
        text: str = "".join(message_parts)
        self._output_handler.display(text)

    def show_defeat(self) -> None:
        self._output_handler.display(
            format_with_emoji(f"You have been defeated.", EmojiType.SKULL, "end")
        )
