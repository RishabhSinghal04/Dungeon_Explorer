from input_output.user_input import UserInputHandler
from input_output.key_maps import Confirmation, CONFIRMATION_KEY_MAP
from ui.show_options import show_options


def confirm_action(
    input_handler: UserInputHandler, message: str = "Select an option: "
) -> bool:
    """
    Prompt user for Yes/No confirmation.

    Args:
        input_handler: For user input.
        message: Optional custom prompt message.

    Returns:
        bool: True if user selected Yes, False if No.
    """
    show_options(CONFIRMATION_KEY_MAP, " " * len(CONFIRMATION_KEY_MAP))
    choice: str = input_handler.get_action(message, CONFIRMATION_KEY_MAP)
    return choice == Confirmation.YES.value
