from core.interfaces import IItem, InventorySlot, IPlayer
from items.item import Weapon
from game_flow.game_context import GameContext

from ui.inventory_operations_display import InventoryOperationsDisplay
from ui.confirmation import confirm_action

from input_output.key_maps import InventoryAction, INVENTORY_KEY_MAP


class InventoryOperations:
    def __init__(self, context: GameContext) -> None:
        self._context: GameContext = context
        self._display = InventoryOperationsDisplay(self._context.output_handler)

    def inventory_operations(self) -> None:
        while True:
            items: list[InventorySlot] = self._context.player.inventory.list_items()
            if not items:
                self._display.empty_inventory()
                return
            self._display.player_status(self._context.player)
            self._display.show_inventory(items)
            self._display.format_options(INVENTORY_KEY_MAP)

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

    def handle_inventory_action(self, action: str, item: IItem, index: int) -> None:
        if action == InventoryAction.EQUIP_OR_USE.value:
            result: bool = self._equip_or_use_item(self._context.player, item, index)
            if not result:
                return
            if isinstance(item, Weapon):
                self._display.show_equiped(item)
            else:
                self._display.show_used(item)
        elif action == InventoryAction.VIEW_DESCRIPTION.value:
            self._display.show_description(item)
        elif action == InventoryAction.DISCARD_ITEM.value:
            choice: bool = confirm_action(self._context.input_handler)
            if not choice:
                return
            discarded: bool = self._discard_item(index, self._context.player)
            if discarded:
                self._display.show_discarded(item)

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
