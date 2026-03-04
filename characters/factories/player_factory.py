from core.interfaces import IPlayer, IWeapon, IHealingItem

from characters.player import Player
from characters.managers.cash_manager import CashManager

from inventory.inventory import Inventory
from inventory.inventory_manager import InventoryManager
from inventory.inventory_storage import InventoryStorage

from items.item_factory import ItemFactory

from loaders.player_config import PlayerConfig, load_player_config


class PlayerFactory:
    """Factory for creating player instances."""

    @classmethod
    def get_default_weapon(cls) -> IWeapon:
        weapons: list[IWeapon] = ItemFactory().get_all_weapons()
        return min(weapons, key=lambda w: w.attack_points)

    @classmethod
    def get_default_healing_item(cls) -> IHealingItem:
        healing_items: list[IHealingItem] = ItemFactory().get_all_healing_items()
        return min(healing_items, key=lambda h: h.health_points)

    @classmethod
    def create_player(cls, player_name: str) -> IPlayer:
        inventory_storage = InventoryStorage()
        inventory_manager = InventoryManager(inventory_storage)
        inventory = Inventory(inventory_storage, inventory_manager)
        cash_manager = CashManager()

        default_weapon: IWeapon = cls.get_default_weapon()
        default_healing_item: IHealingItem = cls.get_default_healing_item()

        inventory.add_item(default_weapon, 1)
        inventory.add_item(default_healing_item, 2)

        config: PlayerConfig = load_player_config()
        player = Player(player_name, inventory, cash_manager, config)

        player.equip_weapon(default_weapon.name)
        return player
