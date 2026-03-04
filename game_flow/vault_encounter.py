from abc import ABC, abstractmethod

from core.interfaces import IHealingItem, IEnemy

from game_flow.encounter_result import EncounterResult
from game_flow.game_context import GameContext
from game_flow.combat import Combat
from game_flow.inventory_operations import InventoryOperations

from ui.emoji import EmojiType, format_with_emoji
from ui.confirmation import confirm_action


class VaultContent(ABC):
    """Base class for vault contents."""

    @abstractmethod
    def resolve(self, context: GameContext) -> EncounterResult:
        """Resolve the encounter."""
        pass


class ItemContent(VaultContent):
    """Vault containing a healing item."""

    def __init__(self, item: IHealingItem) -> None:
        self._item: IHealingItem = item

    def resolve(self, context: GameContext) -> EncounterResult:
        """Handle finding a healing item."""
        context.output_handler.display(
            format_with_emoji(
                f"You found a {self._item.display_name()}. Take?", EmojiType.HERB
            ),
        )

        while True:
            choice: bool = confirm_action(context.input_handler)
            if not choice:
                context.output_handler.display("You left the item.")
                break
            if not context.player.inventory.storage.is_full():
                self._add_item(context)
                break

            context.output_handler.display("Inventory is full.")
            InventoryOperations(context).inventory_operations()

        return EncounterResult.SUCCESS

    def _add_item(self, context: GameContext) -> None:
        context.player.inventory.storage.add_item(self._item, 1)
        message: str = f"{self._item.display_name()} added to inventory."

        context.output_handler.display(format_with_emoji(message, EmojiType.GREEN_TICK))


class CashContent(VaultContent):
    """Vault containing cash."""

    def __init__(self, amount: float) -> None:
        self.amount: float = amount

    def resolve(self, context: GameContext) -> EncounterResult:
        """Handle finding cash."""
        context.output_handler.display(
            format_with_emoji(f"You found {self.amount}.", EmojiType.COIN)
        )
        context.player.cash.add_cash(self.amount)
        return EncounterResult.SUCCESS


class EnemyContent(VaultContent):
    """Vault containing an enemy."""

    def __init__(self, enemy: IEnemy) -> None:
        self.enemy: IEnemy = enemy

    def resolve(self, context: GameContext) -> EncounterResult:
        return Combat(self.enemy, context).start()


class VaultEncounter:
    def __init__(self, content: VaultContent, context: GameContext) -> None:
        self.content: VaultContent = content
        self.context: GameContext = context

    def resolve(self) -> EncounterResult:
        """Resolve the vault encounter."""
        return self.content.resolve(self.context)
