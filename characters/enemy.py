from dataclasses import dataclass

from core.interfaces import ICharacter, IEnemy
from characters.character import Character

from config.game_config import Difficulty


@dataclass
class EnemyStats:
    """Represents stats for an enemy type at a given difficulty."""

    type: str
    difficulty: Difficulty
    health_points: int
    attack_points: int
    cash_drop: float


class Enemy(Character, IEnemy):
    """Enemy character with attack and cash drop attributes."""

    def __init__(self, stats: EnemyStats) -> None:
        super().__init__(stats.health_points)
        self._type: str = stats.type
        self._difficulty: Difficulty = stats.difficulty
        self._attack_points: int = stats.attack_points
        self._cash_drop: float = stats.cash_drop

    @property
    def type(self) -> str:
        return self._type

    def drop_cash(self) -> float:
        return self._cash_drop

    def attack(self, target: ICharacter) -> bool:
        """Direct attack always succeeds."""
        target.take_damage(self._attack_points)
        return True

    def __repr__(self) -> str:
        return f"Enemy(type={self._type}, difficulty={self._difficulty}, HP={self.health_points}, ATK={self._attack_points}, cash_drop={self._cash_drop})"
