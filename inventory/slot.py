from typing import Optional

from core.interfaces import IItem


class Slot:
    def __init__(self, item: Optional[IItem] = None, quantity: int = 0) -> None:
        self.item: Optional[IItem] = item
        self.quantity: int = quantity

    def is_full(self) -> bool:
        """Check if slot is at maximum capacity."""
        return self.item is not None and self.quantity >= self.item.max_stack

    def add_item(self, item: IItem, quantity: int = 1) -> int:
        """
        Add items into this slot. Returns leftover quantity.

        Args:
            item (IItem): The item to add.
            quantity (int): Number of items to add.

        Returns:
            int: Leftover items that could not fit in this slot.
        """
        if self._can_stack_items(item):
            return self._stack_items(item, quantity)
        elif self.item is None:
            self.item = item
            items_to_add: int = min(item.max_stack, quantity)
            self.quantity = items_to_add
            return quantity - items_to_add
        return quantity

    def simulate_add_item(self, item: IItem, quantity: int = 1) -> int:
        """
        Simulate adding items into this slot without mutating state.

        Args:
            item (IItem): The item to add.
            quantity (int): Number of items to add.

        Returns:
            int: Leftover items that could not fit in this slot.
        """
        if self._can_stack_items(item) and self.item is not None:
            space_left: int = self.item.max_stack - self.quantity
            return max(0, quantity - space_left)
        elif self.item is None:
            items_to_add: int = min(item.max_stack, quantity)
            return quantity - items_to_add
        return quantity

    def remove_item(self, quantity: int = 1) -> tuple[Optional[IItem], int]:
        """
        Remove a given quantity of items from the slot.

        Args:
            quantity: Number of items to remove.

        Returns:
            tuple: (item_reference, actual_quantity_removed)
        """
        if self.item is None:
            return None, 0
        removed: int = min(quantity, self.quantity)
        self.quantity -= removed
        item_ref: Optional[IItem] = self.item

        if self.quantity == 0:
            self.item = None
        return item_ref, removed

    def _can_stack_items(self, item: IItem) -> bool:
        return (
            item.stackable
            and not self.is_full()
            and self.item is not None
            and self.item.name.lower() == item.name.lower()
        )

    def _stack_items(self, item: IItem, quantity: int = 1) -> int:
        """
        Stack items into this slot if possible.

        Args:
            item (IItem): The item to stack.
            quantity (int): Number of items to stack.

        Returns:
            int: Leftover items that could not fit in this slot.
        """
        if not self._can_stack_items(item) or self.item is None:
            return quantity

        # Calculate space available before stacking
        space_left: int = self.item.max_stack - self.quantity

        # decide how many items to put in a slot
        items_to_add: int = min(space_left, quantity)

        # increase the quantity of item that has been added into the slot
        self.quantity += items_to_add
        return quantity - items_to_add
