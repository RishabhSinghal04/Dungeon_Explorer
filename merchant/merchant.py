from typing import Optional

from core.interfaces import IItem, IWeapon, IHealingItem, IPlayer
from items.item_factory import ItemFactory
from loaders.merchant_config import MerchantConfig, load_merchant_config


class Merchant:
    """Base merchant with stock management."""

    def __init__(self, config: Optional[MerchantConfig] = None) -> None:
        """
        Initialize merchant.

        Args:
            config: Optional merchant configuration.

        Raises:
            ConfigError: If config cannot be loaded.
        """
        self._config: MerchantConfig = config or load_merchant_config()

    def show_player_cash(self, player: IPlayer) -> str:
        """Get player's cash balance as string."""
        return f"{player.cash.get_balance()}"

    def get_available_stock(self, player: IPlayer) -> dict[IItem, int]:
        """
        Get available stock filtered for a specific player.

        Filters out weapons player already owns and adjusts healing item
        quantities based on player's current inventory.

        Args:
            player: The player viewing the merchant.

        Returns:
            dict mapping available items to quantities.
        """
        stock: dict[IItem, int] = {}
        weapons: list[IWeapon] = ItemFactory.get_all_weapons()
        healing_items: list[IHealingItem] = ItemFactory.get_all_healing_items()

        weapon_stock_qty: int = self._config.get("weapon_stock_quantity")
        healing_item_stock_qty: int = self._config.get("healing_item_stock_quantity")
        max_healing_items: int = self._config.get("max_healing_items_per_player")

        for weapon in weapons:
            stock[weapon] = (
                0 if player.inventory.find_item(weapon.name) else weapon_stock_qty
            )

        for healing_item in healing_items:
            current_count: int = player.inventory.count_item(healing_item.name)
            available: int = max_healing_items - current_count
            stock[healing_item] = (
                min(available, healing_item_stock_qty) if available > 0 else 0
            )

        return stock
