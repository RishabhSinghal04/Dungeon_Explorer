class Character:
    def __init__(self, health_points: int):
        self._health_points = health_points

    @property
    def health_points(self) -> int:
        return self._health_points
    
    @health_points.setter
    def health_points(self, value: int) -> None:
        self._health_points = value

    def is_alive(self) -> bool:
        return self._health_points > 0

    def take_damage(self, amount: int) -> None:
        self._health_points = max(0, self._health_points - amount)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(HP={self._health_points})"
