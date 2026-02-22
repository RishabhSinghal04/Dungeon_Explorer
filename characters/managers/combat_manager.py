from characters.character import Character
from interfaces import IPlayer, IWeapon, IHealingItem, IInventory
from typing import Optional


class CombatManager:
    def __init__(self, player: IPlayer, inventory: IInventory):
        self.player = player
        self.inventory = inventory
        self.equipped_weapon: Optional[IWeapon] = None

    def attack_performed(self, target: Character) -> bool:
        """Apply damage to target if a weapon is equipped. Returns success/failure."""
        if not self.equipped_weapon:
            return False
        target.take_damage(self.equipped_weapon.get_attack_points())
        return True

    def equip_weapon(self, weapon_name: str) -> bool:
        """Equip a weapon from inventory. Returns success/failure."""
        weapon = self.inventory.manager.get_weapon(weapon_name)
        if weapon:
            self.equipped_weapon = weapon
            return True
        return False

    def healing_item_used(self, slot_index: int) -> bool:
        """Use a healing item if possible. Returns success/failure."""
        if self.player.get_health_points() == self.player.max_health_points:
            return False
        item, _ = self.inventory.storage.remove_item(slot_index=slot_index)

        if not item or not isinstance(item, IHealingItem):
            return False
        self.player.update_health_points(item.get_health_points())
        return True
        # healing_item = self.inventory.manager.get_healing_item(healing_item_name)

        # if not healing_item:
        #     return False
        # if self.player.get_health_points() == self.player.max_health_points:
        #     return False

        # self.player.update_health_points(healing_item.get_health_points())
        # self.inventory.manager.discard_item_by_name(healing_item.get_name())
        # return True

    def is_weapon_equipped(self) -> bool:
        return True if self.equipped_weapon else False

    def log_attack(self, target: Character) -> None:
        if not self.equipped_weapon:
            self.log_action(f"{self.player.name} has no weapon equipped to attack")
        else:
            self.log_action(
                f"{self.player.name} attacked {target.__class__.__name__} with {self.equipped_weapon.get_name()}"
            )

    def log_equip_weapon(self, weapon_name: str) -> None:
        if (
            self.equipped_weapon
            and self.equipped_weapon.get_name().lower() == weapon_name.lower()
        ):
            self.log_action(
                f"{self.player.name} equipped {self.equipped_weapon.get_name()}"
            )
        else:
            self.log_action(f"No such weapon found")

    def log_healing_item_used(self, healing_item_name: str, has_used: bool) -> None:
        if has_used:
            self.log_action(f"{self.player.name} has used {healing_item_name}")
        else:
            self.log_action(f"Could not use {healing_item_name}")

    def log_action(self, message: str):
        print(message)
