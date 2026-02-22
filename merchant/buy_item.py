from typing import Optional
from dataclasses import dataclass

from merchant.merchant import Merchant
from interfaces import IItem, IWeapon, IHealingItem, IPlayer
from merchant.column_widths import ColumnWidths


@dataclass
class PurchaseResult:
    success: bool
    message: str
    item: Optional[IItem] = None


class BuyItem(Merchant):
    def __init__(self, max_healing_item: int = 6):
        super().__init__()
        self._sorted_items_stock: Optional[list[tuple[IItem, int]]] = None
        self.max_healing_item = max_healing_item

    # def __init__(self, items_stock: dict[IItem:int], max_healing_item: int = 6):
    #     self._items_stock = items_stock
    #     self.max_healing_item = max_healing_item

    @property
    def sorted_items_stock(self) -> list[tuple[IItem, int]]:
        if self._sorted_items_stock is None:
            self._sorted_items_stock = sorted(
                self._items_stock.items(),
                key=lambda pair: pair[0].get_max_stack(),
            )
        return self._sorted_items_stock

    def show_items(self, player: IPlayer) -> list[str]:
        items = [item for item, _ in self.sorted_items_stock]
        return self._format_items_for_display(items, player)

    def buy_item(self, item_name: str, player: IPlayer) -> PurchaseResult:
        if self._inventory_full(player):
            return PurchaseResult(False, "Inventory is full")

        item = self._find_item(item_name)
        if not item:
            return PurchaseResult(False, f"{item_name} not found")

        if self._owns_weapon(player, item):
            return PurchaseResult(
                False, f"Not available to buy. You already own {item.get_name()}."
            )

        if self._has_too_many_healing_items(player, item):
            return PurchaseResult(
                False,
                f"Not available to buy. You already have {self.max_healing_item} {item.get_name()}s.",
            )

        if not self._has_enough_cash(player, item):
            return PurchaseResult(False, f"Not enough cash to buy {item.get_name()}")

        return self._process_purchase(player, item)

    def _inventory_full(self, player: IPlayer) -> bool:
        return player.inventory.storage.is_full()

    def _find_item(self, item_name: str) -> Optional[IItem]:
        all_items = self.get_all_items()
        for item in all_items:
            if item.get_name().lower() == item_name.lower():
                return item
        return None

    def _owns_weapon(self, player: IPlayer, item: IItem) -> bool:
        return isinstance(item, IWeapon) and player.inventory.storage.find_item(
            item.get_name()
        )

    def _has_too_many_healing_items(self, player: IPlayer, item: IItem) -> bool:
        return (
            isinstance(item, IHealingItem)
            and player.inventory.storage.count_item(item.get_name())
            >= self.max_healing_item
        )

    def _has_enough_cash(self, player: IPlayer, item: IItem) -> bool:
        return player.cash.get_balance() >= item.get_cost_price()

    def _process_purchase(self, player: IPlayer, item: IItem) -> PurchaseResult:
        cost = item.get_cost_price()
        player.cash.reduce_cash(cost)
        leftover = player.inventory.storage.try_add_item(item, 1)
        if leftover == 0:
            self._items_stock[item] = max(0, self._items_stock[item] - 1)
            return PurchaseResult(
                True, f"Bought {item.get_name()} for {item.get_cost_price()}"
            )
        player.cash.add_cash(cost)
        return PurchaseResult(False, "Inventory is full. Cannot add item.")

    def _format_items_for_display(
        self, items: list[IItem], player: IPlayer
    ) -> list[str]:
        """Format a list of items for display with their stats and price."""
        space = " " * 5
        columns: dict[int, str] = {1: "Name", 2: "Attack/Health Points", 3: "Price"}
        widths = self._calculate_column_widths(items, columns)

        # header
        lines = [
            f"{columns.get(1,"").ljust(widths.name)}{space}"
            f"{columns.get(2,"").center(widths.stat)}{space}"
            f"{columns.get(3,"").rjust(widths.price)}"
        ]
        # rows
        for item in items:
            lines.append(self._format_item_lines(item, player, widths, space))
        return lines

    def _calculate_column_widths(
        self, items: list[IItem], columns: dict[int, str]
    ) -> ColumnWidths:
        name_width = max(
            len(columns.get(1, "")), *(len(item.get_name()) for item in items)
        )
        stat_width = len(columns.get(2, ""))
        price_width = max(
            len(columns.get(3, "")),
            *(len(str(item.get_cost_price())) for item in items),
        )
        return ColumnWidths(name=name_width, stat=stat_width, price=price_width)

    def _format_item_lines(
        self, item: IItem, player: IPlayer, widths: ColumnWidths, space: str
    ) -> str:
        stat_value = "-"
        if isinstance(item, IWeapon):
            stat_value = f"Attack: {item.get_attack_points()}"
        elif isinstance(item, IHealingItem):
            stat_value = f"Health: {item.get_health_points()}"
        line = (
            f"{item.get_name().ljust(widths.name)}  "
            f"{stat_value.center(widths.stat)}{space}"
            f"{str(item.get_cost_price()).rjust(widths.price)}{space}"
        )
        if isinstance(item, IWeapon) and player.inventory.storage.find_item(
            item.get_name()
        ):
            line += space + "Own"
        elif (
            isinstance(item, IHealingItem)
            and player.inventory.storage.count_item(item.get_name())
            >= self.max_healing_item
        ):
            line += space + "Enough"
        return line
