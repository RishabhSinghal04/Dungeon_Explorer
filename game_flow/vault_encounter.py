from abc import ABC, abstractmethod

from core.interfaces import IHealingItem, IEnemy

from game_flow.encounter_result import EncounterResult
from game_flow.game_context import GameContext
from game_flow.combat import Combat
from game_flow.inventory_operations import InventoryOperations

from ui.emoji import EmojiType, format_with_emoji
from ui.show_options import show_options


class VaultContent(ABC):
    """Base class for vault contents."""

    @abstractmethod
    def resolve(self, context: GameContext) -> EncounterResult:
        """Resolve the encounter."""
        pass


class ItemContent(VaultContent):
    """Vault containing a healing item."""

    def __init__(self, item: IHealingItem) -> None:
        self.item: IHealingItem = item

    def resolve(self, context: GameContext) -> EncounterResult:
        """Handle finding a healing item."""
        context.output_handler.display(
            format_with_emoji(f"You found a {self.item.name}.", EmojiType.HERB)
        )
        options: dict[str, str] = {"1": "take", "0": "leave"}

        while True:
            show_options(options, " " * len(options))
            choice: str = context.input_handler.get_action(
                "Select an option: ", options
            )
            if choice == "0":
                context.output_handler.display("You left the item.")
                break
            if not context.player.inventory.storage.is_full():
                self._add_item(context)
                break

            context.output_handler.display("Inventory is full.")
            InventoryOperations(context).inventory_operations()

        return EncounterResult.SUCCESS

    def _add_item(self, context: GameContext) -> None:
        context.player.inventory.storage.add_item(self.item)
        context.output_handler.display(
            format_with_emoji(
                f"{self.item.name} added to inventory.", EmojiType.GREEN_TICK
            )
        )


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
