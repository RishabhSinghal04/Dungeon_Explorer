from typing import Optional
from dataclasses import dataclass

from core.interfaces import IItem


@dataclass
class TransactionResult:
    """Base result for all merchant transactions."""

    success: bool
    message: str


@dataclass
class PurchaseResult:
    """Result of a purchase transaction."""

    success: bool
    message: str
    item: Optional[IItem] = None


@dataclass
class SaleResult:
    """Result of a sale transaction."""

    success: bool
    message: str
    item: Optional[IItem] = None
    quantity: int = 0
    cash_earned: float = 0.0
