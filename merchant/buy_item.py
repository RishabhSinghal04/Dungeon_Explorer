from typing import Optional
from dataclasses import dataclass

from core.interfaces import IItem, IWeapon, IHealingItem, IPlayer, IItemFormatter
from merchant.merchant import Merchant
from merchant.transaction_results import PurchaseResult


class BuyItem(Merchant):
    def __init__(self, formatter: IItemFormatter, max_healing_item: int = 6) -> None:
        super().__init__()
        self._sorted_items_stock: Optional[list[tuple[IItem, int]]] = None
        self._formatter: IItemFormatter = formatter
        self._max_healing_item: int = max_healing_item

    @property
    def sorted_items_stock(self) -> list[tuple[IItem, int]]:
        if self._sorted_items_stock is None:
            self._sorted_items_stock = sorted(
                self._items_stock.items(),
                key=lambda pair: pair[0].max_stack,
            )
        return self._sorted_items_stock

    def show_items(self, player: IPlayer) -> list[str]:
        """Display available items for purchase with headings: Name, Attack/Health Points, Price."""
        items: list[IItem] = [item for item, _ in self.sorted_items_stock]
        return self._formatter.format_for_purchase(
            items, player, self._max_healing_item
        )

    def buy_item(self, item_name: str, player: IPlayer) -> PurchaseResult:
        """
        Attempt to purchase an item.

        Args:
            item_name (str): Name of the item.
            player (IPlayer): Player object.

        Returns:
            PurchaseResult with success status and message.
        """
        if self._inventory_full(player):
            return PurchaseResult(False, "Inventory is full")

        item: Optional[IItem] = self._find_item(item_name)
        if not item:
            return PurchaseResult(False, f"{item_name} not found")

        if self._owns_weapon(player, item):
            return PurchaseResult(
                False, f"Not available to buy. You already own {item.name}."
            )

        if self._has_too_many_healing_items(player, item):
            return PurchaseResult(
                False,
                f"Not available to buy. You already have {self._max_healing_item} {item.name}s.",
            )

        if not self._can_afford(player, item):
            return PurchaseResult(False, f"Not enough cash to buy {item.name}")

        return self._process_purchase(player, item)

    def _inventory_full(self, player: IPlayer) -> bool:
        return player.inventory.is_full()

    def _find_item(self, item_name: str) -> Optional[IItem]:
        """Find item in stock by name (case-insensitive)."""
        all_items: dict[IItem, int] = self.get_all_items()
        for item in all_items:
            if item.name.lower() == item_name.lower():
                return item
        return None

    def _owns_weapon(self, player: IPlayer, item: IItem) -> bool:
        """Check if player already owns this weapon."""
        if not isinstance(item, IWeapon):
            return False
        weapon: Optional[IItem] = player.inventory.find_item(item.name)
        return weapon is not None and isinstance(weapon, IWeapon)
        # return isinstance(item, IWeapon) and player.inventory.find_item(item.name)

    def _has_too_many_healing_items(self, player: IPlayer, item: IItem) -> bool:
        return (
            isinstance(item, IHealingItem)
            and player.inventory.count_item(item.name) >= self._max_healing_item
        )

    def _can_afford(self, player: IPlayer, item: IItem) -> bool:
        return player.cash.get_balance() >= item.cost_price

    def _process_purchase(self, player: IPlayer, item: IItem) -> PurchaseResult:
        cost: float = item.cost_price
        player.cash.reduce_cash(cost)
        leftover: int = player.inventory.add_item(item, 1)

        if leftover == 0:
            self._items_stock[item] = max(0, self._items_stock[item] - 1)
            return PurchaseResult(True, f"Bought {item.name} for {item.cost_price}")

        player.cash.add_cash(cost)
        return PurchaseResult(False, "Inventory is full. Cannot add item.")
