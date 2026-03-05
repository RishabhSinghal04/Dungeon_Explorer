from core.interfaces import IEnemy
from characters.enemy import Enemy, EnemyStats
from config.game_config import EnemyType, Difficulty

from core.config_loader import ConfigError


class EnemyFactory:
    def __init__(self, config: dict[str, dict[str, EnemyStats]]) -> None:
        self._config: dict[str, dict[str, EnemyStats]] = config

    def create(self, enemy_type: EnemyType, difficulty: Difficulty) -> IEnemy:
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
            available: list[str] = list(self._config.keys())
            raise ConfigError(
                f"Enemy '{enemy_type.value}' with difficulty '{difficulty.value}' "
                f"not found in config. Available types: {available}"
            )
