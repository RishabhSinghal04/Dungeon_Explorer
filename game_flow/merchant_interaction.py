from core.interfaces import IItem, IWeapon, IHealingItem

from game_flow.game_context import GameContext

from merchant.buy_item import PurchaseResult
from merchant.sell_item import SaleResult
from merchant.buy_item import BuyItem
from merchant.sell_item import SellItem
from merchant.item_formatter import ItemFormatter

from ui.show_options import show_options
from ui.emoji import EmojiType, format_with_emoji


class MerchantInteraction:
    def __init__(self, context: GameContext) -> None:
        self._context: GameContext = context

    def interact(self) -> None:
        self._context.output_handler.display("")
        options: dict[str, str] = {"1": "talk", "i": "inventory", "0": "exit"}
        self._context.output_handler.display("-> Merchant:-")
        while True:
            show_options(options, " " * len(options))
            choice: str = self._context.input_handler.get_action(
                "Select an option: ", options
            )
            return None if choice == "0" else self.talk()

    def talk(self) -> None:
        options: dict[str, str] = {"1": "buy", "2": "sell", "0": "exit"}
        while True:
            show_options(options, " " * len(options))
            choice: str = self._context.input_handler.get_action(
                "Select an option: ", options
            )
            if choice == "0":
                break
            if choice == "1":
                self._buy()
            else:
                self._sell()

    def _buy(self) -> None:
        formatter = ItemFormatter()
        buy_service = BuyItem(formatter)

        cash_text: str = format_with_emoji(
            f"Cash: {buy_service.show_player_cash(self._context.player)}",
            EmojiType.COIN,
        )
        self._context.output_handler.display(cash_text)

        lines: list[str] = buy_service.show_items(self._context.player)
        formatted_lines: str = "\n".join(
            f"{index}. {line}" if index > 0 else "   " + line
            for index, line in enumerate(lines)
        )
        self._context.output_handler.display(formatted_lines)

        items: list[tuple[IItem, int]] = buy_service.sorted_items_stock
        buyable_items: dict[str, IItem] = {}
        valid_choices: dict[str, str] = {}

        for index, (item, _) in enumerate(items, start=1):
            owned_weapon: bool = (
                isinstance(item, IWeapon)
                and item in self._context.player.inventory.get_unique_items()
            )
            maxed_healing_item: bool = (
                isinstance(item, IHealingItem)
                and self._context.player.inventory.count_item(item.name)
                >= buy_service._max_healing_item
            )
            if not (owned_weapon or maxed_healing_item):
                buyable_items[str(index)] = item
                valid_choices[str(index)] = f"item_{index}"

        if not buyable_items:
            self._context.output_handler.display("No items to buy.")
            return

        choice: str = self._context.input_handler.get_action(
            f"Select an item (1-{len(items)}): ", valid_choices
        )
        selected_item: IItem = buyable_items[choice]
        result: PurchaseResult = buy_service.buy_item(
            selected_item.name, self._context.player
        )
        self._context.output_handler.display(result.message)

    def _sell(self) -> None:
        formatter = ItemFormatter()
        sell_service = SellItem(formatter)

        cash_text: str = format_with_emoji(
            f"Cash: {sell_service.show_player_cash(self._context.player)}",
            EmojiType.COIN,
        )
        self._context.output_handler.display(cash_text)

        items: list[tuple[IItem, int]] = (
            self._context.player.inventory.storage.get_items_with_quantity()
        )

        lines: list[str] = sell_service.show_items(self._context.player)
        self._context.output_handler.display(
            "\n".join(
                f"{index}. {line}" if index > 0 else "   " + line
                for index, line in enumerate(lines)
            )
        )

        sellable_items: dict[str, IItem] = {}
        valid_choices: dict[str, str] = {}
        for index, (item, qty) in enumerate(items, start=1):
            sellable_items[str(index)] = item
            valid_choices[str(index)] = f"item_{index}"

        if not sellable_items:
            self._context.output_handler.display("No items to sell.")
            return

        choice: str = self._context.input_handler.get_action(
            f"Select an item (1-{len(items)}): ", valid_choices
        )
        selected_item: IItem = sellable_items[choice]

        try:
            max_qty: int = self._context.player.inventory.count_item(selected_item.name)
            quantity = int(
                self._context.input_handler.get_int(
                    f"Enter quantity to sell " f"(max {max_qty}): ", 1, max_qty
                )
            )
        except ValueError as e:
            self._context.output_handler.display(str(e))
            return

        result: SaleResult = sell_service.sell_item(
            selected_item.name, self._context.player, quantity
        )
        if (
            isinstance(result.item, IWeapon)
            and result.item == self._context.player.get_equipped_weapon()
        ):
            self._context.player.unequip_weapon()

        (
            self._context.output_handler.display("Sold")
            if result
            else self._context.output_handler.display("Cannot Sold")
        )
