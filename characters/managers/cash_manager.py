from core.interfaces import ICash


class CashManager(ICash):
    def __init__(self, starting_cash: float = 0.0) -> None:
        self.cash: float = starting_cash

    def add_cash(self, amount: float) -> None:
        self.cash += amount

    def reduce_cash(self, amount: float) -> None:
        self.cash = max(0, self.cash - amount)

    def get_balance(self) -> float:
        return self.cash
