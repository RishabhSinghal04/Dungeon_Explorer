from typing import Optional

from core.interfaces import IItem, IWeapon, IItemFormatter

from game_flow.game_context import GameContext
from game_flow.inventory_operations import InventoryOperations

from merchant.merchant import Merchant
from merchant.transaction_results import PurchaseResult, SaleResult
from merchant.buy_item import BuyItem
from merchant.sell_item import SellItem
from merchant.item_formatter import ItemFormatter

from input_output.key_maps import (
    MerchantAction,
    TradeAction,
    MERCHANT_KEY_MAP,
    TRADE_KEY_MAP,
)
from ui.confirmation import confirm_action
from ui.show_options import show_options
from ui.emoji import EmojiType, format_with_emoji


class MerchantInteraction:
    """Handles merchant trade interactions."""

    def __init__(
        self, context: GameContext, formatter: Optional[IItemFormatter] = None
    ) -> None:
        """
        Initialize merchant interaction.

        Args:
            context: Game context with player and handlers.
        """
        self._context: GameContext = context
        self._merchant = Merchant()
        self._formatter: IItemFormatter = formatter or ItemFormatter()
        self._buy_service = BuyItem(self._formatter)
        self._sell_service = SellItem(self._formatter)

    def interact(self) -> None:
        self._context.output_handler.display("")
        self._context.output_handler.display("-> Merchant:-")

        while True:
            show_options(MERCHANT_KEY_MAP, " " * len(MERCHANT_KEY_MAP))
            choice: str = self._context.input_handler.get_action(
                "Select an option: ", MERCHANT_KEY_MAP
            )
            if choice == MerchantAction.EXIT.value:
                if confirm_action(self._context.input_handler):
                    break
            elif choice == MerchantAction.TALK.value:
                self._talk()
            elif choice == MerchantAction.INVENTORY.value:
                InventoryOperations(self._context).inventory_operations()

    def _talk(self) -> None:
        while True:
            show_options(TRADE_KEY_MAP, " " * len(TRADE_KEY_MAP))
            choice: str = self._context.input_handler.get_action(
                "Select an option: ", TRADE_KEY_MAP
            )

            if choice == TradeAction.EXIT.value:
                break
            elif choice == TradeAction.BUY.value:
                self._buy()
            elif choice == TradeAction.SELL.value:
                self._sell()

    def _buy(self) -> None:
        while True:
            self._context.output_handler.display("")
            self._context.output_handler.display("-> Buy:-")

            items_and_qty: list[tuple[IItem, int]] = self._buy_service.get_sorted_stock(
                self._context.player
            )
            if not items_and_qty:
                self._context.output_handler.display("No items available to buy.")
                return

            lines: list[str] = self._buy_service.show_items(self._context.player)
            self._show_cash()
            self._display_items(lines, items_and_qty)

            buyable_items: dict[str, IItem] = self._build_item_dict(items_and_qty, True)
            if not buyable_items:
                self._context.output_handler.display("All items are unavailable.")
                return

            total_items: int = len(items_and_qty)
            selected_item: Optional[IItem] = self._get_item_selection(
                buyable_items, total_items, "buy"
            )
            if not selected_item:
                return

            result: PurchaseResult = self._buy_service.buy_item(
                selected_item.name, self._context.player
            )
            self._context.output_handler.display(result.message)

    def _sell(self) -> None:
        while True:
            self._context.output_handler.display("")
            self._context.output_handler.display("-> Sell:-")

            items_with_qty: list[tuple[IItem, int]] = (
                self._context.player.inventory.storage.get_items_with_quantity()
            )
            if not items_with_qty:
                self._context.output_handler.display("No items to sell")
                return

            lines: list[str] = self._sell_service.show_items(self._context.player)
            self._show_cash()
            self._display_items(lines, items_with_qty)

            sellable_items: dict[str, IItem] = self._build_item_dict(
                items_with_qty, False
            )

            total_items: int = len(items_with_qty)
            selected_item: Optional[IItem] = self._get_item_selection(
                sellable_items, total_items, "sell"
            )
            if not selected_item:
                return

            max_qty: int = self._context.player.inventory.count_item(selected_item.name)
            quantity: Optional[int] = self._get_sell_quantity(max_qty)
            if quantity is None:
                return

            result: SaleResult = self._sell_service.sell_item(
                self._context.player, selected_item.name, quantity
            )
            self._handle_weapon_unequip(result)
            self._display_result(result)

    def _show_cash(self) -> None:
        cash_text: str = format_with_emoji(
            f"Cash: {self._merchant.show_player_cash(self._context.player)}",
            EmojiType.COIN,
        )
        self._context.output_handler.display(cash_text)

    def _display_items(
        self, lines: list[str], items: list[tuple[IItem, int]], border_char="."
    ) -> None:
        headings: str = self._formatter.format_headings(items)
        border: str = (border_char + " ") * (len(lines[0]) // 2)
        space: str = " " * (2 + len(str(len(items))))

        formatted_lines: str = f"{space}{headings}\n{border}\n"
        formatted_lines += "\n".join(
            f"{index}. {line}" for index, line in enumerate(lines, start=1)
        )

        formatted_lines += "\n" + border
        self._context.output_handler.display(formatted_lines)

    def _build_item_dict(
        self, items_with_qty: list[tuple[IItem, int]], only_available: bool = False
    ) -> dict[str, IItem]:
        """
        Build dict mapping index to item.

        Args:
            items_with_qty: List of (item, quantity) tuples.
            only_available: If True, only include items with qty > 0.

        Returns:
            Dict mapping string index to item.
        """
        result: dict[str, IItem] = {}
        for index, (item, qty) in enumerate(items_with_qty, start=1):
            if not only_available or qty > 0:
                result[str(index)] = item

        return result

    def _get_item_selection(
        self, items: dict[str, IItem], total_items: int, action: str
    ) -> Optional[IItem]:
        """
        Get user's item selection.

        Args:
            items: Dict mapping index to item.
            action: Action name for prompt ("buy" or "sell").

        Returns:
            Selected item or None if user cancels.
        """
        valid_choices: dict[str, str] = {"0": "back"}
        for index in items.keys():
            valid_choices[index] = f"item_{index}"

        prompt: str = f"Select item to {action} (1-{total_items}) or 0 to go back: "
        choice: str = self._context.input_handler.get_action(prompt, valid_choices)
        return None if choice == "0" else items[choice]

    def _get_sell_quantity(self, max_qty: int) -> Optional[int]:
        """
        Get quantity to sell from user.

        Args:
            max_qty: Maximum quantity available.

        Returns:
            Quantity to sell, or None if user cancels.
        """
        try:
            prompt: str = f"Enter quantity to sell " f"(0-{max_qty}): "
            quantity: int = self._context.input_handler.get_int(prompt, 0, max_qty)
            return None if quantity == 0 else quantity
        except ValueError as e:
            self._context.output_handler.display(str(e))
            return

    def _handle_weapon_unequip(self, result: SaleResult) -> None:
        """
        Unequip weapon if player sold their equipped weapon.

        Args:
            result: Sale transaction result.
        """
        if not result.success or not result.item:
            return

        if isinstance(result.item, IWeapon):
            equipped: Optional[IWeapon] = self._context.player.get_equipped_weapon()
            if equipped and result.item.name == equipped.name:
                self._context.player.unequip_weapon()

    def _display_result(self, result: SaleResult, border_char="*") -> None:
        text: str = result.message
        border: str = border_char * len(text)
        text_for_display: str = f"{border}\n{text}\n{border}"
        self._context.output_handler.display(text_for_display)
