from characters.enemy import Enemy, EnemyStats
from config.game_config import EnemyType, Difficulty


class EnemyFactory:
    def __init__(self, config: dict[str, dict[str, EnemyStats]]) -> None:
        self._config: dict[str, dict[str, EnemyStats]] = config

    def create(self, enemy_type: EnemyType, difficulty: Difficulty) -> Enemy:
        """
        Create enemy by type and difficulty.

        Args:
            enemy_type: Type of enemy to create.
            difficulty: Game difficulty.

        Returns:
            Enemy instance.

        Raises:
            ValueError: If type/difficulty combination not found.
        """
        try:
            stats: EnemyStats = self._config[enemy_type.value][difficulty.value]
            return Enemy(stats)
        except KeyError:
            raise ValueError(
                f"Unknown enemy type or difficulty: {enemy_type.value}, {difficulty.value}"
                f"Available types: {list(self._config.keys())}"
            )

    def create_form_stats(self, stats: EnemyStats) -> Enemy:
        """Create enemy directly from stats."""
        return Enemy(stats)
