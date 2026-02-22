from merchant import BuyItem, SellItem
from item import Item, Weapon, HealingItem
from game_flow.game_context import GameContext

from show_options import show_options
from emoji import EMOJIS


class MerchantInteraction:
    def __init__(self, context: GameContext):
        self.context = context
        self.coin_emoji = EMOJIS.get("coin", "")

    def interact(self) -> None:
        self.context.output_handler.display("")
        options: dict[str, str] = {"1": "Talk", "0": "Exit"}
        self.context.output_handler.display("-> Merchant:-")
        while True:
            show_options(options, " " * len(options))
            choice = self.context.input_handler.get_action(
                "Select an option: ", options
            )
            return None if choice == "0" else self.talk()

    def talk(self) -> None:
        options: dict[str, str] = {"1": "Buy", "2": "Sell", "0": "Exit"}
        while True:
            show_options(options, " " * len(options))
            choice = self.context.input_handler.get_action(
                "Select an option: ", options
            )
            if choice == "0":
                break
            if choice == "1":
                self._buy()
            else:
                self._sell()

    def _buy(self):
        buy_item = BuyItem()

        self.context.output_handler.display(
            f"{self.coin_emoji}  Cash: {buy_item.show_player_cash(self.context.player)}"
        )
        lines = buy_item.show_items(self.context.player)
        self.context.output_handler.display(
            "\n".join(
                f"{index}. {line}" if index > 0 else "   " + line
                for index, line in enumerate(lines)
            )
        )

        items = buy_item.sorted_items_stock
        total_items = len(items)
        buyable_items: dict[str, Item] = {}
        for index, (item, _) in enumerate(items, start=1):
            owned_weapon = (
                isinstance(item, Weapon)
                and item in self.context.player.inventory.manager.get_unique_items()
            )
            maxed_healing_item = (
                isinstance(item, HealingItem)
                and self.context.player.inventory.storage.count_item(item.get_name())
                >= buy_item.max_healing_item
            )
            if not (owned_weapon and maxed_healing_item):
                buyable_items[str(index)] = item

        if not buyable_items:
            self.context.output_handler.display("No items to buy.")
            return

        choice = self.context.input_handler.get_action(
            f"Select an item (1-{total_items}): ", buyable_items
        )
        selected_item = buyable_items[choice]
        result = buy_item.buy_item(selected_item.get_name(), self.context.player)
        self.context.output_handler.display(result.message)

    def _sell(self):
        sell_item = SellItem()
        items = self.context.player.inventory.storage.get_items_with_quantity()

        self.context.output_handler.display(
            f"{self.coin_emoji}  Cash: {sell_item.show_player_cash(self.context.player)}"
        )
        lines = sell_item.show_items(self.context.player)
        self.context.output_handler.display(
            "\n".join(
                f"{index}. {line}" if index > 0 else "   " + line
                for index, line in enumerate(lines)
            )
        )

        total_items = len(items)
        sellable_items: dict[str, Item] = {}
        for index, (item, qty) in enumerate(items, start=1):
            sellable_items[str(index)] = item

        if not sellable_items:
            self.context.output_handler.display("No items to sell.")
            return

        choice = self.context.input_handler.get_action(
            f"Select an item (1-{total_items}): ", sellable_items
        )
        selected_item = sellable_items[choice]

        try:
            max_qty = self.context.player.inventory.storage.count_item(
                selected_item.get_name()
            )
            quantity = int(
                self.context.input_handler.get_int(
                    f"Enter quantity to sell " f"(max {max_qty}): ", 1, max_qty
                )
            )
        except ValueError as e:
            self.context.output_handler.display(str(e))
            return

        result = sell_item.item_sold(
            selected_item.get_name(), self.context.player, quantity
        )
        if (
            isinstance(result.item, Weapon)
            and result.item == self.context.player.get_equipped_weapon()
        ):
            self.context.player.combat_manager.equipped_weapon = None
        (
            self.context.output_handler.display("Sold")
            if result
            else self.context.output_handler.display("Cannot Sold")
        )
