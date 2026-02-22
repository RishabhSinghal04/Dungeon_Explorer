from typing import Optional
from dataclasses import dataclass

@dataclass
class ColumnWidths:
    name: int
    stat: Optional[int] = None
    quantity: Optional[int] = None
    price: int = 0
