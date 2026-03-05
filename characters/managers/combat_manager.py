from typing import Optional, Callable

from core.interfaces import (
    ICharacter,
    IItem,
    IWeapon,
    IHealingItem,
    ICombatManager,
    IInventory,
)


class CombatManager(ICombatManager):
    def __init__(
        self,
        inventory: IInventory,
        get_health_points: Callable[[], int],
        max_health_points: int,
        update_health_points: Callable[[int], None],
    ) -> None:

        self._inventory: IInventory = inventory
        self._get_health_points: Callable[[], int] = get_health_points
        self._max_health_points: int = max_health_points
        self._update_health_points: Callable[[int], None] = update_health_points
        self._equipped_weapon: Optional[IWeapon] = None

    @property
    def equipped_weapon(self) -> Optional[IWeapon]:
        return self._equipped_weapon

    @equipped_weapon.setter
    def equipped_weapon(self, weapon: Optional[IWeapon]) -> None:
        self._equipped_weapon = weapon

    def attack_performed(self, target: ICharacter) -> bool:
        """Apply damage to target if a weapon is equipped. Returns success/failure."""
        if not self.equipped_weapon:
            return False
        target.take_damage(self.equipped_weapon.attack_points)
        return True

    def equip_weapon(self, weapon_name: str) -> bool:
        """Equip a weapon from inventory. Returns success/failure."""
        weapon: Optional[IWeapon] = self._inventory.get_weapon(weapon_name)
        if weapon:
            self.equipped_weapon = weapon
            return True
        return False

    def healing_item_used(self, slot_index: int) -> bool:
        """Use a healing item if possible. Returns success/failure."""
        current_health: int = self._get_health_points()
        if current_health >= self._max_health_points:
            return False

        # Peek first to verify it's a healing item
        item: Optional[IItem] = self._inventory.peek_item(slot_index)
        if not item or not isinstance(item, IHealingItem):
            return False

        # Now remove it
        removed_item, removed_qty = self._inventory.remove_item(
            slot_index=slot_index, quantity=1
        )

        # Verify removal was successful and item is correct type
        if not removed_item or removed_qty == 0:
            return False

        if not isinstance(removed_item, IHealingItem):
            # Wrong item type - this shouldn't happen but handle it
            # Re-add the item back
            self._inventory.add_item(removed_item, removed_qty)
            return False

        self._update_health_points(removed_item.health_points)
        return True