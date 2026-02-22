from typing import Optional
from interfaces import IItem, IInventoryStorage
from inventory.slot import Slot


class InventoryStorage(IInventoryStorage):
    def __init__(self, max_slots: int = 5):
        self.slots = [Slot() for _ in range(max_slots)]

    def add_item(self, item: IItem, quantity: int = 1) -> None:
        self.try_add_item(item, quantity)

    def get_unadded_items(self, item: IItem, quantity: int = 1) -> int:
        """Return how many items could not be added."""
        leftover = quantity
        for slot in self.slots:
            if leftover == 0:
                break
            leftover = slot.simulate_add_item(item, leftover)
        return leftover

    def try_add_item(self, item: IItem, quantity: int = 1) -> int:
        """Convenience method: add items and return leftover."""
        leftover = quantity
        for slot in self.slots:
            if leftover == 0:
                break
            items_that_fit = leftover - slot.simulate_add_item(item, leftover)
            if items_that_fit > 0:
                slot.add_item(item, items_that_fit)
                leftover -= items_that_fit
        return leftover

    def find_item(self, item_name: str) -> Optional[IItem]:
        target_name = item_name.lower()
        for slot in self.slots:
            if not slot.is_empty() and slot.item.get_name().lower() == target_name:
                return slot.item
        return None

    def count_item(self, item_name: str) -> int:
        total = 0
        target_name = item_name.lower()
        for slot in self.slots:
            if not slot.is_empty() and slot.item.get_name().lower() == target_name:
                total += slot.quantity
        return total

    def is_full(self) -> bool:
        return all(slot.is_full() for slot in self.slots)

    def list_items(self) -> list[tuple[int, IItem, int]]:
        """Return (slot_index, item, quantity) for each non-empty slot."""
        result = []
        for index, slot in enumerate(self.slots):
            if not slot.is_empty():
                result.append((index, slot.item, slot.quantity))
        return result
        # return [
        #     (slot.item, slot.quantity) for slot in self.slots if not slot.is_empty()
        # ]

    def get_items_with_quantity(self) -> list[tuple[IItem, int]]:
        unique = {}
        for slot in self.slots:
            if not slot.is_empty():
                name = slot.item.get_name().lower()
                if name not in unique:
                    total_qty = self.count_item(slot.item.get_name())
                    unique[name] = (slot.item, total_qty)
        return list(unique.values())

    def remove_item(
        self,
        slot_index: Optional[int] = None,
        item_name: Optional[str] = None,
        quantity: int = 1,
    ) -> tuple[Optional[IItem], int]:
        if slot_index is not None and 0 <= slot_index < len(self.slots):
            return self._remove_from_slot(slot_index, quantity)

        elif item_name is not None:
            for index, slot in enumerate(self.slots):
                if (
                    not slot.is_empty()
                    and slot.item.get_name().lower() == item_name.lower()
                ):
                    return self._remove_from_slot(index, quantity)
        return None, 0

    def _remove_from_slot(
        self, index: int, quantity: int = 1
    ) -> tuple[Optional[IItem], int]:
        slot = self.slots[index]
        return slot.remove_item(quantity)
