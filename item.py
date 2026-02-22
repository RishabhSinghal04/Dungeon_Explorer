from typing import Optional
from interfaces import IItem, IWeapon, IHealingItem


class Item(IItem):
    def __init__(
        self,
        name: str,
        cost_price: float = 0.0,
        selling_price: Optional[float] = None,
        stackable: bool = False,
        max_stack: int = 1,
    ):
        self._name = name
        self._cost_price = cost_price
        self._selling_price = (
            selling_price if selling_price is not None else self._cost_price / 2
        )
        self._stackable = stackable
        self._max_stack = max_stack

    def get_name(self) -> str:
        return self._name

    def get_cost_price(self) -> float:
        return self._cost_price

    def get_selling_price(self) -> float:
        return self._selling_price

    def is_stackable(self) -> bool:
        return self._stackable

    def get_max_stack(self) -> int:
        return self._max_stack

    def get_description(self) -> str:
        return f"{self._name}"

    def __eq__(self, other):
        return isinstance(other, Item) and self._name.lower() == other._name.lower()

    def __hash__(self):
        return hash(self._name.lower())


class Weapon(Item, IWeapon):
    def __init__(self, name, attack_points: int = 0, cost_price: float = 0.0):
        super().__init__(
            name,
            cost_price=cost_price,
            selling_price=cost_price / 2,
            stackable=False,
            max_stack=1,
        )
        self._attack_points = attack_points

    def get_attack_points(self) -> int:
        return self._attack_points

    def get_description(self):
        return (
            super().get_description() + f" -> Attack Points: {self.get_attack_points()}"
        )


class HealingItem(Item, IHealingItem):
    def __init__(
        self, name, health_points: int = 0, cost_price: float = 0.0, max_stack: int = 2
    ):
        super().__init__(
            name,
            cost_price=cost_price,
            selling_price=cost_price / 2,
            stackable=True,
            max_stack=max_stack,
        )
        self._health_points = health_points

    def get_health_points(self) -> int:
        return self._health_points

    def get_description(self):
        return (
            super().get_description() + f" -> Healing Points: {self.get_health_points()}"
        )
