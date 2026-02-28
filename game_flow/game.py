from typing import Optional

from core.interfaces import IOutputHandler, IPlayer, IEnemy

from characters.enemy import EnemyStats
from characters.factories.enemy_factory import EnemyFactory
from characters.factories.player_factory import PlayerFactory

from game_flow.vault_encounter import VaultEncounter
from game_flow.game_context import GameContext
from game_flow.combat import Combat
from game_flow.level_runner import LevelRunner
from game_flow.vault_assigner import VaultAssigner

from input_output.user_input import UserInputHandler

from config.game_config import (
    Difficulty,
    GameConfig,
    EnemyType,
    LevelConfig,
    load_game_config,
)

from loaders.enemy_config import load_enemy_config
from ui.build_player_status import build_player_status


class Game:
    def __init__(
        self,
        player_name: str,
        difficulty: Difficulty,
        output_handler: IOutputHandler,
        input_handler: Optional[UserInputHandler] = None,
        game_config: Optional[GameConfig] = None,
    ) -> None:
        self._player: IPlayer = PlayerFactory.create_player(player_name)
        self._difficulty: Difficulty = difficulty

        self.input_handler: UserInputHandler = input_handler or UserInputHandler()
        self.output_handler: IOutputHandler = output_handler

        self._enemy_config: dict[str, dict[str, EnemyStats]] = load_enemy_config()
        self._game_config: GameConfig = game_config or load_game_config()
        self._level_config = LevelConfig()

        self._enemy_factory = EnemyFactory(self._enemy_config)

        self._context = GameContext(
            self._player, self.input_handler, self.output_handler
        )

    @property
    def player(self) -> IPlayer:
        return self._player

    def start(self) -> None:
        """Start and run the game."""
        self.output_handler.display(
            f"{self.player.name} selected {self._difficulty.value.capitalize()} difficulty"
        )

        if not self._run_levels():
            return

        self._run_final_boss()
        self._display_final_status()

    def _run_levels(self) -> bool:
        """Run all game levels. Returns True if player survived."""
        for level_num in range(1, self._game_config.total_levels + 1):
            if not self._run_single_level(level_num):
                return False
        return True

    def _run_single_level(self, level_num: int) -> bool:
        """Run a single level."""
        vaults: dict[int, VaultEncounter] = self._create_vaults_for_level()
        runner = LevelRunner(
            level_num, self._difficulty, vaults, self._context, self._enemy_factory
        )

        result: int = runner.run(self._game_config.inventory_interaction_keys)
        return result > 0

    def _create_vaults_for_level(self) -> dict[int, VaultEncounter]:
        """Create vaults for a level."""
        assigner = VaultAssigner(
            self._difficulty, self._enemy_config, self._context, self._level_config
        )
        return assigner.assign_vaults()

    def _run_final_boss(self) -> None:
        """Run the final boss encounter."""
        final_boss: IEnemy = self._enemy_factory.create(
            EnemyType.FINAL_BOSS, self._difficulty
        )
        Combat(final_boss, self._context).start()

    def _display_final_status(self) -> None:
        """Display final game status."""
        self.output_handler.display(build_player_status(self._player))
