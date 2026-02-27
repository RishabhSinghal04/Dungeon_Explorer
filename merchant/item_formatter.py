from typing import Optional
from dataclasses import dataclass

from core.interfaces import IItemFormatter, IItem, IWeapon, IHealingItem, IPlayer


@dataclass
class ColumnWidths:
    name: int
    middle: int
    price: int


class ItemFormatter(IItemFormatter):
    """Handles formatting of items for display."""

    def __init__(self, column_spacing: int = 5) -> None:
        self._column_spacing: int = column_spacing

    def format_for_purchase(
        self, items: list[IItem], player: IPlayer, max_healing_items: int
    ) -> list[str]:
        """Format items for purchase display."""
        columns: dict[str, str] = {
            "name": "Name",
            "middle": "Attack/Health Points",
            "price": "Price",
        }
        widths: ColumnWidths = self._calculate_widths_for_purchase(items, columns)

        # header
        lines: list[str] = [self._create_header(columns, widths)]
        # rows
        for item in items:
            lines.append(
                self._format_purchase_line(item, player, widths, max_healing_items)
            )
        return lines

    def format_for_sale(self, items_with_qty: list[tuple[IItem, int]]) -> list[str]:
        columns: dict[str, str] = {
            "name": "Name",
            "middle": "Quantity",
            "price": "Price",
        }
        widths: ColumnWidths = self._calculate_widths_for_sale(items_with_qty, columns)

        # header
        lines: list[str] = [self._create_header(columns, widths)]
        # rows
        for item, qty in items_with_qty:
            if item is not None:
                lines.append(self._format_sale_line(item, qty, widths))
        return lines

    def _create_header(self, columns: dict[str, str], widths: ColumnWidths) -> str:
        space: str = " " * self._column_spacing
        return (
            f"{columns['name'].ljust(widths.name)}{space}"
            f"{columns['middle'].center(widths.middle )}{space}"
            f"{columns['price'].rjust(widths.price)}"
        )

    def _calculate_widths_for_purchase(
        self, items: list[IItem], columns: dict[str, str]
    ) -> ColumnWidths:
        name_width: int = max(len(columns["name"]), *(len(item.name) for item in items))
        middle_width: int = len(columns["middle"])
        price_width: int = max(
            len(columns["price"]),
            *(len(str(item.cost_price)) for item in items),
        )
        return ColumnWidths(name=name_width, middle=middle_width, price=price_width)

    def _calculate_widths_for_sale(
        self, items: list[tuple[IItem, int]], columns: dict[str, str]
    ) -> ColumnWidths:
        name_width: int = max(
            len(columns["name"]),
            *(len(item.name) for item, _ in items if item is not None),
        )
        qty_width: int = len(columns["middle"])
        price_width: int = max(
            len(columns["price"]),
            *(len(str(item.selling_price)) for item, _ in items if item is not None),
        )
        return ColumnWidths(name=name_width, middle=qty_width, price=price_width)

    def _format_purchase_line(
        self, item: IItem, player: IPlayer, widths: ColumnWidths, max_healing_items: int
    ) -> str:
        stat_value: str = self._get_item_stat(item)
        space: str = " " * self._column_spacing

        line: str = (
            f"{item.name.ljust(widths.name)}{space}"
            f"{stat_value.center(widths.middle )}{space}"
            f"{str(item.cost_price).rjust(widths.price)}{space}"
        )

        status: Optional[str] = self._get_purchase_status(
            item, player, max_healing_items
        )
        if status:
            line += f"{space}{status}"

        return line

    def _format_sale_line(self, item: IItem, qty: int, widths: ColumnWidths) -> str:
        space: str = " " * self._column_spacing
        line: str = (
            f"{item.name.ljust(widths.name)}  "
            f"{str(qty).center(widths.middle )}{space}"
            f"{str(item.selling_price).rjust(widths.price)}{space}"
        )
        return line

    def _get_item_stat(self, item: IItem) -> str:
        if isinstance(item, IWeapon):
            return f"Attack: {item.attack_points}"
        elif isinstance(item, IHealingItem):
            return f"Health: {item.health_points}"
        return "-"

    def _get_purchase_status(
        self, item: IItem, player: IPlayer, max_healing_items: int
    ) -> Optional[str]:
        if isinstance(item, IWeapon):
            weapon: Optional[IItem] = player.inventory.find_item(item.name)
            if weapon:
                return "Own"
        elif isinstance(item, IHealingItem):
            count: int = player.inventory.count_item(item.name)
            if count >= max_healing_items:
                return "Enough"
        return None
