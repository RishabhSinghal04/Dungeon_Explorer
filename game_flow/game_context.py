from characters.player import Player
from input_output.user_input import UserInputHandler
from input_output.display_output import ConsoleOutputHandler


class GameContext:
    def __init__(
        self,
        player: Player,
        input_handler: UserInputHandler,
        output_handler: ConsoleOutputHandler,
    ):
        self.player = player
        self.input_handler = input_handler
        self.output_handler = output_handler
