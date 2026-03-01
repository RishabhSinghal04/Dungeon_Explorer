from typing import Optional

from core.interfaces import IItem, IPlayer, IItemFormatter
from merchant.merchant import Merchant
from merchant.transaction_results import SaleResult


class SellItem(Merchant):
    def __init__(self, formatter: IItemFormatter) -> None:
        super().__init__()
        self._formatter: IItemFormatter = formatter

    def show_items(self, player: IPlayer) -> list[str]:
        """
        Display player's items available for sale.

        Args:
            player (IPlayer): The player whose items to display.

        Returns:
            list[str]: Formatted lines showing items with quantities and prices.
        """
        items_with_qty: list[tuple[IItem, int]] = (
            player.inventory.get_items_with_quantity()
        )
        return self._formatter.format_for_sale(items_with_qty)

    def sell_item(
        self, item_name: str, player: IPlayer, quantity: int = 1
    ) -> SaleResult:
        """
        Attempt to sell items.

        Args:
            item_name (str): Name of item to sell.
            player (IPlayer): The player selling items.
            quantity (int): Number of items to sell.

        Returns:
            SaleResult with success status and details.
        """
        if quantity <= 0:
            return SaleResult(False, "Quantity must be positive.")

        item: Optional[IItem] = player.inventory.find_item(item_name)
        if not item:
            return SaleResult(False, f"{item_name} not found.")

        current_qty: int = player.inventory.count_item(item.name)
        if quantity > current_qty:
            return SaleResult(False, "Not enough quantity to sell.")

        player.inventory.remove_item(item_name=item.name, quantity=quantity)
        total_cash: float = item.selling_price * quantity
        player.cash.add_cash(total_cash)
        return SaleResult(
            True,
            f"Sold {quantity} {item.name} for {total_cash}",
            item,
            quantity,
            total_cash,
        )

    # def _group_items(
    #     self, items_with_qty: list[tuple[IItem, int]]
    # ) -> list[tuple[IItem, int]]:
    #     grouped = {}
    #     for item, qty in items_with_qty:
    #         if item is not None:
    #             name: str = item.name.lower()
    #             if item.stackable:
    #                 if name in grouped:
    #                     existing_item, existing_qty = grouped[name]
    #                     grouped[name] = (existing_item, existing_qty + qty)
    #                 else:
    #                     grouped[name] = (item, qty)
    #             else:  # non-stackable items stay separate by using a unique key
    #                 grouped[f"{name}_{id(item)}"] = (item, qty)
    #     return list(grouped.values())
