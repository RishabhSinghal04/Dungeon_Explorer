import random
from typing import Optional

from core.interfaces import IHealingItem
from characters.factories.enemy_factory import EnemyFactory

from game_flow.vault_encounter import (
    VaultContent,
    VaultEncounter,
    ItemContent,
    CashContent,
    EnemyContent,
)
from game_flow.game_context import GameContext

from config.game_config import LevelConfig, Difficulty, EnemyType

from items.item_factory import get_random_healing_item


class VaultAssigner:
    """Handles assignment of encounters to vaults (Single Responsibility)."""

    def __init__(
        self,
        difficulty: Difficulty,
        enemy_config: dict,
        context: GameContext,
        level_config: Optional[LevelConfig] = None,
    ) -> None:
        self._difficulty: Difficulty = difficulty
        self._enemy_config: dict = enemy_config
        self._context: GameContext = context
        self._level_config: LevelConfig = level_config or LevelConfig()

    def assign_vaults(self) -> dict[int, VaultEncounter]:
        """
        Generate randomized vault encounters for a level.

        Returns:
            dict mapping vault number to VaultEncounter.
        """
        contents: list[VaultContent] = self._generate_encounters()
        random.shuffle(contents)

        return {
            vault_num: VaultEncounter(content, self._context)
            for vault_num, content in enumerate(contents, start=1)
        }

    def _generate_encounters(self) -> list[VaultContent]:
        """Generate list of encounters based on level config."""
        config: LevelConfig = self._level_config
        contents: list[VaultContent] = []

        factory = EnemyFactory(self._enemy_config)
        contents.extend(
            [
                EnemyContent(factory.create(EnemyType.REGULAR, self._difficulty))
                for _ in range(config.regular_enemies)
            ]
        )

        healing_item: Optional[IHealingItem] = get_random_healing_item()
        if healing_item:
            contents.extend(
                [ItemContent(healing_item) for _ in range(config.healing_items)]
            )

        contents.extend(
            [CashContent(config.cash_amount) for _ in range(config.cash_rewards)]
        )

        if config.has_mini_boss:
            contents.append(
                EnemyContent(factory.create(EnemyType.MINI_BOSS, self._difficulty))
            )

        return contents
