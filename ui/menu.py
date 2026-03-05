from typing import Callable

from core.interfaces import IOutputHandler
from config.game_config import Difficulty, MenuKey
from input_output.user_input import UserInputHandler
from game_flow.game import Game
from config.game_config import GameConfig
from core.config_loader import ConfigError

from ui.show_options import show_options


class MenuOption:
    """Represents a single menu option with a key, label, and action."""

    def __init__(self, key: str, label: str, action: Callable[[], None]) -> None:
        self.key: str = key
        self.label: str = label
        self.action: Callable[[], None] = action


class GameMenu:
    def __init__(
        self,
        input_handler: UserInputHandler,
        output_handler: IOutputHandler,
        default_difficulty: Difficulty = Difficulty.MEDIUM,
    ) -> None:
        self._player_name: str = ""
        self._difficulty: Difficulty = default_difficulty
        self._input_handler: UserInputHandler = input_handler
        self._output_handler: IOutputHandler = output_handler

    def main_menu(self) -> None:
        options: list[MenuOption] = [
            MenuOption(MenuKey.START.value, "start_game", self._name_menu),
            MenuOption(MenuKey.ABOUT.value, "about", self._about_game),
            MenuOption(MenuKey.EXIT.value, "exit", lambda: None),
        ]

        formatted_options: dict[str, str] = self._format_options(options)
        while True:
            show_options(formatted_options)
            choice: str = self._get_user_choice(formatted_options)
            if not self._handle_choice(choice, options):
                return

    def _about_game(self) -> None:
        self._output_handler.display("-> About Game:-")
        self._output_handler.display(
            "The game has 4 levels, ending with a final boss fight."
        )
        self._output_handler.display("Each level has 5 vaults and one boss at the end.")
        self._output_handler.display(
            "Before each boss, you can visit the merchant to buy or sell items."
        )
        self._output_handler.display("Game Controls:")
        self._output_handler.display(" - Press 1-5 to enter a vault.")
        self._output_handler.display(" - Press 'i' to check your inventory.")
        self._output_handler.display(" - Press '0' to quit your current game.")

        option: dict[str, str] = {MenuKey.BACK.value: "back"}
        self._input_handler.get_action("0. Back to Menu: ", option)

    def _name_menu(self) -> None:
        options: list[MenuOption] = [
            MenuOption(MenuKey.START.value, "name", self._set_player_name),
            MenuOption(MenuKey.BACK.value, "back", lambda: None),
        ]

        formatted_options: dict[str, str] = self._format_options(options)
        show_options(formatted_options)
        choice: str = self._get_user_choice(formatted_options)
        self._handle_choice(choice, options)

    def _select_difficulty(self) -> None:
        """Display difficulty selection menu."""
        difficulty_map: dict[str, Difficulty] = {
            str(index): difficulty
            for index, difficulty in enumerate(Difficulty, start=1)
        }
        options: dict[str, str] = {
            key: value.name.lower() for key, value in difficulty_map.items()
        }
        options["0"] = "back"

        show_options(options)
        choice: str = self._get_user_choice(options)
        if choice == MenuKey.BACK.value:
            return

        self._difficulty: Difficulty = difficulty_map.get(choice, self._difficulty)
        try:
            self._start_game()
        except ConfigError as e:
            self._output_handler.display(
                "Cannot start game due to configuration error:"
            )
            self._output_handler.display(f"  {e}")
            self._output_handler.display("Returning to main menu...")

    def _get_user_choice(self, options: dict[str, str]) -> str:
        return self._input_handler.get_action("Enter your choice: ", options)

    def _handle_choice(self, choice: str, options: list[MenuOption]) -> bool:
        """
        Execute action for chosen option.

        Returns:
            bool: False if exit selected, True otherwise.
        """
        for opt in options:
            if choice == opt.key:
                opt.action()
                return choice != MenuKey.EXIT.value
        return True

    def _format_options(self, options: list[MenuOption]) -> dict[str, str]:
        """Format menu options for display."""
        return {opt.key: opt.label for opt in options}

    def _set_player_name(self) -> None:
        self._player_name: str = self._input_handler.get_string("Enter your name: ")
        self._select_difficulty()

    def _start_game(self) -> None:
        """
        Initialize and start the game.

        Raises:
            ConfigError: If game configuration cannot be loaded
        """
        game = Game(
            self._player_name,
            self._difficulty,
            self._output_handler,
            self._input_handler,
            GameConfig(),
        )
        game.start()
