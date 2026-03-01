from core.interfaces import IItem, InventorySlot, IPlayer
from items.item import Weapon
from game_flow.game_context import GameContext

from ui.emoji import EmojiType, format_with_emoji
from ui.show_options import show_options
from ui.build_player_status import build_player_status
from ui.confirmation import confirm_action

from input_output.key_maps import InventoryAction, INVENTORY_KEY_MAP


class InventoryOperations:
    def __init__(self, context: GameContext) -> None:
        self._context: GameContext = context

    def inventory_operations(self) -> None:
        while True:
            items: list[InventorySlot] = self._context.player.inventory.list_items()
            if not items:
                self._context.output_handler.display("Inventory is empty")
                return

            self._context.output_handler.display(
                "\n" + build_player_status(self._context.player)
            )
            self._context.output_handler.display(self.format_inventory(items))
            show_options(INVENTORY_KEY_MAP, " " * len(INVENTORY_KEY_MAP))

            action: str = self._context.input_handler.get_action(
                "Select an option: ", INVENTORY_KEY_MAP
            )
            if action == InventoryAction.EXIT.value:
                return
            elif action == InventoryAction.AUTO_SORT.value:
                self._context.player.inventory.auto_sort()
            else:
                selection: int = self._context.input_handler.get_int(
                    "Select an item: ", 1, len(items)
                )
                slot: InventorySlot = items[selection - 1]
                slot_index, selected_item = slot.index, slot.item

                self.handle_inventory_action(action, selected_item, slot_index)

    def format_inventory(self, items: list[InventorySlot], border_char="*") -> str:
        text = " INVENTORY "
        space: str = " " * 4
        item_strings: list[str] = [
            f"{index + 1}. {slot.item.name} (x{slot.quantity})"
            for index, slot in enumerate(items)
        ]

        max_item_length: int = max((len(s) for s in item_strings), default=0)
        padded_items: list[str] = [s.ljust(max_item_length) for s in item_strings]
        item_line: str = space.join(padded_items)
        width: int = max(len(item_line), len(text))
        border: str = " " + (border_char + " ") * (width // 2)

        message_part: list[str] = [f"{text:^{width}}", border, item_line, border]
        return "\n".join(message_part)

    def handle_inventory_action(self, action: str, item: IItem, index: int) -> None:
        if action == InventoryAction.EQUIP_OR_USE.value:
            result: bool = self._equip_or_use_item(self._context.player, item, index)
            if not result:
                return
            if isinstance(item, Weapon):
                self._context.output_handler.display(
                    format_with_emoji(f"Equipped {item.name}", EmojiType.WEAPON)
                )
            else:
                self._context.output_handler.display(
                    format_with_emoji(f"Used {item.name}", EmojiType.HERB)
                )
        elif action == InventoryAction.VIEW_DESCRIPTION.value:
            border: str = "*" * len(item.description)
            self._context.output_handler.display(
                border + "\n" + item.description + "\n" + border
            )
        elif action == InventoryAction.DISCARD_ITEM.value:
            choice: bool = confirm_action(self._context.input_handler)
            if not choice:
                return
            discarded: bool = self._discard_item(index, self._context.player)
            if discarded:
                self._context.output_handler.display(
                    format_with_emoji(f"Discarded {item.name}", EmojiType.GREEN_TICK)
                )

    def _discard_item(self, index: int, player: IPlayer) -> bool:
        item, _ = player.inventory.storage.remove_item(index)
        if not item:
            return False

        if item == player.get_equipped_weapon():
            player.unequip_weapon()
        return True

    def _equip_or_use_item(self, player: IPlayer, item: IItem, index: int) -> bool:
        if isinstance(item, Weapon):
            return player.equip_weapon(item.name)
        return player.use_healing_item(index)
