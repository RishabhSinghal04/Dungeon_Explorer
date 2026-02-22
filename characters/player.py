from typing import Optional
from interfaces import IItem, IPlayer, IWeapon, IInventory, ICash
from characters.managers import CombatManager, CashManager
from characters.character import Character


# from item import Item


class Player(Character, IPlayer):
    DEFAULT_HEALTH_POINTS = 100
    MAX_HEALTH_POINTS = 100

    def __init__(
        self,
        name: str,
        inventory: IInventory,
        starting_cash: float = 0.0,
        starting_items: dict[IItem, int] = None,
    ):
        super().__init__(self.DEFAULT_HEALTH_POINTS)
        self._name = name
        self._inventory = inventory
        self._cash_manager = CashManager(starting_cash)
        self.combat_manager = CombatManager(self, inventory)

        if starting_items:
            for item, quantity in starting_items.items():
                self.inventory.storage.add_item(item, quantity)
                if (
                    isinstance(item, IWeapon)
                    and not self.combat_manager.equipped_weapon
                ):
                    self.equip_weapon(item.get_name())

        # for item in starting_items.keys():
        #     if isinstance(item, IWeapon):
        #         self.equip_weapon(item.get_name())
        #         break

    @property
    def inventory(self) -> IInventory:
        return self._inventory

    # ___getters___
    @property
    def name(self) -> str:
        return self._name

    @property
    def max_health_points(self) -> int:
        return self.MAX_HEALTH_POINTS

    @property
    def cash(self) -> ICash:
        return self._cash_manager

    def get_health_points(self) -> int:
        return self.health_points

    # def get_cash(self) -> float:
    #     return self.cash.get_balance()

    def get_equipped_weapon(self) -> Optional[IWeapon]:
        """Return the currently equipped weapon, or None if no weapon is equipped."""
        return self.combat_manager.equipped_weapon

    # ___combat___
    def attack(self, target: Character) -> bool:
        """Perform an attack on the target using the equipped weapon. Returns success/failure."""
        return self.combat_manager.attack_performed(target)

    def equip_weapon(self, weapon_name: str) -> bool:
        """Equip a weapon from the inventory by name. Returns success/failure."""
        return self.combat_manager.equip_weapon(weapon_name)

    def use_healing_item(self, index: int) -> bool:
        """Use a healing item to restore health if available. Returns success/failure."""
        return self.combat_manager.healing_item_used(index)

    def update_health_points(self, amount: int) -> None:
        """Update health points by a given amount, clamped between 0 and max health."""
        self.health_points = max(
            0, min(self.MAX_HEALTH_POINTS, self.health_points + amount)
        )

    # ___economy___
    # def add_cash(self, amount: float) -> None:
    #     self.cash.add_cash(amount)

    # def reduce_cash(self, amount: float) -> None:
    #     self.cash.reduce_cash(amount)

    def __str__(self) -> str:
        return f"Player(name={self._name}, HP={self.health_points}, cash={self.get_cash()})"


# ___inventory/equipment___
# def select_weapon(self, weapon_name: str, inventory: Inventory) -> None:
# equipped = self.inventory.equip_weapon(weapon_name)
# if equipped:
#     for slot in self.inventory.slots:
#         if slot.item and slot.item.name.lower() == weapon_name.lower():
#             self.weapon_equipped = slot.item  # assign to weapon_equipped
#             print(f"{self.name} equipped {weapon_name}")
#             return True
# print("Weapon not found in inventory")
# return False
