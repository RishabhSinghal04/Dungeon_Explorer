from typing import Optional
from interfaces import (
    IItem,
    IWeapon,
    IHealingItem,
    IInventory,
    IInventoryManager,
    IInventoryStorage,
)


class Inventory(IInventory):
    def __init__(self, storage: IInventoryStorage, manager: IInventoryManager):
        self._storage = storage
        self._manager = manager

    @property
    def storage(self) -> IInventoryStorage:
        return self._storage

    @property
    def manager(self) -> IInventoryManager:
        return self._manager

    def get_items(self) -> list[tuple[IItem, int]]:
        return self.storage.list_items()

    def view_description(self, item_name: str) -> str:
        return self.manager.view_description(item_name)

    # def discard_item(self, item: Item) -> None:
    #     slot = self.get_slot(item)
    #     if slot:
    #         slot.remove_item()

    # OR
    def discard_item(self, item_name: str) -> str:
        return self.manager.discard_item_by_name(item_name)

    def add_item(self, item: IItem, quantity: int = 1) -> None:
        self.storage.add_item(item, quantity)

    def try_add_item(self, item: IItem, quantity: int = 1) -> int:
        return self.storage.try_add_item(item, quantity)
        """# try stacking into existing slots
        for slot in self.slots:
            if slot.can_stack_items(item):
                quantity = slot.stack_items(item, quantity)
                if quantity == 0:
                    return "Item added"

        # try placing into empty slots
        for slot in self.slots:
            if slot.item is None:
                # put the item into this empty slot
                slot.item = item

                # put as many as possible
                items_to_add = min(item.max_stack, quantity)
                slot.quantity = items_to_add

                # reduce the leftover quantity
                quantity -= items_to_add

                if quantity == 0:
                    return "Item added"

        return "Inventory is full, leave the item or delete an item""" ""

    # def get_slot(self, item: Item) -> Optional[Slot]:
    #     for slot in self.slots:
    #         if (
    #             not slot.is_empty()
    #             and isinstance(slot.item, Item)
    #             and slot.item.get_name().lower() == item.get_name().lower()
    #         ):
    #             return slot
    #     return None

    # def get_slot_by_name(self, item_name: str) -> Optional[Slot]:
    #     return self.storage.get_slot_by_name(item_name)

    def get_unique_items(self) -> list[str]:
        return self.manager.get_unique_items()

    def get_weapon(self, weapon_name: str) -> Optional[IWeapon]:
        return self.manager.get_weapon(weapon_name)

    def get_healing_item(self, healing_item_name: str) -> Optional[IHealingItem]:
        return self.manager.get_healing_item(healing_item_name)

    def is_full(self) -> bool:
        return self.storage.is_full()

    def find_item(self, item_name: str) -> Optional[IItem]:
        return self.storage.find_item(item_name)
