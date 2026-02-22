import random

from .player import PlayerFactory
from game_flow.vault_encounter import VaultEncounter
from game_flow.game_context import GameContext
from input_output.user_input import UserInputHandler
from input_output.display_output import ConsoleOutputHandler
from game_flow.combat import Combat
from game_flow.level_runner import LevelRunner

from .player import build_player_status
from characters.enemy import create_enemy


class Game:
    def __init__(self, player_name: str, difficulty: str = "medium"):
        self.input_handler = UserInputHandler()
        self.output_handler = ConsoleOutputHandler()
        self.player = PlayerFactory.create_player(player_name)
        self.context = GameContext(self.player, self.input_handler, self.output_handler)
        self.difficulty = difficulty

    def start(self) -> None:
        input_chars: list[str] = ["i", "I"]
        context = GameContext(self.player, self.input_handler, self.output_handler)

        self.output_handler.display(
            f"{self.player.name} selected {self.difficulty.capitalize()} difficulty"
        )
        levels = {
            index: VaultAssigner(self.difficulty, self.context).assign_vaults
            for index in range(1, 5)
        }

        for level_num, vaults_func in levels.items():
            runner = LevelRunner(level_num, self.difficulty, vaults_func(), context)
            result = runner.run(input_chars)
            if result <= 0:
                return

        Combat(create_enemy("final_boss", self.difficulty), context).start()
        self.output_handler.display(build_player_status(self.player))


class VaultAssigner:
    def __init__(self, difficulty: str, context: GameContext):
        self.difficulty = difficulty
        self.context = context

    def assign_vaults(self) -> dict[int, VaultEncounter]:
        healing_item = PlayerFactory.get_one_healing_item()
        CASH = 1000

        encounters = (
            [create_enemy("regular", self.difficulty) for _ in range(4)]
            + [healing_item for _ in range(2)]
            + [CASH] * 2
            + [create_enemy("mini_boss", self.difficulty)]
        )

        random.shuffle(encounters)
        # context = GameContext(self.player, self.input_handler, self.output_handler)

        return {
            index + 1: VaultEncounter(encounters[index], self.context)
            for index in range(len(encounters))
        }
