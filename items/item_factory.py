import random
from typing import Optional

from core.interfaces import IHealingItem
from items.item import HealingItem
from items.all_items import all_items


@staticmethod
def get_random_healing_item() -> Optional[IHealingItem]:
    healing_items: list[HealingItem] = [
        item for item in all_items if isinstance(item, HealingItem)
    ]
    if healing_items:
        return random.choice(healing_items)
    return None
