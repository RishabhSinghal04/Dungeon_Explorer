from characters.character import Character

# (Health Points, Attack Points, Cash Drop)
enemy_config = {
    "regular": {"medium": (80, 10, 400.0), "hard": (90, 10, 400.0)},
    "mini_boss": {"medium": (120, 20, 800.0), "hard": (130, 20, 800.0)},
    "boss": {"medium": (180, 30, 1200.0), "hard": (190, 30, 1200.0)},
    "final_boss": {"medium": (230, 40, 800.0), "hard": (240, 40, 2000.0)},
}


class Enemy(Character):
    def __init__(self, health_points: int, attack_points: int, cash_drop: int):
        super().__init__(health_points)
        self.attack_points = attack_points
        self.cash_drop = cash_drop

    def drop_cash(self) -> float:
        return self.cash_drop

    def attack(self, target: Character) -> None:
        target.take_damage(self.attack_points)


def create_enemy(enemy_type: str, difficulty: str = "medium") -> Enemy:
    if enemy_type not in enemy_config:
        raise ValueError(f"Unknown enemy type: {enemy_type}")
    if difficulty not in enemy_config[enemy_type]:
        raise ValueError(f"Invalid difficulty: {difficulty}")
    health_points, attack_points, cash_drop = enemy_config[enemy_type][difficulty]
    return Enemy(health_points, attack_points, cash_drop)


# class Regular(Enemy):
#     def __init__(self, difficulty: str = "medium"):
#         health_points, attack_points, cash_drop = ENEMY_CONFIG["Regular"][difficulty]
#         super().__init__(health_points, attack_points, cash_drop)


# class MiniBoss(Enemy):
#     def __init__(self, difficulty: str = "medium"):
#         health_points, attack_points, cash_drop = ENEMY_CONFIG["Mini Boss"][difficulty]
#         super().__init__(health_points, attack_points, cash_drop)


# class Boss(Enemy):
#     def __init__(self, difficulty: str = "medium"):
#         health_points, attack_points, cash_drop = ENEMY_CONFIG["Boss"][difficulty]
#         super().__init__(health_points, attack_points, cash_drop)


# class FinalBoss(Enemy):
#     def __init__(self, difficulty: str = "medium"):
#         health_points, attack_points, cash_drop = ENEMY_CONFIG["Final Boss"][difficulty]
#         super().__init__(health_points, attack_points, cash_drop)


# class Regular(Enemy):
#     def __init__(self, difficulty: str = "medium"):
#         if difficulty not in ENEMY_CONFIG["Regular"]:
#             raise ValueError(f"Invalid difficulty: {difficulty}")
#         health_points, attack_points, cash_drop = ENEMY_CONFIG["Regular"][difficulty]
#         super().__init__(health_points, attack_points, cash_drop)
