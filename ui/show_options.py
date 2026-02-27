def show_options(
    options: dict[str, str], separator: str = "\n", border_char: str = "-"
) -> None:
    """
    Display menu options with border.

    Args:
        options: Mapping of keys to option labels.
        separator: String to separate menu items.
        border_char: Character to use for border.
    """
    menu_text: str = separator.join(
        f"{index}. {format_label(option)}" for index, option in options.items()
    )

    border: str = border_line(menu_text, separator, border_char)
    print(border, menu_text, border, sep="\n")


def format_label(text: str) -> str:
    """Convert underscore-separated text into capitalized words with spaces."""
    return " ".join(word.capitalize() for word in text.split("_"))


def border_line(text: str, separator: str, border_char: str) -> str:
    if separator == "\n":
        lines: list[str] = [line.strip() for line in text.split("\n") if line.strip()]
        return border_char * (len(max(lines, key=len)) + 1)

    return border_char * (len(text) + 1)
