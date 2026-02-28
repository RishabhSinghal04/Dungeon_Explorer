from typing import Optional

from core.interfaces import IItem, InventorySlot, IInventoryStorage

from inventory.slot import Slot


class SlotIndexError(Exception):
    """Raised when a slot index is invalid."""


class InventoryStorage(IInventoryStorage):
    def __init__(self, max_slots: int = 5) -> None:
        self.slots: list[Slot] = [Slot() for _ in range(max_slots)]

    # def add_item(self, item: IItem, quantity: int = 1) -> None:
    #     self.try_add_item(item, quantity)

    # def get_unadded_items(self, item: IItem, quantity: int = 1) -> int:
    #     """Return how many items could not be added."""
    #     leftover = quantity
    #     for slot in self.slots:
    #         if leftover == 0:
    #             break
    #         leftover = slot.simulate_add_item(item, leftover)
    #     return leftover

    def add_item(self, item: IItem, quantity: int = 1) -> int:
        """Convenience method: add items and return leftover."""
        leftover: int = quantity
        for slot in self.slots:
            if leftover == 0:
                break
            items_that_fit: int = leftover - slot.simulate_add_item(item, leftover)
            if items_that_fit > 0:
                slot.add_item(item, items_that_fit)
                leftover -= items_that_fit
        return leftover

    def find_item(self, item_name: str) -> Optional[IItem]:
        slot: Optional[Slot] = self._find_slot_by_name(item_name)
        if not slot or slot.item is None:
            return None
        return slot.item
        # target_name: str = item_name.lower()
        # for slot in self.slots:
        #     if slot.item is not None and slot.item.name.lower() == target_name:
        #         return slot.item
        # return None

    def peek_item(self, slot_index: int) -> Optional[IItem]:
        slot: Slot = self._validate_slot_index(slot_index)
        if not slot.item:
            return None
        return slot.item

        # if slot_index < 0 or slot_index >= len(self.slots):
        #     return
        # return self.slots[slot_index].item

    def count_item(self, item_name: str) -> int:
        target_name: str = item_name.lower()
        return sum(
            slot.quantity
            for slot in self.slots
            if slot.item and slot.item.name.lower() == target_name
        )
        # total = 0
        # target_name: str = item_name.lower()
        # for slot in self.slots:
        #     if slot.item is not None and slot.item.name.lower() == target_name:
        #         total += slot.quantity
        # return total

    def is_full(self) -> bool:
        return all(slot.is_full() for slot in self.slots)

    def list_items(self) -> list[InventorySlot]:
        """Return (slot_index, item, quantity) for each non-empty slot."""
        return [
            InventorySlot(index, slot.item, slot.quantity)
            for index, slot in enumerate(self.slots)
            if slot.item
        ]
        # result = []
        # for index, slot in enumerate(self.slots):
        #     if slot.item is not None:
        #         result.append((index, slot.item, slot.quantity))
        # return result
        # return [
        #     (slot.item, slot.quantity) for slot in self.slots if not slot.is_empty()
        # ]

    def get_items_with_quantity(self) -> list[tuple[IItem, int]]:
        unique = {}
        for slot in self.slots:
            if slot.item is not None:
                name: str = slot.item.name.lower()
                if name not in unique:
                    total_qty: int = self.count_item(slot.item.name)
                    unique[name] = (slot.item, total_qty)
        return list(unique.values())

    def remove_item(
        self,
        slot_index: Optional[int] = None,
        item_name: Optional[str] = None,
        quantity: int = 1,
    ) -> tuple[Optional[IItem], int]:
        slot: Optional[Slot] = None

        if slot_index is not None:
            slot = self._validate_slot_index(slot_index)
            return slot.remove_item(quantity)

        elif item_name is not None:
            slot = self._find_slot_by_name(item_name)
            if not slot:
                return None, 0
            return slot.remove_item(quantity)

        raise ValueError("Either slot_index or item_name must be provided")

        # if slot_index is not None and 0 <= slot_index < len(self.slots):
        #     return self._remove_from_slot(slot_index, quantity)

        # elif item_name is not None:
        #     for index, slot in enumerate(self.slots):
        #         if (
        #             slot.item is not None
        #             and slot.item.name.lower() == item_name.lower()
        #         ):
        #             return self._remove_from_slot(index, quantity)
        # return None, 0

    def _find_slot_by_name(self, item_name: str) -> Optional[Slot]:
        target_name: str = item_name.lower()
        for slot in self.slots:
            if slot.item and slot.item.name.lower() == target_name:
                return slot
        return None

    def _validate_slot_index(self, slot_index: int) -> Slot:
        if slot_index < 0 or slot_index >= len(self.slots):
            raise SlotIndexError(f"Invalid slot index: {slot_index}")
        return self.slots[slot_index]
