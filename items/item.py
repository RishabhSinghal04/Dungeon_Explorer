from typing import Optional

from core.interfaces import IItem


class Item(IItem):

    DEFAULT_SELLING_RATIO: float = 0.5

    def __init__(
        self,
        name: str,
        cost_price: float = 0.0,
        selling_price: Optional[float] = None,
        stackable: bool = False,
        max_stack: int = 1,
    ) -> None:
        self._name: str = name
        self._cost_price: float = cost_price
        self._selling_price: float = (
            selling_price
            if selling_price is not None
            else self._cost_price * self.DEFAULT_SELLING_RATIO
        )
        self._stackable: bool = stackable
        self._max_stack: int = max_stack

    @property
    def name(self) -> str:
        return self._name

    @property
    def cost_price(self) -> float:
        return self._cost_price

    @property
    def selling_price(self) -> float:
        return self._selling_price

    @property
    def stackable(self) -> bool:
        return self._stackable

    @property
    def max_stack(self) -> int:
        return self._max_stack

    @property
    def description(self) -> str:
        return f"{self.display_name()}"

    def display_name(self) -> str:
        return self._name.replace("_", " ").title()

    def __eq__(self, other: object) -> bool:
        """Items are equal if they have the same name (case-insensitive)."""
        if not isinstance(other, Item):
            return NotImplemented
        return self._name.lower() == other._name.lower()

    def __hash__(self) -> int:
        """Hash based on lowercase name for use in sets/dicts."""
        return hash(self._name.lower())

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return (
            f"{self.__class__.__name__}(name={self._name!r}, cost={self._cost_price})"
        )


class Weapon(Item):
    def __init__(
        self,
        name: str,
        attack_points: int = 0,
        cost_price: float = 0.0,
        selling_price: Optional[float] = None,
    ) -> None:
        super().__init__(
            name,
            cost_price=cost_price,
            selling_price=selling_price,
            stackable=False,
            max_stack=1,
        )
        self._attack_points: int = attack_points

    @property
    def attack_points(self) -> int:
        return self._attack_points

    @property
    def description(self) -> str:
        return super().description + f" -> Attack: {self.attack_points}"


class HealingItem(Item):
    def __init__(
        self,
        name: str,
        health_points: int = 0,
        cost_price: float = 0.0,
        selling_price: Optional[float] = None,
    ) -> None:
        super().__init__(
            name,
            cost_price=cost_price,
            selling_price=selling_price,
            stackable=True,
            max_stack=2,
        )
        self._health_points: int = health_points

    @property
    def health_points(self) -> int:
        return self._health_points

    @property
    def description(self) -> str:
        return super().description + f" -> Heals: {self.health_points} Health Points"
