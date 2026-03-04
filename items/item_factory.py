import random
from typing import Optional

from core.interfaces import IItem, IHealingItem, IWeapon

from loaders.item_config import (
    ItemsConfig,
    WeaponStats,
    HealingItemStats,
    load_items_config,
)

from items.item import Weapon, HealingItem


class ItemFactory:
    """Factory for creating and retrieving game items."""

    _config: Optional[ItemsConfig] = None

    @classmethod
    def _load_config(cls) -> ItemsConfig:
        """
        Load config.

        Raises:
            ConfigError: If config cannot be loaded.
        """
        if cls._config is None:
            cls._config = load_items_config()
        return cls._config

    @classmethod
    def get_all_items(cls) -> list[IItem]:
        weapons: list[IWeapon] = cls.get_all_weapons()
        healing_items: list[IHealingItem] = cls.get_all_healing_items()
        all_items: list[IItem] = [*weapons, *healing_items]
        return all_items

    @classmethod
    def get_all_weapons(cls) -> list[IWeapon]:
        """
        Get all weapon instances.

        Raises:
            ConfigError: If config not loaded.
        """
        config: ItemsConfig = cls._load_config()
        weapons_data: dict[str, WeaponStats] = config["weapon"]
        weapons: list[IWeapon] = [
            Weapon(name, **stats) for name, stats in weapons_data.items()
        ]
        return weapons

    @classmethod
    def get_all_healing_items(cls) -> list[IHealingItem]:
        """
        Get all healing item instances.

        Raises:
            ConfigError: If config not loaded.
        """
        config: ItemsConfig = cls._load_config()
        healing_items_data: dict[str, HealingItemStats] = config["healing_item"]
        healing_items: list[IHealingItem] = [
            HealingItem(name, **stats) for name, stats in healing_items_data.items()
        ]
        return healing_items

    @classmethod
    def get_random_healing_item(cls) -> Optional[IHealingItem]:
        """Get random healing item."""
        items: list[IHealingItem] = cls.get_all_healing_items()
        return random.choice(items) if items else None
