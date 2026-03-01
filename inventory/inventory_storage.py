from typing import Optional

from core.interfaces import IItem, InventorySlot, IInventoryStorage

from inventory.slot import Slot


class SlotIndexError(Exception):
    """Raised when a slot index is invalid."""


class InventoryStorage(IInventoryStorage):
    def __init__(self, max_slots: int = 5) -> None:
        self.slots: list[Slot] = [Slot() for _ in range(max_slots)]

    def add_item(self, item: IItem, quantity: int = 1) -> int:
        """Add items and return leftover."""
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

    def peek_item(self, slot_index: int) -> Optional[IItem]:
        slot: Slot = self._validate_slot_index(slot_index)
        if not slot.item:
            return None
        return slot.item

    def count_item(self, item_name: str) -> int:
        target_name: str = item_name.lower()
        return sum(
            slot.quantity
            for slot in self.slots
            if slot.item and slot.item.name.lower() == target_name
        )

    def is_full(self) -> bool:
        return all(slot.is_full() for slot in self.slots)

    def list_items(self) -> list[InventorySlot]:
        """Return (slot_index, item, quantity) for each non-empty slot."""
        return [
            InventorySlot(index, slot.item, slot.quantity)
            for index, slot in enumerate(self.slots)
            if slot.item
        ]

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

    def auto_sort(self) -> None:
        """
        Consolidate partially filled slots containing the same item.
        Fills slots from left to right by merging items from later slots.
        """
        for index in range(0, len(self.slots)):
            item: Optional[IItem] = self.slots[index].item
            if item is not None and not self.slots[index].is_full():
                self._fill_slot_from_later_slot(index)
        self._remove_empty_gaps()

    def _fill_slot_from_later_slot(self, target_index: int) -> None:
        """Fill target slot by transferring items from later slots with same item."""
        target_slot: Slot = self.slots[target_index]
        target_item: Optional[IItem] = target_slot.item

        if target_item is None:
            return
        for index in range(target_index + 1, len(self.slots)):
            if target_slot.is_full():
                return
            if self._can_transfer_items(target_item.name.lower(), index):
                self._transfer_items(target_index, index)

    def _can_transfer_items(self, target_item_name, source_index: int) -> bool:
        """Check if items can be transferred from source slot."""
        source_slot: Slot = self.slots[source_index]
        return (
            target_item_name == source_slot.item.name.lower()
            if source_slot.item is not None
            else False
        )

    def _transfer_items(self, target_index: int, source_index: int) -> None:
        """Transfer items from source to target slot."""
        target_slot: Slot = self.slots[target_index]
        source_slot: Slot = self.slots[source_index]

        if target_slot.item is None:
            return
        space_available: int = target_slot.item.max_stack - target_slot.quantity
        amount_to_transfer: int = min(space_available, source_slot.quantity)

        target_slot.quantity += amount_to_transfer
        source_slot.quantity -= amount_to_transfer

        if source_slot.quantity == 0:
            source_slot.item = None

    def _remove_empty_gaps(self) -> None:
        """Shift all items to the left, removing empty slots in between."""
        write_pos = 0
        for read_pos in range(len(self.slots)):
            if self.slots[read_pos].item is not None:
                if read_pos != write_pos:
                    self._move_slot_contents(read_pos, write_pos)
                write_pos += 1

    def _move_slot_contents(self, from_index: int, to_index: int) -> None:
        """Move slot contents from one position to another."""
        self.slots[to_index].item = self.slots[from_index].item
        self.slots[to_index].quantity = self.slots[from_index].quantity

        self.slots[from_index].item = None
        self.slots[from_index].quantity = 0

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
