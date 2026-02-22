from input_output.display_output import ConsoleOutputHandler
from characters import Player
from item import Item, Weapon, HealingItem
from game_flow.game_context import GameContext

from show_options import show_options
from .player import build_player_status
from key_maps import INVENTORY_KEY_MAP


class InventoryOperations:
    def __init__(self, context: GameContext):
        self.context = context

    def inventory_operations(self) -> None:
        while True:
            items = self.context.player.inventory.storage.list_items()
            if not items:
                self.context.output_handler.display("Inventory is empty")
                return

            self.context.output_handler.display(
                "\n" + build_player_status(self.context.player)
            )
            self.context.output_handler.display(self.format_inventory(items))
            show_options(INVENTORY_KEY_MAP, " " * len(INVENTORY_KEY_MAP))

            action = self.context.input_handler.get_action(
                "Select an option: ", INVENTORY_KEY_MAP
            )

            if action == "0":
                return

            item_map = {
                str(display_index + 1): (slot_index, item)
                for display_index, (slot_index, item, _) in enumerate(items)
                if item is not None
            }
            selection = self.context.input_handler.get_action(
                "Select an item: ", item_map
            )
            slot_index, selected_item = item_map[selection]

            self.handle_inventory_action(action, selected_item, slot_index)

    def format_inventory(
        self, items: list[tuple[int, Item, int]], border_char="="
    ) -> str:
        text = " INVENTORY "

        item_strings = [
            f"{index + 1}. {item.get_name()} (x{quantity})"
            for index, (slot_index, item, quantity) in enumerate(items)
        ]

        max_item_length = max((len(s) for s in item_strings), default=0)
        padded_items = [s.ljust(max_item_length) for s in item_strings]
        item_line = "  ".join(padded_items)
        width = max(len(item_line), len(text))

        return f"{text:^{width}}\n{border_char * width}\n{item_line}\n{border_char * width}"

    def handle_inventory_action(self, action: str, item: Item, index: int) -> None:
        if action == "1":
            result = self._equip_or_use_item(self.context.player, item, index)
            if not result:
                return
            if isinstance(item, Weapon):
                self.context.output_handler.display(f"Equipped {item.get_name()}")
            else:
                self.context.output_handler.display(f"Used {item.get_name()}")
        elif action == "2":
            border = "*" * len(item.get_description())
            self.context.output_handler.display(
                border + "\n" + item.get_description() + "\n" + border
            )
        elif action == "3":
            choice = self._confirm_choice()
            if choice == "0":
                return
            discarded = self._discard_item(index, self.context.player)
            if discarded:
                self.context.output_handler.display(f"Discarded {item.get_name()}")

    def _confirm_choice(self) -> str:
        options: dict[str, str] = {"1": "Yes", "0": "No"}
        show_options(options, " " * len(options))
        return self.context.input_handler.get_action("Select an option: ", options)

    def _discard_item(self, index: int, player: Player) -> bool:
        item, _ = player.inventory.storage.remove_item(index)
        if not item:
            return False

        if item == player.get_equipped_weapon():
            player.combat_manager.equipped_weapon = None
        return True

        # item_name = item.get_name()
        # if item == player.get_equipped_weapon():
        #     player.combat_manager.equipped_weapon = None

        # item_name = player.inventory.storage.remove_item(index)
        # if item_name:
        #     output_handler.display(f"{item_name} discarded from inventory.")

    def _equip_or_use_item(self, player: Player, item: Item, index: int) -> bool:
        if isinstance(item, Weapon):
            return player.equip_weapon(item.get_name())
        elif isinstance(item, HealingItem):
            return player.use_healing_item(index)
