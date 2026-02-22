from input_output.user_input import UserInputHandler
from game_flow.game import Game
from show_options import show_options


class GameMenu:
    def __init__(self):
        self.player_name: str = ""
        self.difficulty: str = "medium"
        self.input_handler = UserInputHandler()

    def main_menu(self) -> None:
        while True:
            options: dict[str, str] = {"1": "start_game", "2": "about", "0": "exit"}
            show_options(options)
            choice = self.input_handler.get_action(self._prompt_for_user(), options)
            if choice == "0":
                return
            elif choice == "1":
                self.name_menu()
            elif choice == "2":
                self.about_game()

    def about_game(self) -> str:
        option: dict[str, str] = {"0": "back"}
        print("Welcome to Dungeon Explorer!")
        print("The game has 4 levels, ending with a final boss fight.")
        print("Each level has 9 crypts and one boss at the end.")
        print("Before each boss, you can visit the merchant to buy or sell items.")
        print("Game Controls:")
        print(" - Press 1-9 to enter a crypt.")
        print(" - Press 'i' to check your inventory.")
        print(" - Press '0' to quit your current game.")
        # return get_user_choice("Press '0' to go back: ", {0: "Back"})
        return self.input_handler.get_action("0. Back to Menu: ", option)

    def name_menu(self) -> None:
        options: dict[str, str] = {"1": "name", "0": "back"}
        show_options(options)
        choice = self.input_handler.get_action(self._prompt_for_user(), options)
        if choice == "0":
            return

        self.player_name = self.input_handler.get_string("Enter your name: ")
        self.select_difficulty()

    def select_difficulty(self) -> None:
        options: dict[str, str] = {"1": "medium", "2": "hard", "0": "back"}
        show_options(options)
        choice = self.input_handler.get_action(self._prompt_for_user(), options)
        if choice == "0":
            return
        self.difficulty = options.get(choice, "medium").lower()
        Game(self.player_name, self.difficulty).start()

    def _prompt_for_user(self) -> str:
        return "Enter your choice: "
