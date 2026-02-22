from typing import Optional
from interfaces import IItem


class Slot:
    def __init__(self, item: Optional[IItem] = None, quantity: int = 0):
        self.item = item
        self.quantity = quantity

    def is_empty(self) -> bool:
        """Check if a slot is empty"""
        return self.item is None

    def is_full(self) -> bool:
        return not self.is_empty() and self.quantity >= self.item.get_max_stack()

    def add_item(self, item: IItem, quantity: int = 1) -> None:
        """
        Try to add items into this slot.

        Args:
            item (IItem): The item to add.
            quantity (int): Number of items to add.
        """
        if self.can_stack_items(item):
            return self._stack_items(item, quantity)
        elif self.is_empty():
            self.item = item
            items_to_add = min(item.get_max_stack(), quantity)
            self.quantity = items_to_add
        #     return quantity - items_to_add
        # return quantity

    def simulate_add_item(self, item: IItem, quantity: int = 1) -> int:
        """
        Simulate adding items into this slot without mutating state.

        Args:
            item (IItem): The item to add.
            quantity (int): Number of items to add.

        Returns:
            int: Leftover items that could not fit in this slot.
        """
        if self.can_stack_items(item):
            space_left = self.item.get_max_stack() - self.quantity
            return max(0, quantity - space_left)
        elif self.is_empty():
            items_to_add = min(item.get_max_stack(), quantity)
            return quantity - items_to_add
        return quantity

    def _stack_items(self, item: IItem, quantity: int = 1) -> None:
        """
        Stack items into this slot if possible.

        Args:
            item (IItem): The item to stack.
            quantity (int): Number of items to stack.
        """
        if not self.can_stack_items(item):
            return

        # calculate the space left in this slot (after stacking item)
        space_left = self.item.get_max_stack() - self.quantity

        # decide how many items to put in a slot
        items_to_add = min(space_left, quantity)

        # increase the quantity of item that has been added into the slot
        self.quantity += items_to_add

        # return leftover items
        # return quantity - items_to_add

    def can_stack_items(self, item: IItem) -> bool:
        return (
            item.is_stackable()
            and not self.is_empty()
            and not self.is_full()
            and self.item.get_name().lower() == item.get_name().lower()
        )

    def remove_item(self, quantity: int = 1) -> tuple[Optional[IItem], int]:
        """
        Remove a given quantity of items from the slot.
        Returns the actual number removed.
        """
        if self.is_empty():
            return 0
        removed = min(quantity, self.quantity)
        self.quantity -= removed
        item_ref = self.item

        if self.quantity == 0:
            self.item = None
        return item_ref, removed
