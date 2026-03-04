from typing import TypedDict, Any, cast

from characters.enemy import EnemyStats
from config.game_config import Difficulty

from core.config_loader import ConfigError, load_json_config


class EnemyStatsDict(TypedDict):
    health_points: int
    attack_points: int
    cash_drop: float


def load_enemy_config(
    path: str = "config/enemies.json",
) -> dict[str, dict[str, EnemyStats]]:
    """
    Load enemy configuration from JSON file.

    Args:
        path: Path to enemies config file.

    Returns:
        dict mapping enemy type to difficulty to EnemyStats.
        Structure: {enemy_type: {difficulty: EnemyStats}}

    Raises:
        ConfigError: If config cannot be loaded or is invalid.
    """
    raw_config = load_json_config(path)
    if not isinstance(raw_config, dict):
        raise ConfigError(f"Invalid config format: expected dict at top level.")

    result: dict[str, dict[str, EnemyStats]] = {}
    for enemy_type, difficulties in raw_config.items():
        if not isinstance(enemy_type, str):
            raise ConfigError(f"Invalid enemy type key: {enemy_type}")
        if not isinstance(difficulties, dict):
            raise ConfigError(
                f"Invalid format for enemy type '{enemy_type}': expected dict."
            )

        parsed = _parse_difficulties(enemy_type, difficulties)
        result[enemy_type] = parsed
    return result


def _parse_difficulties(
    enemy_type: str, difficulties: dict[str, Any]
) -> dict[str, EnemyStats]:
    """
    Parse difficulty levels for an enemy type.

    Args:
        enemy_type: Name of the enemy type.
        difficulties: dict mapping difficulty to stats.

    Returns:
        dict mapping difficulty string to EnemyStats.

    Raises:
        ConfigError: If difficulty data is invalid.
    """
    parsed: dict[str, EnemyStats] = {}
    for difficulty, stats in difficulties.items():
        if not isinstance(difficulty, str):
            raise ConfigError(f"Invalid difficulty key for {enemy_type}: {difficulty}")
        if not isinstance(stats, dict):
            raise ConfigError(
                f"Invalid stats format for {enemy_type}/{difficulty}: expected dict."
            )

        enemy_stats: EnemyStats = _parse_stats(enemy_type, difficulty, stats)
        parsed[difficulty] = enemy_stats
    return parsed


def _parse_stats(enemy_type: str, difficulty: str, stats: dict[str, Any]) -> EnemyStats:
    """
    Parse enemy stats from raw JSON data.

    Args:
        enemy_type: Name of the enemy type.
        difficulty: Difficulty level string.
        stats: Raw stats dict from JSON.

    Returns:
        EnemyStats dataclass with validated data.

    Raises:
        ConfigError: If stats are invalid or missing required fields.
    """
    try:
        if "health_points" not in stats:
            raise ConfigError(f"Missing 'health_points' for {enemy_type}/{difficulty}")
        if "attack_points" not in stats:
            raise ConfigError(f"Missing 'attack_points' for {enemy_type}/{difficulty}")
        if "cash_drop" not in stats:
            raise ConfigError(f"Missing 'cash_drop' for {enemy_type}/{difficulty}")

        health_points = stats["health_points"]
        attack_points = stats["attack_points"]
        cash_drop = stats["cash_drop"]

        if not isinstance(health_points, int) or health_points < 1:
            raise ConfigError(
                f"health_points must be positive int for {enemy_type}/{difficulty}, "
                f"got {health_points}"
            )

        if not isinstance(attack_points, int) or attack_points < 0:
            raise ConfigError(
                f"attack_points must be non-negative int for {enemy_type}/{difficulty}, "
                f"got {attack_points}"
            )

        if not isinstance(cash_drop, (int, float)) or cash_drop < 0:
            raise ConfigError(
                f"cash_drop must be non-negative number for {enemy_type}/{difficulty}, "
                f"got {cash_drop}"
            )

        try:
            difficulty_enum = Difficulty(difficulty)
        except ValueError:
            valid_difficulties: list[str] = [d.value for d in Difficulty]
            raise ConfigError(
                f"Invalid difficulty '{difficulty}' for {enemy_type}. "
                f"Valid values: {valid_difficulties}"
            )

        return EnemyStats(
            type=enemy_type,
            difficulty=difficulty_enum,
            health_points=health_points,
            attack_points=attack_points,
            cash_drop=float(cash_drop),
        )

    except ConfigError:
        # Re-raise ConfigErrors as-is
        raise
    except Exception as e:
        # Catch any other unexpected errors
        raise ConfigError(
            f"Failed to parse enemy config for {enemy_type}/{difficulty}: {e}"
        ) from e
