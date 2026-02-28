from enum import Enum


def build_main_key_map(total_crypts: int) -> dict[str, str]:
    key_map: dict[str, str] = {
        str(vault_num): f"crypt_{vault_num}" for vault_num in range(1, total_crypts + 1)
    }

    key_map["i"] = "inventory"
    key_map["0"] = "exit_game"
    return key_map


class CombatAction(Enum):
    ATTACK = "1"
    INVENTORY = "i"
    EXIT = "0"


class InventoryAction(Enum):
    EQUIP_OR_USE = "1"
    COMBINE = "2"
    VIEW_DESCRIPTION = "3"
    DISCARD_ITEM = "4"
    EXIT = "0"


COMBAT_KEY_MAP: dict[str, str] = {
    CombatAction.ATTACK.value: "attack",
    CombatAction.INVENTORY.value: "inventory",
    CombatAction.EXIT.value: "exit_game",
}

INVENTORY_KEY_MAP: dict[str, str] = {
    InventoryAction.EQUIP_OR_USE.value: "equip_or_use",
    InventoryAction.COMBINE.value: "combine",
    InventoryAction.VIEW_DESCRIPTION.value: "view_description",
    InventoryAction.DISCARD_ITEM.value: "discard_item",
    InventoryAction.EXIT.value: "exit_inventory",
}
