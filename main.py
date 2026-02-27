from input_output import UserInputHandler, ConsoleOutputHandler
from ui.menu import GameMenu


def main() -> None:
    input_handler = UserInputHandler()
    output_handler = ConsoleOutputHandler()
    output_handler.display("Dungeon Explorer")
    menu = GameMenu(input_handler, output_handler)
    menu.main_menu()


if __name__ == "__main__":
    main()
