from typing import Optional
from dataclasses import dataclass

from interfaces import IItem, IPlayer
from merchant.merchant import Merchant
from merchant.column_widths import ColumnWidths


@dataclass
class SaleResult:
    success: bool
    message: str
    item: Optional[IItem] = None
    quantity: int = 0
    cash_earned: int = 0


class SellItem(Merchant):
    def __init__(self):
        super().__init__()

    def show_items(self, player: IPlayer) -> list[str]:
        space = " " * 2
        items_with_qty = player.inventory.storage.get_items_with_quantity()
        
        columns: dict[int, str] = {1: "Name", 2: "Quantity", 3: "Price"}
        widths = self._calculate_column_widths(items_with_qty, columns)

        # header
        lines = [
            f"{columns.get(1,"").ljust(widths.name)}{space}"
            f"{columns.get(2,"").center(widths.stat)}{space}"
            f"{columns.get(3,"").rjust(widths.price)}"
        ]
        # rows
        for item, qty in items_with_qty:
            if item is not None:
                lines.append(self._format_item_lines(item, qty, widths, space))
        return lines

    def item_sold(
        self, item_name: str, player: IPlayer, quantity: int = 1
    ) -> SaleResult:
        item = player.inventory.storage.find_item(item_name)
        if not item:
            return SaleResult(False, f"{item_name} not found.")

        current_qty = player.inventory.storage.count_item(item.get_name())

        if quantity > current_qty:
            return SaleResult(False, "Not enough quantity to sell.")

        player.inventory.storage.remove_item(
            item_name=item.get_name(), quantity=quantity
        )
        total_cash = item.get_selling_price() * quantity
        player.cash.add_cash(total_cash)
        return SaleResult(
            True,
            f"Sold {quantity} {item.get_name()} for {total_cash}",
            item,
            quantity,
            total_cash,
        )

    def _group_items(
        self, items_with_qty: list[tuple[Optional[IItem], int]]
    ) -> list[tuple[IItem, int]]:
        grouped = {}
        for item, qty in items_with_qty:
            if item is not None:
                name = item.get_name().lower()
                if item.is_stackable():
                    if name in grouped:
                        existing_item, existing_qty = grouped[name]
                        grouped[name] = (existing_item, existing_qty + qty)
                    else:
                        grouped[name] = (item, qty)
                else:  # non-stackable items stay separate by using a unique key
                    grouped[f"{name}_{id(item)}"] = (item, qty)
        return list(grouped.values())

    def _calculate_column_widths(
        self, items: list[tuple[Optional[IItem], int]], columns: dict[int, str]
    ) -> ColumnWidths:
        name_width = max(
            len(columns.get(1, "")),
            *(len(item.get_name()) for item, _ in items if item is not None),
        )
        stat_width = len(columns.get(2, ""))
        price_width = max(
            len(columns.get(3, "")),
            *(
                len(str(item.get_selling_price()))
                for item, _ in items
                if item is not None
            ),
        )
        return ColumnWidths(name=name_width, stat=stat_width, price=price_width)

    def _format_item_lines(
        self,
        item: IItem,
        qty: int,
        widths: ColumnWidths,
        space: str,
    ) -> str:
        line = (
            f"{item.get_name().ljust(widths.name)}  "
            f"{str(qty).center(widths.stat)}{space}"
            f"{str(item.get_selling_price()).rjust(widths.price)}{space}"
        )
        return line
