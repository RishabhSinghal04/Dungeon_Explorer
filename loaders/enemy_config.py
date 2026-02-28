from typing import TypedDict

from characters.enemy import EnemyStats
from config.game_config import Difficulty

from core.config_loader import load_json_config


class EnemyStatsDict(TypedDict):
    health_points: int
    attack_points: int
    cash_drop: float


def load_enemy_config(
    path: str = "config/enemies.json",
) -> dict[str, dict[str, EnemyStats]]:
    """Load enemy configuration from JSON file into structured dataclasses."""
    raw_config: dict[str, dict[str, EnemyStatsDict]] = load_json_config(path)
    return {
        enemy_type: {
            difficulty: EnemyStats(
                type=enemy_type,
                difficulty=Difficulty(difficulty),
                health_points=stats["health_points"],
                attack_points=stats["attack_points"],
                cash_drop=stats["cash_drop"],
            )
            for difficulty, stats in difficulties.items()
        }
        for enemy_type, difficulties in raw_config.items()
    }
