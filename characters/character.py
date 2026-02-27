from core.interfaces import ICharacter


class Character(ICharacter):
    def __init__(self, health_points: int) -> None:
        self._health_points: int = health_points

    @property
    def health_points(self) -> int:
        return self._health_points

    @health_points.setter
    def health_points(self, value: int) -> None:
        self._health_points = value

    def is_alive(self) -> bool:
        return self._health_points > 0

    def take_damage(self, amount: int) -> None:
        if amount < 0:
            raise ValueError(f"Damage must be non-negative, got {amount}")
        self._health_points = max(0, self._health_points - amount)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(Health Points = {self._health_points})"
