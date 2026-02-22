def build_main_key_map(total_crypts: int) -> dict[str, str]:
    key_map: dict[str, str] = {
        str(vault_num): f"crypt_{vault_num}" for vault_num in range(1, total_crypts + 1)
    }

    key_map["i"] = "inventory"
    key_map["0"] = "exit_game"
    return key_map


COMBAT_KEY_MAP: dict[str, str] = {"1": "attack", "i": "inventory", "0": "exit_game"}

INVENTORY_KEY_MAP: dict[str, str] = {
    "1": "equip_or_use",
    "2": "view_description",
    "3": "discard_item",
    "0": "exit_inventory",
}

# 0 : exit, 1 : attack, 2 : inventory
COMMANDS = {"0": 0, "1": 1, "i": 2, "I": 2}
