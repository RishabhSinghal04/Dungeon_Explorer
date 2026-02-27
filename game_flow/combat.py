from typing import Optional

from characters.enemy import Enemy
from core.interfaces import IWeapon
from game_flow.game_context import GameContext
from .encounter_result import EncounterResult

from ui.build_player_status import build_player_status
from ui.show_options import show_options
from game_flow.inventory_operations import InventoryOperations


from input_output.key_maps import COMBAT_KEY_MAP
from ui.emoji import EMOJIS


class Combat:
    def __init__(self, enemy: Enemy, context: GameContext) -> None:
        self._enemy: Enemy = enemy
        self._context: GameContext = context

    def start(self) -> EncounterResult:
        """
        Run the combat loop until outcome is determined.

        Returns:
            EncounterResult: EXIT_GAME, SUCCESS, or DEFEAT.
        """
        self._announce_battle()

        while self._context.player.is_alive() and self._enemy.is_alive():
            action: str = self._prompt_player_action()

            if action == "0":
                return EncounterResult.EXIT_GAME
            elif action == "1":
                self._do_attack()
            elif action == "2":
                InventoryOperations(self._context)

        return self._resolve_outcome()

    def _announce_battle(self) -> None:
        battle_emoji: Optional[str] = EMOJIS.get("battle")
        self._context.output_handler.display(
            f"{battle_emoji}  You are now facing an enemy({self._enemy.type})."
        )

    def _prompt_player_action(self) -> str:
        """
        Prompt player for combat action.

        Returns:
            int: 0 - exit,
                 1 - attack,
                 2 - inventory.
        """
        self._context.output_handler.display(build_player_status(self._context.player))
        show_options(COMBAT_KEY_MAP, " " * len(COMBAT_KEY_MAP))
        action: str = self._context.input_handler.get_action(
            "Select an option: ", COMBAT_KEY_MAP
        )
        return action

    def _do_attack(self) -> None:
        self._player_turn()
        if self._enemy.is_alive():
            self._enemy_turn()

    def _player_turn(self) -> None:
        if not self._context.player.attack(self._enemy):
            self._context.output_handler.display(
                "\nYou cannot attack because no weapon is equipped.", " "
            )
            return

        weapon: Optional[IWeapon] = self._context.player.get_equipped_weapon()
        if weapon:
            self._context.output_handler.display(
                f"\nYou attacked the enemy with your {weapon.name}.", " "
            )

    def _enemy_turn(self) -> None:
        self._enemy.attack(self._context.player)
        self._context.output_handler.display("Enemy attacked you.")

    def _resolve_outcome(self) -> EncounterResult:
        """
        Handle combat outcome and reward player if victorious.

        Returns:
            EncounterResult: VICTORY or DEFEAT.
        """
        if self._context.player.is_alive() and not self._enemy.is_alive():
            self._context.output_handler.display(
                f"You defeated the _enemy. Reward {self._enemy.drop_cash()}"
            )
            self._context.player.cash.add_cash(self._enemy.drop_cash())
            return EncounterResult.SUCCESS
        else:
            self._context.output_handler.display("You have been defeated.")
            return EncounterResult.DEFEAT
