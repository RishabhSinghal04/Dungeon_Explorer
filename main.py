import sys

from input_output import UserInputHandler, ConsoleOutputHandler
from ui.menu import GameMenu
from core.config_loader import ConfigError


def main() -> int:
    """
    Main entry point for the game.

    Returns:
        Exit code: 0 for success, 1 for error.
    """
    input_handler = UserInputHandler()
    output_handler = ConsoleOutputHandler()
    output_handler.display(f"{"Dungeon Explorer".center(5)}")
    output_handler.display("")
    try:
        menu = GameMenu(input_handler, output_handler)
        menu.main_menu()
        return 0

    except ConfigError as e:
        output_handler.display("FATAL ERROR: Configuration Problem")
        output_handler.display(f"Error: {e}")
        output_handler.display("Please check your configuration files:")
        output_handler.display("  - config/items.json")
        output_handler.display("  - config/enemies.json")
        output_handler.display("  - config/player.json")
        output_handler.display("  - config/merchant.json")
        output_handler.display("Make sure all files exist and contain valid JSON.")
        return 1

    except KeyboardInterrupt:
        output_handler.display("Game interrupted by user.")
        return 130

    except Exception as e:
        output_handler.display("UNEXPECTED ERROR")
        output_handler.display(f"An unexpected error occurred: {e}")
        output_handler.display("Please report this bug.")
        return 1


if __name__ == "__main__":
    exit_code: int = main()
    sys.exit(exit_code)
