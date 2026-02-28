from core.interfaces import IItem, InventorySlot
from characters.player import Player
from items.item import Weapon
from game_flow.game_context import GameContext

from ui.show_options import show_options
from ui.build_player_status import build_player_status
from ui.emoji import get_emoji
from input_output.key_maps import INVENTORY_KEY_MAP


class InventoryOperations:
    def __init__(self, context: GameContext) -> None:
        self.context: GameContext = context

    def inventory_operations(self) -> None:
        while True:
            items: list[InventorySlot] = self.context.player.inventory.list_items()
            if not items:
                self.context.output_handler.display("Inventory is empty")
                return

            self.context.output_handler.display(
                "\n" + build_player_status(self.context.player)
            )
            self.context.output_handler.display(self.format_inventory(items))
            show_options(INVENTORY_KEY_MAP, " " * len(INVENTORY_KEY_MAP))

            action: str = self.context.input_handler.get_action(
                "Select an option: ", INVENTORY_KEY_MAP
            )
            if action == "0":
                return

            selection: int = self.context.input_handler.get_int(
                "Select an item: ", 1, len(items)
            )
            slot: InventorySlot = items[selection - 1]
            slot_index, selected_item = slot.index, slot.item

            self.handle_inventory_action(action, selected_item, slot_index)

    def format_inventory(self, items: list[InventorySlot], border_char="=") -> str:
        text = " INVENTORY "
        item_strings: list[str] = [
            f"{index + 1}. {slot.item.name} (x{slot.quantity})"
            for index, slot in enumerate(items)
        ]

        max_item_length: int = max((len(s) for s in item_strings), default=0)
        padded_items: list[str] = [s.ljust(max_item_length) for s in item_strings]
        item_line: str = "  ".join(padded_items)
        width: int = max(len(item_line), len(text))

        return f"{text:^{width}}\n{border_char * width}\n{item_line}\n{border_char * width}"

    def handle_inventory_action(self, action: str, item: IItem, index: int) -> None:
        if action == "1":
            result: bool = self._equip_or_use_item(self.context.player, item, index)
            if not result:
                return
            if isinstance(item, Weapon):
                self.context.output_handler.display(
                    f"{get_emoji("weapon")}  Equipped {item.name}"
                )
            else:
                self.context.output_handler.display(
                    f"{get_emoji("herb")}  Used {item.name}"
                )
        elif action == "2":
            border: str = "*" * len(item.description)
            self.context.output_handler.display(
                border + "\n" + item.description + "\n" + border
            )
        elif action == "3":
            choice: str = self._confirm_choice()
            if choice == "0":
                return
            discarded: bool = self._discard_item(index, self.context.player)
            if discarded:
                self.context.output_handler.display(f"Discarded {item.name}")

    def _confirm_choice(self) -> str:
        options: dict[str, str] = {"1": "Yes", "0": "No"}
        show_options(options, " " * len(options))
        return self.context.input_handler.get_action("Select an option: ", options)

    def _discard_item(self, index: int, player: Player) -> bool:
        item, _ = player.inventory.storage.remove_item(index)
        if not item:
            return False

        if item == player.get_equipped_weapon():
            player.unequip_weapon()
        return True

    def _equip_or_use_item(self, player: Player, item: IItem, index: int) -> bool:
        if isinstance(item, Weapon):
            return player.equip_weapon(item.name)
        return player.use_healing_item(index)
