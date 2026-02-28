from core.interfaces import IOutputHandler
from characters.player import IPlayer
from input_output.user_input import UserInputHandler


class GameContext:
    def __init__(
        self,
        player: IPlayer,
        input_handler: UserInputHandler,
        output_handler: IOutputHandler,
    ) -> None:
        self.player: IPlayer = player
        self.input_handler: UserInputHandler = input_handler
        self.output_handler: IOutputHandler = output_handler
