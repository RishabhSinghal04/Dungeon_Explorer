import random
from typing import Optional
from characters import Player
from inventory import Inventory, InventoryManager, InventoryStorage
from item import Item, Weapon, HealingItem
from all_items import all_items


class PlayerFactory:
    @staticmethod
    def get_one_healing_item() -> Optional[HealingItem]:
        healing_items = [item for item in all_items if isinstance(item, HealingItem)]
        if healing_items:
            return random.choice(healing_items)
        return None

    @staticmethod
    def get_default_weapon() -> Weapon:
        weapons = [item for item in all_items if isinstance(item, Weapon)]
        default_weapon = min(weapons, key=lambda w: w._attack_points)
        return default_weapon

    @staticmethod
    def get_default_healing_item() -> HealingItem:
        healing_items = [item for item in all_items if isinstance(item, HealingItem)]
        default_healing_item = min(healing_items, key=lambda h: h.get_health_points())
        return default_healing_item

    @staticmethod
    def create_player(player_name: str) -> Player:
        inventory_storage = InventoryStorage()
        inventory_manager = InventoryManager(inventory_storage)
        inventory = Inventory(inventory_storage, inventory_manager)
        default_weapon = PlayerFactory.get_default_weapon()
        default_healing_item = PlayerFactory.get_default_healing_item()
        starting_items: dict[Item, int] = {default_weapon: 1, default_healing_item: 2}
        player = Player(player_name, inventory, 0, starting_items)
        return player
