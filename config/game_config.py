from typing import TypedDict

from enum import Enum
from dataclasses import dataclass, field

from core.config_loader import load_json_config


class Difficulty(Enum):
    MEDIUM = "medium"
    HARD = "hard"


class EnemyType(Enum):
    REGULAR = "regular"
    MINI_BOSS = "mini_boss"
    BOSS = "boss"
    FINAL_BOSS = "final_boss"


class MenuKey(Enum):
    BACK = "0"
    EXIT = "0"
    START = "1"
    ABOUT = "2"


@dataclass
class LevelConfig:
    """Configuration for a single level."""

    regular_enemies: int = 2
    healing_items: int = 1
    cash_rewards: int = 1
    cash_amount: float = 1000.0
    has_mini_boss: bool = True


@dataclass
class GameConfig:
    """Overall game configuration."""

    total_levels: int = 4
    inventory_interaction_keys: list[str] = field(default_factory=lambda: ["i", "I"])


class RawGameConfig(TypedDict, total=False):
    """Raw game config from JSON file."""

    total_levels: int
    inventory_keys: list[str]


def load_game_config(path: str = "config/game.json") -> GameConfig:
    """Load game configuration from JSON file."""
    raw: RawGameConfig = load_json_config(path)
    return GameConfig(
        total_levels=raw.get("total_levels", 4),
        inventory_interaction_keys=raw.get("inventory_keys", ["i", "I"]),
    )
