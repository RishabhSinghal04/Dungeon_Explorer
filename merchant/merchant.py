from typing import Optional

from core.interfaces import IItem, IWeapon, IHealingItem, IPlayer

from loaders.merchant_config import load_merchant_config

from items.all_items import all_items


class Merchant:
    """Base merchant with stock management."""

    def __init__(self, config: Optional[dict[str, int]] = None) -> None:
        self._config: dict[str, int] = config or load_merchant_config()
        self._items_stock: dict[IItem, int] = self._initialize_stock()

    def show_player_cash(self, player: IPlayer) -> str:
        """Get player's cash balance as string."""
        return f"{player.cash.get_balance()}"

    def get_all_items(self) -> dict[IItem, int]:
        """Get current stock."""
        return self._items_stock

    def _initialize_stock(self) -> dict[IItem, int]:
        """Initialize merchant's stock with default quantities."""
        stock: dict[IItem, int] = {}
        for item in all_items:
            if isinstance(item, IWeapon):
                stock[item] = self._config["weapon_stock_quantity"]
            elif isinstance(item, IHealingItem):
                stock[item] = self._config["healing_item_stock_quantity"]
        return stock
