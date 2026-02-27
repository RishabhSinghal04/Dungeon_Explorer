import random
from typing import Optional

from items.all_items import all_items
from items.item import HealingItem


@staticmethod
def get_random_healing_item() -> Optional[HealingItem]:
    healing_items: list[HealingItem] = [
        item for item in all_items if isinstance(item, HealingItem)
    ]
    if healing_items:
        return random.choice(healing_items)
    return None
