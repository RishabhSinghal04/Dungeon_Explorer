from core.config_loader import load_json_config


def load_merchant_config(path: str = "config/merchant.json") -> dict[str, int]:
    return load_json_config(path)
