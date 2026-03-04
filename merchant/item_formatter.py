from typing import Optional
from dataclasses import dataclass

from core.interfaces import IItemFormatter, IItem, IWeapon, IHealingItem, IPlayer
from merchant.merchant import Merchant


@dataclass
class ColumnWidths:
    name: int
    point: int
    price: int
    quantity: int


class ItemFormatter(IItemFormatter):
    """Handles formatting of items for display."""

    def __init__(self, column_spacing: int = 5) -> None:
        self._column_spacing: int = column_spacing

    def format_headings(self, items_with_qty: list[tuple[IItem, int]]) -> str:
        widths: ColumnWidths = self._calculate_col_widths(items_with_qty)
        lines: str = self._create_header(widths)
        return lines

    def format_for_purchase(
        self,
        items_with_qty: list[tuple[IItem, int]],
        player: IPlayer,
        max_healing_items: int,
    ) -> list[str]:
        """
        Format items for purchase display.

        Args:
            items_with_qty: List of (item, quantity) tuples.
            player: Player viewing the items_with_qty.
            max_healing_items: Maximum healing items_with_qty allowed per player.

        Returns:
            List of formatted strings for display.
        """
        if not items_with_qty:
            return ["No items available for purchase"]
        lines: list[str] = []
        widths: ColumnWidths = self._calculate_col_widths(items_with_qty)

        for item, qty in items_with_qty:
            lines.append(
                self._format_purchase_line(widths, item, qty, player, max_healing_items)
            )
        return lines

    def format_for_sale(self, items_with_qty: list[tuple[IItem, int]]) -> list[str]:
        """
        Format items for sale display.

        Args:
            items_with_qty: List of (item, quantity) tuples.

        Returns:
            List of formatted strings for display.
        """
        if not items_with_qty:
            return ["No items to sell"]
        lines: list[str] = []
        widths: ColumnWidths = self._calculate_col_widths(items_with_qty)

        for item, qty in items_with_qty:
            if item is not None:
                lines.append(self._format_sale_line(widths, item, qty))
        return lines

    def _column_headings(self) -> dict[str, str]:
        columns: dict[str, str] = {
            "name": "Name",
            "point": "Attack/Health Points",
            "price": "Price",
            "quantity": "Quantity",
        }
        return columns

    def _create_header(self, widths: ColumnWidths) -> str:
        columns: dict[str, str] = self._column_headings()
        space: str = " " * self._column_spacing

        return (
            f"{columns['name'].ljust(widths.name)}{space}"
            f"{columns['point'].center(widths.point)}{space}"
            f"{columns['price'].rjust(widths.price)}{space}"
            f"{columns['quantity'].rjust(widths.quantity)}"
        )

    def _calculate_col_widths(
        self, items_with_qty: list[tuple[IItem, int]]
    ) -> ColumnWidths:
        """
        Calculate column widths based on items.

        Args:
            items_with_qty: List of (item, quantity) tuples to display.

        Returns:
            ColumnWidths with calculated widths.
        """
        columns: dict[str, str] = self._column_headings()
        items: list[IItem] = [item for item, _ in items_with_qty]

        name_width: int = max(
            len(columns["name"]), *(len(item.display_name()) for item in items)
        )
        point_width: int = len(columns["point"])
        price_width: int = self._calculate_price_width(items)
        qty_width: int = len(columns["quantity"])
        return ColumnWidths(
            name=name_width, point=point_width, price=price_width, quantity=qty_width
        )

    def _calculate_price_width(self, items: list[IItem]) -> int:
        """Calculate width needed for price column."""
        if not items:
            return self._column_spacing

        max_width: int = 0
        for item in items:
            cost_price_col_width: int = len(str(item.cost_price))
            selling_price_col_width: int = len(str(item.selling_price))
            max_width: int = max(
                max_width, cost_price_col_width, selling_price_col_width
            )

        return max_width

    def _format_purchase_line(
        self,
        widths: ColumnWidths,
        item: IItem,
        qty: int,
        player: IPlayer,
        max_healing_items: int,
    ) -> str:
        """Format a single purchase line."""
        stat_value: str = self._get_item_stat(item)
        space: str = " " * self._column_spacing

        line: str = (
            f"{item.display_name().ljust(widths.name)}{space}"
            f"{stat_value.center(widths.point)}{space}"
            f"{str(item.cost_price).rjust(widths.price)}{space}"
            f"{str(qty).center(widths.quantity)}"
        )

        status: Optional[str] = self._get_purchase_status(
            item, player, max_healing_items
        )
        if status:
            line += f"{space}{status}"
        return line

    def _format_sale_line(self, widths: ColumnWidths, item: IItem, qty: int) -> str:
        """Format a single sale line."""
        stat_value: str = self._get_item_stat(item)
        space: str = " " * self._column_spacing
        line: str = (
            f"{item.display_name().ljust(widths.name)}  "
            f"{stat_value.center(widths.point)}{space}"
            f"{str(item.selling_price).rjust(widths.price)}{space}"
            f"{str(qty).center(widths.quantity)}{space}"
        )
        return line

    def _get_item_stat(self, item: IItem) -> str:
        if isinstance(item, IWeapon):
            return f"Attack: {item.attack_points}"
        elif isinstance(item, IHealingItem):
            return f"Health: {item.health_points}"
        return "-"

    def _get_purchase_status(
        self, item: IItem, player: IPlayer, max_healing_items
    ) -> Optional[str]:
        if isinstance(item, IWeapon):
            weapon: Optional[IItem] = player.inventory.find_item(item.name)
            if weapon:
                return "Own"
        elif isinstance(item, IHealingItem):
            count: int = player.inventory.count_item(item.name)
            if count >= max_healing_items:
                return "Max"
        return None
