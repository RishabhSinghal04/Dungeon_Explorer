from interfaces import IItem, IWeapon, IHealingItem, IPlayer
from all_items import all_items


class Merchant:
    def __init__(self):
        self._items_stock: dict[IItem, int] = self._initialize_stock()

    def show_player_cash(self, player: IPlayer) -> str:
        return f"{player.cash.get_balance()}"

    def get_all_items(self) -> dict[IItem, int]:
        return self._items_stock

    # def exit_deal(self) -> str:
    #     return "exit"

    def _initialize_stock(self):
        stock: dict[IItem, int] = {}
        for item in all_items:
            if isinstance(item, IWeapon):
                stock[item] = 1
            elif isinstance(item, IHealingItem):
                stock[item] = 6
        return stock
