from typing import TypedDict, cast

from core.config_loader import ConfigError, load_json_config


class PlayerConfig(TypedDict):
    """Player configuration structure."""

    default_health_points: int
    max_health_points: int


class RawPlayerConfig(TypedDict, total=False):
    """Raw player config from JSON."""

    default_health_points: int
    max_health_points: int


def load_player_config(path: str = "config/player.json") -> PlayerConfig:
    raw_data = load_json_config(path)
    raw_config: RawPlayerConfig = cast(RawPlayerConfig, raw_data)

    default_health: int = raw_config.get("default_health_points", 100)
    max_health: int = raw_config.get("max_health_points", 100)

    # Runtime validation
    if not isinstance(default_health, int) or default_health < 1:
        raise ConfigError(
            f"default_health_points must be positive int, got {default_health}"
        )

    if not isinstance(max_health, int) or max_health < 1:
        raise ConfigError(f"max_health_points must be positive int, got {max_health}")

    if default_health > max_health:
        raise ConfigError(
            f"default_health_points ({default_health}) cannot exceed "
            f"max_health_points ({max_health})"
        )

    return PlayerConfig(
        default_health_points=default_health,
        max_health_points=max_health,
    )
