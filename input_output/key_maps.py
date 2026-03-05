from enum import Enum


class CombatAction(Enum):
    ATTACK = "1"
    INVENTORY = "i"
    EXIT = "0"


COMBAT_KEY_MAP: dict[str, str] = {
    CombatAction.ATTACK.value: "attack",
    CombatAction.INVENTORY.value: "inventory",
    CombatAction.EXIT.value: "exit_game",
}


class InventoryAction(Enum):
    EQUIP_OR_USE = "1"
    AUTO_SORT = "2"
    VIEW_DESCRIPTION = "3"
    DISCARD_ITEM = "4"
    EXIT = "0"


INVENTORY_KEY_MAP: dict[str, str] = {
    InventoryAction.EQUIP_OR_USE.value: "equip_or_use",
    InventoryAction.AUTO_SORT.value: "auto_sort",
    InventoryAction.VIEW_DESCRIPTION.value: "view_description",
    InventoryAction.DISCARD_ITEM.value: "discard_item",
    InventoryAction.EXIT.value: "exit_inventory",
}


class MerchantAction(Enum):
    """Merchant interaction keys."""

    TALK = "1"
    INVENTORY = "i"
    EXIT = "0"


MERCHANT_KEY_MAP: dict[str, str] = {
    MerchantAction.TALK.value: "talk",
    MerchantAction.INVENTORY.value: "inventory",
    MerchantAction.EXIT.value: "leave",
}


class TradeAction(Enum):
    """Trade action keys."""

    BUY = "1"
    SELL = "2"
    EXIT = "0"


TRADE_KEY_MAP: dict[str, str] = {
    TradeAction.BUY.value: "buy_items",
    TradeAction.SELL.value: "sell_items",
    TradeAction.EXIT.value: "exit",
}


class Confirmation(Enum):
    YES = "1"
    NO = "0"


CONFIRMATION_KEY_MAP: dict[str, str] = {
    Confirmation.YES.value: "yes",
    Confirmation.NO.value: "no",
}


def build_main_key_map(total_vaults: int) -> dict[str, str]:
    key_map: dict[str, str] = {
        str(vault_num): f"crypt_{vault_num}" for vault_num in range(1, total_vaults + 1)
    }

    key_map["i"] = "inventory"
    key_map["0"] = "exit_game"
    return key_map