from core.config_loader import load_json_config


def load_player_config(path: str = "config/player.json") -> dict[str, int]:
    raw_config = load_json_config(path)
    return {
        "default_health_points": raw_config["default_health_points"],
        "max_health_points": raw_config["max_health_points"],
    }
