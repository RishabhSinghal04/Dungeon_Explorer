from core.interfaces import IItem
from merchant import BuyItem, SellItem
from items.item import Item, Weapon, HealingItem
from game_flow.game_context import GameContext

from merchant.buy_item import PurchaseResult
from merchant.sell_item import SaleResult
from merchant.item_formatter import ItemFormatter

from ui.show_options import show_options
from ui.emoji import EMOJIS


class MerchantInteraction:
    def __init__(self, context: GameContext) -> None:
        self.context: GameContext = context
        self.coin_emoji: str = EMOJIS.get("coin", "")

    def interact(self) -> None:
        self.context.output_handler.display("")
        options: dict[str, str] = {"1": "Talk", "0": "Exit"}
        self.context.output_handler.display("-> Merchant:-")
        while True:
            show_options(options, " " * len(options))
            choice: str = self.context.input_handler.get_action(
                "Select an option: ", options
            )
            return None if choice == "0" else self.talk()

    def talk(self) -> None:
        options: dict[str, str] = {"1": "Buy", "2": "Sell", "0": "Exit"}
        while True:
            show_options(options, " " * len(options))
            choice: str = self.context.input_handler.get_action(
                "Select an option: ", options
            )
            if choice == "0":
                break
            if choice == "1":
                self._buy()
            else:
                self._sell()

    def _buy(self) -> None:
        buy_item = BuyItem(ItemFormatter())

        self.context.output_handler.display(
            f"{self.coin_emoji}  Cash: {buy_item.show_player_cash(self.context.player)}"
        )
        lines: list[str] = buy_item.show_items(self.context.player)
        self.context.output_handler.display(
            "\n".join(
                f"{index}. {line}" if index > 0 else "   " + line
                for index, line in enumerate(lines)
            )
        )

        items: list[tuple[IItem, int]] = buy_item.sorted_items_stock
        total_items: int = len(items)
        buyable_items: dict[str, Item] = {}
        for index, (item, _) in enumerate(items, start=1):
            owned_weapon: bool = (
                isinstance(item, Weapon)
                and item in self.context.player.inventory.manager.get_unique_items()
            )
            maxed_healing_item: bool = (
                isinstance(item, HealingItem)
                and self.context.player.inventory.storage.count_item(item.name)
                >= buy_item._max_healing_item
            )
            if not (owned_weapon and maxed_healing_item):
                buyable_items[str(index)] = item

        if not buyable_items:
            self.context.output_handler.display("No items to buy.")
            return

        choice: str = self.context.input_handler.get_action(
            f"Select an item (1-{total_items}): ", buyable_items
        )
        selected_item: Item = buyable_items[choice]
        result: PurchaseResult = buy_item.buy_item(
            selected_item.name, self.context.player
        )
        self.context.output_handler.display(result.message)

    def _sell(self):
        sell_item = SellItem()
        items: list[tuple[IItem, int]] = (
            self.context.player.inventory.storage.get_items_with_quantity()
        )

        self.context.output_handler.display(
            f"{self.coin_emoji}  Cash: {sell_item.show_player_cash(self.context.player)}"
        )
        lines: list[str] = sell_item.show_items(self.context.player)
        self.context.output_handler.display(
            "\n".join(
                f"{index}. {line}" if index > 0 else "   " + line
                for index, line in enumerate(lines)
            )
        )

        total_items: int = len(items)
        sellable_items: dict[str, Item] = {}
        for index, (item, qty) in enumerate(items, start=1):
            sellable_items[str(index)] = item

        if not sellable_items:
            self.context.output_handler.display("No items to sell.")
            return

        choice: str = self.context.input_handler.get_action(
            f"Select an item (1-{total_items}): ", sellable_items
        )
        selected_item: Item = sellable_items[choice]

        try:
            max_qty: int = self.context.player.inventory.storage.count_item(
                selected_item.name
            )
            quantity = int(
                self.context.input_handler.get_int(
                    f"Enter quantity to sell " f"(max {max_qty}): ", 1, max_qty
                )
            )
        except ValueError as e:
            self.context.output_handler.display(str(e))
            return

        result: SaleResult = sell_item.sell_item(
            selected_item.name, self.context.player, quantity
        )
        if (
            isinstance(result.item, Weapon)
            and result.item == self.context.player.get_equipped_weapon()
        ):
            self.context.player.unequip_weapon()
        (
            self.context.output_handler.display("Sold")
            if result
            else self.context.output_handler.display("Cannot Sold")
        )
