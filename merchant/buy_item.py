from typing import Optional

from core.interfaces import IItem, IItemFormatter, IPlayer

from merchant.merchant import Merchant
from merchant.transaction_results import PurchaseResult

from loaders.merchant_config import MerchantConfig


class BuyItem(Merchant):
    def __init__(
        self,
        formatter: IItemFormatter,
        config: Optional[MerchantConfig] = None,
    ) -> None:
        """
        Initialize buy service.

        Args:
            formatter: Item formatter for display.
            config: Optional merchant configuration.
        """
        super().__init__(config)
        self._formatter: IItemFormatter = formatter

    def get_sorted_stock(self, player: IPlayer) -> list[tuple[IItem, int]]:
        """
        Get sorted available stock for player.

        Args:
            player: The player viewing items.

        Returns:
            list of (item, quantity) tuples sorted by stack size.
        """
        stock: dict[IItem, int] = self.get_available_stock(player)
        return sorted(stock.items(), key=lambda pair: pair[0].max_stack)

    def show_items(self, player: IPlayer) -> list[str]:
        """
        Display available items for purchase.

        Args:
            player: The player viewing items.

        Returns:
            list of formatted item strings for display.
        """
        items: list[tuple[IItem, int]] = self.get_sorted_stock(player)
        max_healing_items: int = self._config["max_healing_items_per_player"]

        return self._formatter.format_for_purchase(items, player, max_healing_items)

    def buy_item(self, item_name: str, player: IPlayer) -> PurchaseResult:
        """
        Attempt to purchase an item.

        Args:
            item_name (str): Name of the item.
            player (IPlayer): Player object.

        Returns:
            PurchaseResult with success status and message.
        """
        if player.inventory.is_full():
            return PurchaseResult(False, "Inventory is full")

        available_stock: dict[IItem, int] = self.get_available_stock(player)

        item: Optional[IItem] = self._find_item_in_stock(item_name, available_stock)
        if not item:
            return PurchaseResult(False, f"{item_name} not found")

        if not self._can_afford(item, player):
            return PurchaseResult(
                False, f"Not enough cash to buy {item.display_name()}"
            )

        return self._process_purchase(item, player)

    def _find_item_in_stock(
        self, item_name: str, stock: dict[IItem, int]
    ) -> Optional[IItem]:
        """Find item in stock by name (case-insensitive)."""
        for item in stock:
            if item.name.lower() == item_name.lower():
                return item
        return None

    def _can_afford(self, item: IItem, player: IPlayer) -> bool:
        return player.cash.get_balance() >= item.cost_price

    def _process_purchase(self, item: IItem, player: IPlayer) -> PurchaseResult:
        cost: float = item.cost_price
        player.cash.reduce_cash(cost)
        leftover: int = player.inventory.add_item(item, 1)

        if leftover == 0:
            return PurchaseResult(
                True, f"Bought {item.display_name()} for {item.cost_price}"
            )
        else:
            player.cash.add_cash(cost)
            return PurchaseResult(False, "Inventory is full. Cannot add item.")
