from core.interfaces import IOutputHandler
from characters.player import Player
from input_output.user_input import UserInputHandler


class GameContext:
    def __init__(
        self,
        player: Player,
        input_handler: UserInputHandler,
        output_handler: IOutputHandler,
    ) -> None:
        self.player: Player = player
        self.input_handler: UserInputHandler = input_handler
        self.output_handler: IOutputHandler = output_handler
