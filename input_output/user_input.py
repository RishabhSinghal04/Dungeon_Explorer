import sys
from typing import Callable, Optional

from interfaces import IOutputHandler
from input_output.display_output import ConsoleOutputHandler

try:
    import winsound
except ImportError:
    winsound = None


class UserInputHandler:
    def __init__(
        self,
        input_func: Callable[[str], str] = input,
        output_handler: Optional[IOutputHandler] = None,
    ):
        self.input_func = input_func
        self.output_handler = output_handler or ConsoleOutputHandler()

    def get_action(self, prompt: str, key_map: dict[str, str]) -> str:
        """
        Prompt the user until they enter a valid key from the given key_map.

        Args:
            prompt (str): Message shown to the user.
            key_map (dict[str, str]): Mapping of valid keys to actions.

        Returns:
            str: The valid key chosen by the user (normalized to lowercase).
        """
        valid_keys = list(key_map.keys())
        return self._get_validated_input(
            prompt,
            lambda v: v.lower() if v and v.lower() in valid_keys else None,
            "Invalid Input! Valid Key(s): " + ", ".join(valid_keys),
        )

    def get_int(
        self, prompt: str, min_value: int = 1, max_value: Optional[int] = None
    ) -> int:
        """
        if max_value is
        Prompt the user until they enter a valid integer within the given range.

        Args:
            prompt (str): Message shown to the user.
            min_value (int): Minimum value of the range.
            max_value (int): Maximum value of the range.

        Returns:
            int: The valid integer value chosen by the user.

        Raise:
            ValueError: If max_value is less than min_value.
        """
        if max_value is not None and max_value < min_value:
            raise ValueError(
                f"Invalid range: max_value ({max_value}) cannot be less than min_value ({min_value})."
            )
        return self._get_validated_input(
            prompt,
            lambda v: (
                v
                if v.isdigit() and min_value <= int(v) <= (max_value or int(v))
                else None
            ),
            f"Invalid Input! Please enter a number in range {min_value}-{max_value if max_value else {"\u221E"}}.",
        )

    def get_string(self, prompt: str, num_of_chars: int = 12) -> str:
        """
        Prompt the user until they enter a non-empty string.

        Args:
            prompt (str): Message shown to the user.
            num_of_chars (int): Maximum allowed length for the input string (default: 12).

        Returns:
            str: A valid non-empty string entered by the user.
        """
        return self._get_validated_input(
            prompt,
            lambda v: v if v and len(v) <= num_of_chars else None,
            f"Invalid Input! Please enter a non-empty string with at most {num_of_chars} characters.",
            use_strip=True,
        )

    # ___internal helpers___
    def _get_validated_input(
        self,
        prompt: str,
        validator: Callable[[str], Optional[str]],
        error_message: str,
        use_strip: bool = False,
    ) -> str:
        """
        Internal helper: repeatedly prompt until validator returns a non-None value.
        If use_strip=True, input is trimmed before validation.
        Displays error_message once if input is invalid.
        """
        show_invalid = False
        while True:
            raw_value = self.input_func(prompt)
            if use_strip:
                raw_value = raw_value.strip()
            result = validator(raw_value)
            if result is not None:
                return result
            self._beep()
            if not show_invalid:
                self.output_handler.display(error_message)
                show_invalid = True

    def _beep(self) -> None:
        # winsound.Beep(1000, 300)
        if winsound:
            winsound.MessageBeep()
        else:
            sys.stdout.write("\a")
            sys.stdout.flush()
