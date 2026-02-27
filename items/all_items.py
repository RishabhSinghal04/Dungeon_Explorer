from items.item import Weapon, HealingItem

spear = Weapon(name="Spear", attack_points=30, cost_price=2000)
poleaxe = Weapon("Poleaxe", attack_points=50, cost_price=4400)
sword = Weapon("Sword", attack_points=40, cost_price=3600)
mace = Weapon("Mace", attack_points=35, cost_price=2800)

herb = HealingItem("Herb", health_points=50, cost_price=800)

all_items = [spear, poleaxe, sword, mace, herb]
