from typing import Optional

from core.interfaces import IEnemy
from characters.factories.enemy_factory import EnemyFactory

from config.game_config import EnemyType, Difficulty

from game_flow.vault_encounter import VaultEncounter
from game_flow.game_context import GameContext
from game_flow.inventory_operations import InventoryOperations
from game_flow.encounter_result import EncounterResult
from game_flow.combat import Combat
from game_flow.merchant_interaction import MerchantInteraction

from input_output.key_maps import build_main_key_map
from ui.confirmation import confirm_action
from ui.build_player_status import build_player_status


class LevelRunner:
    def __init__(
        self,
        level_num: int,
        difficulty: Difficulty,
        vaults: dict[int, VaultEncounter],
        context: GameContext,
        enemy_factory: EnemyFactory,
    ) -> None:
        self._level_num: int = level_num
        self._difficulty: Difficulty = difficulty
        self._vaults: dict[int, VaultEncounter] = vaults
        self._context: GameContext = context
        self._enemy_factory: EnemyFactory = enemy_factory

    def run(self, input_chars: list[str]) -> int:
        self._display_level_intro()
        result: int = self._run_vaults_loop(input_chars)
        if result <= 0:
            return 0
        return self._after_vaults()

    def _display_level_intro(self) -> None:
        self._context.output_handler.display(f"\nLevel {self._level_num}:-")

    def _run_vaults_loop(self, input_chars: list[str]) -> int:
        total_vaults: int = len(self._vaults)
        cleared_vaults: set[int] = set()
        main_key_map: dict[str, str] = build_main_key_map(total_vaults)

        while len(cleared_vaults) < total_vaults:
            self._context.output_handler.display(
                "\n" + build_player_status(self._context.player)
            )
            choice: str = self._context.input_handler.get_action(
                f"\nVaults: {self._show_vaults_status(cleared_vaults)}    i. Inventory    0. Exit Game : ",
                main_key_map,
            )
            self._context.output_handler.display("")
            result: Optional[int] = self._handle_choice(
                choice, input_chars, cleared_vaults, main_key_map
            )
            if result is not None:
                return result
        return 1

    def _show_vaults_status(self, cleared_vaults: set[int]) -> str:
        remaining_valuts: list[str] = [
            str(vault) for vault in self._vaults.keys() if vault not in cleared_vaults
        ]
        return ", ".join(remaining_valuts) if remaining_valuts else "None"

    def _handle_choice(
        self,
        choice: str,
        input_chars: list[str],
        cleared_vaults: set[int],
        main_key_map: dict[str, str],
    ) -> Optional[int]:
        if choice == "0":
            confirm_choice: bool = confirm_action(self._context.input_handler)
            if confirm_choice:
                return 0
        elif choice in input_chars:
            InventoryOperations(self._context).inventory_operations()
        else:
            result: EncounterResult = self._handle_vault_choice(int(choice))
            if result <= 0:
                self._context.output_handler.display(
                    build_player_status(self._context.player)
                )
                return 0
            cleared_vaults.add(int(choice))
            main_key_map.pop(choice, None)
        return None

    def _handle_vault_choice(self, vault_index: int) -> EncounterResult:
        self._context.output_handler.display(f"-> In vault {vault_index}:-")
        self._context.output_handler.display(build_player_status(self._context.player))
        self._context.output_handler.display("")
        return self._vaults[vault_index].resolve()

    def _after_vaults(self) -> EncounterResult:
        MerchantInteraction(self._context).interact()

        boss: IEnemy = self._enemy_factory.create(EnemyType.BOSS, self._difficulty)
        result: EncounterResult = Combat(boss, self._context).start()

        self._context.output_handler.display(build_player_status(self._context.player))
        return result
