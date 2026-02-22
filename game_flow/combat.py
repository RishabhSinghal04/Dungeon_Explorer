from characters.enemy import Enemy
from game_flow.game_context import GameContext
from .encounter_result import EncounterResult

from .player import build_player_status
from show_options import show_options
from game_flow.inventory_operations import InventoryOperations


from key_maps import COMBAT_KEY_MAP, COMMANDS
from emoji import EMOJIS


class Combat:
    def __init__(self, enemy: Enemy, context: GameContext):
        self.enemy = enemy
        self.context = context

    def start(self) -> EncounterResult:
        """
        Run the combat loop until outcome is determined.

        Returns:
            EncounterResult: EXIT_GAME, SUCCESS, or DEFEAT.
        """
        self._announce_battle()

        while self.context.player.is_alive() and self.enemy.is_alive():
            ACTIONS = {
                0: lambda: EncounterResult.EXIT_GAME,
                1: lambda: self._do_attack(),
                2: lambda: InventoryOperations(self.context).inventory_operations(),
            }
            action = self._prompt_player_action()
            result = ACTIONS.get(action, lambda: None)()
            if result == EncounterResult.EXIT_GAME:
                return EncounterResult.EXIT_GAME

        return self._resolve_outcome()

    def _announce_battle(self) -> None:
        battle_emoji = EMOJIS.get("battle")
        self.context.output_handler.display(
            f"{battle_emoji}  You are now facing {self.enemy.__class__.__name__}"
        )

    def _do_attack(self) -> None:
        self._player_turn()
        if self.enemy.is_alive():
            self._enemy_turn()

    def _player_turn(self) -> None:
        player_attacked = self.context.player.attack(self.enemy)
        if player_attacked:
            self.context.output_handler.display(
                f"\nYou attacked the enemy with your {self.context.player.get_equipped_weapon().get_name()}.",
                " ",
            )
        else:
            self.context.output_handler.display(
                "\nYou cannot attack because no weapon is equipped.", " "
            )

    def _enemy_turn(self) -> None:
        self.enemy.attack(self.context.player)
        self.context.output_handler.display("Enemy attacked you.")

    def _prompt_player_action(self) -> int:
        """
        Prompt player for combat action.

        Returns:
            int: 0 - exit,
                 1 - attack,
                 2 - inventory.
        """
        self.context.output_handler.display(build_player_status(self.context.player))
        show_options(COMBAT_KEY_MAP, " " * len(COMBAT_KEY_MAP))
        action = self.context.input_handler.get_action(
            "Select an option: ", COMBAT_KEY_MAP
        )
        return COMMANDS.get(action, -1)

    def _resolve_outcome(self) -> EncounterResult:
        """
        Handle combat outcome and reward player if victorious.

        Returns:
            EncounterResult: VICTORY or DEFEAT.
        """
        if self.context.player.is_alive() and not self.enemy.is_alive():
            self.context.output_handler.display(
                f"You defeated the enemy. Reward {self.enemy.drop_cash()}"
            )
            self.context.player.cash.add_cash(self.enemy.drop_cash())
            return EncounterResult.SUCCESS
        else:
            self.context.output_handler.display("You have been defeated.")
            return EncounterResult.DEFEAT
