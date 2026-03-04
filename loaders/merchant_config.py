from typing import TypedDict, cast

from core.config_loader import ConfigError, load_json_config


class MerchantConfig(TypedDict):
    """Merchant configuration structure."""

    weapon_stock_quantity: int
    healing_item_stock_quantity: int
    max_healing_items_per_player: int


class RawMerchantConfig(TypedDict, total=False):
    """Raw merchant config from JSON."""

    weapon_stock_quantity: int
    healing_item_stock_quantity: int
    max_healing_items_per_player: int


def load_merchant_config(path: str = "config/merchant.json") -> MerchantConfig:
    """
    Load merchant configuration from JSON file.

    Args:
        path: Path to merchant config file.

    Returns:
        MerchantConfig with validated merchant settings.

    Raises:
        ConfigError: If config cannot be loaded or is invalid.
    """
    raw_data = load_json_config(path)
    raw_config: RawMerchantConfig = cast(RawMerchantConfig, raw_data)

    weapon_stock: int = raw_config.get("weapon_stock_quantity", 1)
    healing_stock: int = raw_config.get("healing_item_stock_quantity", 4)
    max_healing_items: int = raw_config.get("max_healing_items_per_player", 4)

    if not isinstance(weapon_stock, int) or weapon_stock < 0:
        raise ConfigError(
            f"weapon_stock_quantity must be non-negative int, got {weapon_stock}"
        )

    if not isinstance(healing_stock, int) or healing_stock < 0:
        raise ConfigError(
            f"healing_item_stock_quantity must be non-negative int, got {healing_stock}"
        )

    if not isinstance(max_healing_items, int) or max_healing_items < 0:
        raise ConfigError(
            f"max_healing_items_per_player must be non-negative int, got {max_healing_items}"
        )

    return MerchantConfig(
        weapon_stock_quantity=weapon_stock,
        healing_item_stock_quantity=healing_stock,
        max_healing_items_per_player=max_healing_items,
    )
