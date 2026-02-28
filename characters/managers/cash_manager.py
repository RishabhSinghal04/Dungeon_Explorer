from core.interfaces import ICash


class CashManager(ICash):
    def __init__(self, cash: float = 0.0) -> None:
        self._cash: float = cash

    def add_cash(self, amount: float) -> None:
        self._cash += amount

    def reduce_cash(self, amount: float) -> None:
        self._cash = max(0, self._cash - amount)

    def get_balance(self) -> float:
        return self._cash
