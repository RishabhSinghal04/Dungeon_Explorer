from interfaces import ICash


class CashManager(ICash):
    def __init__(self, starting_cash: float = 0.0):
        self.cash = starting_cash

    def add_cash(self, amount: float) -> None:
        self.cash += amount

    def reduce_cash(self, amount: float) -> None:
        self.cash = max(0, self.cash - amount)

    def get_balance(self) -> float:
        return self.cash
