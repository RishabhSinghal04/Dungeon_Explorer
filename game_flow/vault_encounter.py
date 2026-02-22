from typing import Union

from characters.enemy import Enemy
from .encounter_result import EncounterResult
from item import HealingItem
from game_flow.game_context import GameContext
from game_flow.combat import Combat
from game_flow.inventory_operations import InventoryOperations

from show_options import show_options


class VaultEncounter:
    def __init__(self, content: Union[Enemy, HealingItem, int], context: GameContext):
        self.content = content
        self.context = context

    def resolve(self) -> EncounterResult:
        """Resolve the vault encounter:
        - HealingItem : player can take or leave, returns SUCCESS.
        - Cash (int) : player gains cash, returns SUCCESS.
        - Enemy : triggers combat, returns the result of combat.
        """
        if isinstance(self.content, HealingItem):
            self._found_item()
            return EncounterResult.SUCCESS
        elif isinstance(self.content, int):
            self._found_cash()
            return EncounterResult.SUCCESS
        else:
            return Combat(self.content, self.context).start()

    def _found_item(self) -> None:
        self.context.output_handler.display(f"You found a {self.content.get_name()}.")
        options = {"1": "take", "0": "leave"}

        while True:
            show_options(options, " " * len(options))
            choice = self.context.input_handler.get_action(
                "Select an option: ", options
            )
            if choice == "0":
                self.context.output_handler.display("You left the item.")
                break
            if not self.context.player.inventory.storage.is_full():
                self._add_item()
                break
            self.context.output_handler.display("Inventory is full.")
            InventoryOperations(self.context).inventory_operations()

    def _found_cash(self) -> None:
        self.context.output_handler.display(f"You found {self.content}.")
        self.context.player.cash.add_cash(self.content)

    def _add_item(self) -> None:
        self.context.player.inventory.storage.add_item(self.content)
        self.context.output_handler.display(
            f"{self.content.get_name()} added to inventory."
        )
