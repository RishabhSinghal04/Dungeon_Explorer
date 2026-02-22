from typing import Optional

from game_flow.vault_encounter import VaultEncounter
from game_flow.game_context import GameContext
from game_flow.inventory_operations import InventoryOperations
from game_flow.encounter_result import EncounterResult
from game_flow.combat import Combat
from game_flow.merchant_interaction import MerchantInteraction

from characters.enemy import create_enemy
from key_maps import build_main_key_map
from game_flow.player.build_player_status import build_player_status


class LevelRunner:
    def __init__(
        self,
        level_num: int,
        difficulty: str,
        vaults: dict[int, VaultEncounter],
        context: GameContext,
    ):
        self.level_num = level_num
        self.difficulty = difficulty
        self.vaults = vaults
        self.context = context

    def run(self, input_chars: list[str]) -> int:
        self._display_level_intro()
        result = self._run_vaults_loop(input_chars)
        self.context.output_handler.display(build_player_status(self.context.player))
        if result <= 0:
            return 0
        return self._after_vaults()

    def _display_level_intro(self) -> None:
        self.context.output_handler.display(f"\nLevel {self.level_num}:-")

    def _run_vaults_loop(self, input_chars: list[str]) -> int:
        total_vaults = len(self.vaults)
        cleared_vaults: set[int] = set()
        MAIN_KEY_MAP = build_main_key_map(total_vaults)

        while len(cleared_vaults) < total_vaults:
            self.context.output_handler.display(
                "\n" + build_player_status(self.context.player)
            )
            choice = self.context.input_handler.get_action(
                f"\nVaults: {self._show_vaults_status(cleared_vaults)}    i. Inventory    0. Exit Game : ",
                MAIN_KEY_MAP,
            )
            self.context.output_handler.display("")
            result = self._handle_choice(
                choice, input_chars, cleared_vaults, MAIN_KEY_MAP
            )
            if result is not None:
                return result
        return 1

    def _show_vaults_status(self, cleared_vaults: set[int]) -> str:
        remaining_valuts = [
            str(vault) for vault in self.vaults.keys() if vault not in cleared_vaults
        ]
        return ", ".join(remaining_valuts) if remaining_valuts else "None"

    def _handle_choice(
        self,
        choice: str,
        input_chars: list[str],
        cleared_vaults: set[int],
        MAIN_KEY_MAP: dict[str, str],
    ) -> Optional[int]:
        if choice == "0":
            return 0
        elif choice in input_chars:
            InventoryOperations(self.context).inventory_operations()
        else:
            result = self._handle_vault_choice(int(choice))
            if result <= 0:
                self.context.output_handler.display(
                    build_player_status(self.context.player)
                )
                return 0
            cleared_vaults.add(int(choice))
            MAIN_KEY_MAP.pop(choice, None)
        return None

    def _handle_vault_choice(self, vault_index: int) -> EncounterResult:
        self.context.output_handler.display(f"-> In vault {vault_index}:-")
        self.context.output_handler.display(build_player_status(self.context.player))
        self.context.output_handler.display("")
        return self.vaults[vault_index].resolve()

    def _after_vaults(self):
        MerchantInteraction(self.context).interact()
        result = Combat(create_enemy("boss", self.difficulty), self.context).start()
        self.context.output_handler.display(build_player_status(self.context.player))
        return result
