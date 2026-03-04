from typing import Any, TypedDict, cast

from core.config_loader import ConfigError, load_json_config


class WeaponStats(TypedDict):
    attack_points: int
    cost_price: float


class HealingItemStats(TypedDict):
    health_points: int
    cost_price: float


class ItemsConfig(TypedDict):
    weapon: dict[str, WeaponStats]
    healing_item: dict[str, HealingItemStats]


class RawItemConfig(TypedDict, total=False):
    weapon: dict[str, WeaponStats]
    healing_item: dict[str, HealingItemStats]


def load_items_config(path: str = "config/items.json") -> ItemsConfig:
    """
    Load items configuration from JSON file.

    Args:
        path: Path to items config file.
        output_handler: Optional handler to display errors.

    Returns:
        ItemsConfig with weapon and healing_item data.

    Raises:
        ConfigError: If config cannot be loaded or is invalid.
    """
    raw_data = load_json_config(path)
    raw_config: RawItemConfig = cast(RawItemConfig, raw_data)

    if "weapon" not in raw_config:
        raise ConfigError(f"Missing required keys 'weapon' in {path}")
    if "healing_item" not in raw_config:
        raise ConfigError(f"Missing required keys 'healing_item' in {path}")

    weapons = raw_data["weapon"]
    if not isinstance(weapons, dict):
        raise ConfigError(
            f"'weapon' must be a dict in {path}, got {type(weapons).__name__}"
        )
    validated_weapons: dict[str, WeaponStats] = _validate_weapons(weapons, path)

    healing_items = raw_data["healing_item"]
    if not isinstance(healing_items, dict):
        raise ConfigError(
            f"'healing_item' must be a dict in {path}, got {type(healing_items).__name__}"
        )
    validated_healing_items: dict[str, HealingItemStats] = _validate_healing_items(
        healing_items, path
    )

    return ItemsConfig(weapon=validated_weapons, healing_item=validated_healing_items)


def _validate_weapons(weapons: dict[str, Any], path: str) -> dict[str, WeaponStats]:
    """
    Validate weapon data structure.

    Args:
        weapons: Raw weapon data from JSON.
        path: Config file path for error messages.

    Returns:
        Validated weapon stats dict.

    Raises:
        ConfigError: If weapon data is invalid.
    """
    validated: dict[str, WeaponStats] = {}

    for weapon_name, stats in weapons.items():
        if not isinstance(weapon_name, str):
            raise ConfigError(f"Weapon name must be string in {path}")

        if not isinstance(stats, dict):
            raise ConfigError(
                f"Stats for weapon '{weapon_name}' must be a dict in {path}"
            )

        if "attack_points" not in stats:
            raise ConfigError(
                f"Missing 'attack_points' for weapon '{weapon_name}' in {path}"
            )
        if "cost_price" not in stats:
            raise ConfigError(
                f"Missing 'cost_price' for weapon '{weapon_name}' in {path}"
            )

        attack_points = stats["attack_points"]
        cost_price = stats["cost_price"]

        if not isinstance(attack_points, int) or attack_points < 1:
            raise ConfigError(
                f"attack_points for '{weapon_name}' must be positive int, "
                f"got {attack_points}"
            )

        if not isinstance(cost_price, (int, float)) or cost_price < 0:
            raise ConfigError(
                f"cost_price for '{weapon_name}' must be non-negative number, "
                f"got {cost_price}"
            )

        validated[weapon_name] = WeaponStats(
            attack_points=attack_points, cost_price=float(cost_price)
        )

    return validated


def _validate_healing_items(
    healing_items: dict[str, Any], path: str
) -> dict[str, HealingItemStats]:
    """
    Validate healing item data structure.

    Args:
        healing_items: Raw healing item data from JSON.
        path: Config file path for error messages.

    Returns:
        Validated healing item stats dict.

    Raises:
        ConfigError: If healing item data is invalid.
    """
    validated: dict[str, HealingItemStats] = {}

    for item_name, stats in healing_items.items():
        if not isinstance(item_name, str):
            raise ConfigError(f"Healing item name must be string in {path}")

        if not isinstance(stats, dict):
            raise ConfigError(
                f"Stats for healing item '{item_name}' must be a dict in {path}"
            )

        if "health_points" not in stats:
            raise ConfigError(
                f"Missing 'health_points' for healing item '{item_name}' in {path}"
            )
        if "cost_price" not in stats:
            raise ConfigError(
                f"Missing 'cost_price' for healing item '{item_name}' in {path}"
            )

        health_points = stats["health_points"]
        cost_price = stats["cost_price"]

        if not isinstance(health_points, int) or health_points < 1:
            raise ConfigError(
                f"health_points for '{item_name}' must be positive int, "
                f"got {health_points}"
            )

        if not isinstance(cost_price, (int, float)) or cost_price < 0:
            raise ConfigError(
                f"cost_price for '{item_name}' must be non-negative number, "
                f"got {cost_price}"
            )

        validated[item_name] = HealingItemStats(
            health_points=health_points, cost_price=float(cost_price)
        )

    return validated
