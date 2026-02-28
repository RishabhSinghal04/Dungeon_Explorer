from typing import Optional

from core.interfaces import IWeapon, IEnemy

from game_flow.game_context import GameContext
from game_flow.inventory_operations import InventoryOperations
from game_flow.encounter_result import EncounterResult

from ui.combat_display import CombatDisplay
from ui.build_player_status import build_player_status
from ui.show_options import show_options

from input_output.key_maps import CombatAction, COMBAT_KEY_MAP


class Combat:
    def __init__(self, enemy: IEnemy, context: GameContext) -> None:
        self._enemy: IEnemy = enemy
        self._context: GameContext = context
        self._display: CombatDisplay = CombatDisplay(context.output_handler)

    def start(self) -> EncounterResult:
        """
        Run the combat loop until outcome is determined.

        Returns:
            EncounterResult: EXIT_GAME, SUCCESS, or DEFEAT.
        """
        self._display.announce_battle(self._enemy.type)

        while self._context.player.is_alive() and self._enemy.is_alive():
            action: str = self._prompt_player_action()

            if action == CombatAction.EXIT.value:
                return EncounterResult.EXIT_GAME
            elif action == CombatAction.ATTACK.value:
                self._do_attack()
            elif action == CombatAction.INVENTORY.value:
                InventoryOperations(self._context).inventory_operations()

        return self._resolve_outcome()

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
            self._display.show_no_weapon_equipped()
            return

        weapon: Optional[IWeapon] = self._context.player.get_equipped_weapon()
        if weapon:
            self._display.show_player_attack(weapon.name)

    def _enemy_turn(self) -> None:
        if self._enemy.attack(self._context.player):
            self._display.show_enemy_attack()

    def _resolve_outcome(self) -> EncounterResult:
        """
        Handle combat outcome and reward player if victorious.

        Returns:
            EncounterResult: VICTORY or DEFEAT.
        """
        if self._context.player.is_alive() and not self._enemy.is_alive():
            reward: float = self._enemy.drop_cash()
            self._display.show_victory(reward)
            self._context.player.cash.add_cash(reward)
            return EncounterResult.SUCCESS
        else:
            self._display.show_defeat()
            return EncounterResult.DEFEAT
