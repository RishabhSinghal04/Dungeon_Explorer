from typing import Optional
from interfaces import (
    IItem,
    IWeapon,
    IHealingItem,
    IInventoryStorage,
    IInventoryManager,
)


class InventoryManager(IInventoryManager):
    def __init__(self, storage: IInventoryStorage):
        self.storage = storage

    def view_description(self, item_name: str) -> str:
        item = self.storage.find_item(item_name)
        if item:
            return f"{item.get_name()}: {item.get_description()}"
        return f"{item_name} not found in inventory"

    def get_weapon(self, weapon_name: str) -> Optional[IWeapon]:
        item = self.storage.find_item(weapon_name)
        if item and isinstance(item, IWeapon):
            return item
        return None

    def get_healing_item(self, healing_item_name: str) -> Optional[IHealingItem]:
        item = self.storage.find_item(healing_item_name)
        if item and isinstance(item, IHealingItem):
            return item
        return None

    def get_unique_items(self) -> list[IItem]:
        return [
            item
            for item, _ in self.storage.get_items_with_quantity()
            if item is not None
        ]
