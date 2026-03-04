from core.interfaces import IItem, InventorySlot, IOutputHandler, IPlayer

from ui.emoji import EmojiType, format_with_emoji
from ui.show_options import show_options
from ui.show_player_status import show_player_status

from input_output.key_maps import INVENTORY_KEY_MAP


class InventoryOperationsDisplay:
    def __init__(self, output_handler: IOutputHandler) -> None:
        self._output_handler: IOutputHandler = output_handler

    def empty_inventory(self) -> None:
        self._output_handler.display("Inventory is empty")

    def player_status(self, player: IPlayer):
        show_player_status(player, self._output_handler)

    def show_inventory(self, items: list[InventorySlot]) -> None:
        self._output_handler.display(self._format_inventory(items))

    def format_options(self, INVENTORY_KEY_MAP) -> None:
        show_options(INVENTORY_KEY_MAP, " " * len(INVENTORY_KEY_MAP))

    def show_equiped(self, item: IItem) -> None:
        self._output_handler.display(
            format_with_emoji(f"Equipped {item.display_name()}", EmojiType.WEAPON)
        )

    def show_used(self, item: IItem) -> None:
        self._output_handler.display(
            format_with_emoji(f"Used {item.display_name()}", EmojiType.HERB)
        )

    def show_description(self, item: IItem, border_char="*") -> None:
        border: str = border_char * len(item.description)
        self._output_handler.display(border + "\n" + item.description + "\n" + border)

    def show_discarded(self, item: IItem) -> None:
        self._output_handler.display(
            format_with_emoji(f"Discarded {item.display_name()}", EmojiType.GREEN_TICK)
        )

    def _format_inventory(self, items: list[InventorySlot], border_char="*") -> str:
        text = " INVENTORY "
        space: str = " " * 4
        item_strings: list[str] = [
            f"{index + 1}. {slot.item.display_name()} (x{slot.quantity})"
            for index, slot in enumerate(items)
        ]

        max_item_length: int = max((len(s) for s in item_strings), default=0)
        padded_items: list[str] = [s.ljust(max_item_length) for s in item_strings]
        item_line: str = space.join(padded_items)
        width: int = max(len(item_line), len(text))
        border: str = " " + (border_char + " ") * (width // 2)
        message_part: list[str] = [f"{text:^{width}}", border, item_line, border]
        return "\n".join(message_part)
