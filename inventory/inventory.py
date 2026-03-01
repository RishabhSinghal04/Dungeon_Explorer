from typing import Optional

from core.interfaces import (
    IItem,
    IWeapon,
    IHealingItem,
    IInventory,
    IInventoryManager,
    IInventoryStorage,
    InventorySlot,
)


class Inventory(IInventory):
    def __init__(self, storage: IInventoryStorage, manager: IInventoryManager) -> None:
        self._storage: IInventoryStorage = storage
        self._manager: IInventoryManager = manager

    @property
    def storage(self) -> IInventoryStorage:
        return self._storage

    @property
    def manager(self) -> IInventoryManager:
        return self._manager

    def add_item(self, item: IItem, quantity: int = 1) -> int:
        """
        Add items to inventory.

        Args:
            item: The item to add.
            quantity: Number of items to add.

        Returns:
            int: Leftover items that could not fit.
        """
        return self._storage.add_item(item, quantity)

    def auto_sort(self) -> None:
        """
        Consolidate and organize inventory slots.

        This method merges partially filled slots containing the same item into
        earlier slots, ensuring stacks are filled from left to right. After merging,
        it shifts all non-empty slots to the front of the inventory, removing gaps
        between items. The result is a compact and organized inventory layout where
        items are grouped together and empty slots are positioned at the end.

        Returns:
            None
        """
        self._storage.auto_sort()

    def count_item(self, item_name: str) -> int:
        """
        Count quantity of an item.

        Args:
            item_name: Name of the item to find.

        Returns:
            int: Total quantity of an item.
        """
        return self._storage.count_item(item_name)

    def remove_item(
        self,
        slot_index: Optional[int] = None,
        item_name: Optional[str] = None,
        quantity: int = 1,
    ) -> tuple[Optional[IItem], int]:
        """
        Remove items from inventory.

        Args:
            slot_index: Remove from specific slot index.
            item_name: Remove by item name.
            quantity: Number of items to remove.

        Returns:
            tuple: (removed_item, actual_quantity_removed)
        """
        return self._storage.remove_item(slot_index, item_name, quantity)

    def find_item(self, item_name: str) -> Optional[IItem]:
        """
        Find an item by name.

        Args:
            item_name: Name of the item to find.

        Returns:
            Optional[IItem]: The item if found, None otherwise.
        """
        return self._storage.find_item(item_name)

    def peek_item(self, slot_index: int) -> Optional[IItem]:
        """
        View item at a specific slot without removing it.

        Args:
            slot_index: Index of the slot to peek at.

        Returns:
            Optional[IItem]: The item in the slot, or None if empty/invalid.
        """
        return self._storage.peek_item(slot_index)

    def is_full(self) -> bool:
        """
        Check if inventory is full.

        Returns:
            bool: True if all slots are at maximum capacity.
        """
        return self._storage.is_full()

    def list_items(self) -> list[InventorySlot]:
        """
        List all items in inventory with their slot positions.

        Returns:
            list[InventorySlot]: List of (index, item, quantity) for occupied slots.
        """
        return self._storage.list_items()

    def get_items_with_quantity(self) -> list[tuple[IItem, int]]:
        """
        Get unique items with their total quantities.

        Returns:
            list[tuple[IItem, int]]: List of (item, total_quantity) pairs.
        """
        return self._storage.get_items_with_quantity()

    def view_description(self, item_name: str) -> str:
        """
        Get formatted description of an item.

        Args:
            item_name: Name of the item.

        Returns:
            str: Formatted description or not-found message.
        """
        return self._manager.view_description(item_name)

    def get_weapon(self, weapon_name: str) -> Optional[IWeapon]:
        """
        Get a weapon item by name.

        Args:
            weapon_name: Name of the weapon.

        Returns:
            Optional[IWeapon]: The weapon if found and is a weapon, None otherwise.
        """
        return self._manager.get_weapon(weapon_name)

    def get_healing_item(self, healing_item_name: str) -> Optional[IHealingItem]:
        """
        Get a healing item by name.

        Args:
            healing_item_name: Name of the healing item.

        Returns:
            Optional[IHealingItem]: The healing item if found and is a healing item, None otherwise.
        """
        return self._manager.get_healing_item(healing_item_name)

    def get_unique_items(self) -> list[IItem]:
        """
        Get list of unique item types (one instance per item type).

        Returns:
            list[IItem]: List of unique items.
        """
        return self._manager.get_unique_items()
