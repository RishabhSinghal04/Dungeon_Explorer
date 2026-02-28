from typing import Optional

from core.interfaces import (
    ICharacter,
    IPlayer,
    IWeapon,
    IInventory,
    ICash,
    ICombatManager,
)

from characters.character import Character
from characters.managers.combat_manager import CombatManager


class Player(Character, IPlayer):

    def __init__(
        self,
        name: str,
        inventory: IInventory,
        cash: ICash,
        config: dict[str, int],
    ) -> None:
        super().__init__(config["default_health_points"])
        self._name: str = name
        self._inventory: IInventory = inventory
        self._cash: ICash = cash
        self._max_health_points: int = config["max_health_points"]

        self._combat_manager: ICombatManager = CombatManager(
            inventory=self._inventory,
            get_health_points=self.get_health_points,
            max_health_points=self.max_health_points,
            update_health_points=self.update_health_points,
        )

    @property
    def inventory(self) -> IInventory:
        return self._inventory

    # ___getters___
    @property
    def name(self) -> str:
        return self._name

    @property
    def max_health_points(self) -> int:
        return self._max_health_points

    @property
    def cash(self) -> ICash:
        return self._cash

    def get_health_points(self) -> int:
        return self.health_points

    def get_equipped_weapon(self) -> Optional[IWeapon]:
        """Return the currently equipped weapon, or None if no weapon is equipped."""
        return self._combat_manager.equipped_weapon

    def attack(self, target: ICharacter) -> bool:
        """Perform an attack on the target using the equipped weapon. Returns success/failure."""
        return self._combat_manager.attack_performed(target)

    def equip_weapon(self, weapon_name: str) -> bool:
        """Equip a weapon from the inventory by name. Returns success/failure."""
        return self._combat_manager.equip_weapon(weapon_name)

    def unequip_weapon(self) -> None:
        """Unequip the currently equipped weapon."""
        self._combat_manager.equipped_weapon = None

    def use_healing_item(self, index: int) -> bool:
        """Use a healing item to restore health if available. Returns success/failure."""
        return self._combat_manager.healing_item_used(index)

    def update_health_points(self, amount: int) -> None:
        """Update health points by a given amount, clamped between 0 and max health."""
        self.health_points = max(
            0, min(self._max_health_points, self.health_points + amount)
        )

    def __str__(self) -> str:
        return f"Player (name={self._name},  HP={self.health_points}, cash={self.cash.get_balance()})"
