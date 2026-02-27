from dataclasses import dataclass

from core.interfaces import ICharacter
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


class Enemy(Character):
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

    # if enemy_type not in enemy_config:
    # if difficulty not in enemy_config[enemy_type]:
    # health_points, attack_points, cash_drop = enemy_config[enemy_type][difficulty]
    # return Enemy(health_points, attack_points, cash_drop)


# # (Health Points, Attack Points, Cash Drop)
# enemy_config = {
#     "regular": {"medium": (80, 10, 400.0), "hard": (90, 10, 400.0)},
#     "mini_boss": {"medium": (120, 20, 800.0), "hard": (130, 20, 800.0)},
#     "boss": {"medium": (180, 30, 1200.0), "hard": (190, 30, 1200.0)},
#     "final_boss": {"medium": (230, 40, 800.0), "hard": (240, 40, 2000.0)},
# }

# class Regular(Enemy):
#     def __init__(self, difficulty: str = "medium"):
#         health_points, attack_points, cash_drop = ENEMY_CONFIG["Regular"][difficulty]
#         super().__init__(health_points, attack_points, cash_drop)


# class MiniBoss(Enemy):
#     def __init__(self, difficulty: str = "medium"):
#         health_points, attack_points, cash_drop = ENEMY_CONFIG["Mini Boss"][difficulty]
#         super().__init__(health_points, attack_points, cash_drop)


# class Boss(Enemy):
#     def __init__(self, difficulty: str = "medium"):
#         health_points, attack_points, cash_drop = ENEMY_CONFIG["Boss"][difficulty]
#         super().__init__(health_points, attack_points, cash_drop)


# class FinalBoss(Enemy):
#     def __init__(self, difficulty: str = "medium"):
#         health_points, attack_points, cash_drop = ENEMY_CONFIG["Final Boss"][difficulty]
#         super().__init__(health_points, attack_points, cash_drop)


# class Regular(Enemy):
#     def __init__(self, difficulty: str = "medium"):
#         if difficulty not in ENEMY_CONFIG["Regular"]:
#             raise ValueError(f"Invalid difficulty: {difficulty}")
#         health_points, attack_points, cash_drop = ENEMY_CONFIG["Regular"][difficulty]
#         super().__init__(health_points, attack_points, cash_drop)
