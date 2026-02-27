from characters.player import Player
from characters.managers.cash_manager import CashManager
from inventory.inventory import Inventory
from inventory.inventory_manager import InventoryManager
from inventory.inventory_storage import InventoryStorage
from items.item import Weapon, HealingItem

from loaders.player_config import load_player_config

from items.all_items import all_items


class PlayerFactory:
    @staticmethod
    def get_default_weapon() -> Weapon:
        weapons: list[Weapon] = [item for item in all_items if isinstance(item, Weapon)]
        return min(weapons, key=lambda w: w._attack_points)

    @staticmethod
    def get_default_healing_item() -> HealingItem:
        healing_items: list[HealingItem] = [
            item for item in all_items if isinstance(item, HealingItem)
        ]
        return min(healing_items, key=lambda h: h.health_points)

    @staticmethod
    def create_player(player_name: str) -> Player:
        inventory_storage = InventoryStorage()
        inventory_manager = InventoryManager(inventory_storage)
        inventory = Inventory(inventory_storage, inventory_manager)
        cash_manager = CashManager()

        default_weapon: Weapon = PlayerFactory.get_default_weapon()
        default_healing_item: HealingItem = PlayerFactory.get_default_healing_item()

        inventory.add_item(default_weapon, 1)
        inventory.add_item(default_healing_item, 2)
        cash_manager.add_cash(0)

        config: dict[str, int] = load_player_config()
        player = Player(player_name, inventory, cash_manager, config)

        player._combat_manager.equipped_weapon = default_weapon
        return player
