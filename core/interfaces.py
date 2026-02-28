from typing import Protocol, Optional, runtime_checkable
from dataclasses import dataclass


class IOutputHandler(Protocol):
    """
    Interface for handling output operations.
    Provides a contract for displaying text to the user,
    allowing different implementations (CLI, GUI, logging).
    """

    def display(self, text: str, separator: str = "\n") -> None: ...


@runtime_checkable
class IItem(Protocol):
    """
    Base interface for all items in the game.
    Items can be stackable, have costs, and provide descriptions.
    """

    @property
    def name(self) -> str: ...
    @property
    def stackable(self) -> bool: ...
    @property
    def max_stack(self) -> int: ...
    @property
    def cost_price(self) -> float: ...
    @property
    def selling_price(self) -> float: ...
    @property
    def description(self) -> str: ...


@runtime_checkable
class IWeapon(IItem, Protocol):
    """
    Interface for weapon items.
    Extends IItem with attack points.
    """

    @property
    def attack_points(self) -> int: ...


@runtime_checkable
class IHealingItem(IItem, Protocol):
    """
    Interface for healing items.
    Extends IItem with health restoration points.
    """

    @property
    def health_points(self) -> int: ...


@dataclass
class InventorySlot:
    """
    Represents a slot in the inventory.
    Each slot has an index, an item, and a quantity.
    """

    index: int
    item: IItem
    quantity: int


class IInventoryStorage(Protocol):
    """
    Low-level slot operations/
    Handles adding, removing, and querying items in slots.
    """

    def add_item(self, item: IItem, quantity: int = 1) -> int: ...

    # def get_unadded_items(self, item: IItem, quantity: int = 1) -> int: ...
    # def try_add_item(self, item: IItem, quantity: int = 1) -> int: ...
    def find_item(self, item_name: str) -> Optional[IItem]: ...
    def peek_item(self, slot_index: int) -> Optional[IItem]: ...
    def is_full(self) -> bool: ...
    def list_items(self) -> list[InventorySlot]: ...
    def get_items_with_quantity(self) -> list[tuple[IItem, int]]: ...
    def count_item(self, item_name: str) -> int: ...
    def remove_item(
        self,
        slot_index: Optional[int] = None,
        item_name: Optional[str] = None,
        quantity: int = 1,
    ) -> tuple[Optional[IItem], int]: ...


class IInventoryManager(Protocol):
    """
    User-facing inventory operations.
    Provides higher-level methods for viewing descriptions,
    retrieving specific item types, and listing unique items.
    """

    def view_description(self, item_name: str) -> str: ...
    def get_weapon(self, weapon_name: str) -> Optional[IWeapon]: ...
    def get_healing_item(self, healing_item_name: str) -> Optional[IHealingItem]: ...
    def get_unique_items(self) -> list[IItem]: ...


class IInventory(Protocol):
    """
    Facade combinig storage + manager.
    Provides unified access to both low-level slot operations
    and user-facing inventory management.
    """

    @property
    def storage(self) -> IInventoryStorage: ...
    @property
    def manager(self) -> IInventoryManager: ...

    # Storage Operations
    def add_item(self, item: IItem, quantity: int = 1) -> int: ...
    def find_item(self, item_name: str) -> Optional[IItem]: ...
    def peek_item(self, slot_index: int) -> Optional[IItem]: ...
    def is_full(self) -> bool: ...
    def list_items(self) -> list[InventorySlot]: ...
    def get_items_with_quantity(self) -> list[tuple[IItem, int]]: ...
    def count_item(self, item_name: str) -> int: ...
    def remove_item(
        self,
        slot_index: Optional[int] = None,
        item_name: Optional[str] = None,
        quantity: int = 1,
    ) -> tuple[Optional[IItem], int]: ...

    # Manager Operations
    def view_description(self, item_name: str) -> str: ...
    def get_weapon(self, weapon_name: str) -> Optional[IWeapon]: ...
    def get_healing_item(self, healing_item_name: str) -> Optional[IHealingItem]: ...
    def get_unique_items(self) -> list[IItem]: ...


@runtime_checkable
class ICharacter(Protocol):
    """
    Defines the contract for a game character.
    Provides attributes and methods for health management,
    survival checks, and handling damage.
    """

    @property
    def health_points(self) -> int: ...
    def is_alive(self) -> bool: ...
    def take_damage(self, amount: int) -> None: ...


class IEnemy(Protocol):
    """Interface for enemy characters."""

    @property
    def type(self) -> str: ...

    @property
    def health_points(self) -> int: ...

    def is_alive(self) -> bool: ...
    def attack(self, target: ICharacter) -> bool: ...
    def drop_cash(self) -> float: ...
    def take_damage(self, amount: int) -> None: ...


class ICash(Protocol):
    """
    Interface for managing player currency.
    Defines methods for adding, reducing, and checking balance.
    """

    def add_cash(self, amount: float) -> None: ...
    def reduce_cash(self, amount: float) -> None: ...
    def get_balance(self) -> float: ...


class ICombatManager(Protocol):
    """
    Interface for combat management.

    Defines methods for performing attacks, equipping weapons,
    and using healing items.
    """

    @property
    def equipped_weapon(self) -> Optional[IWeapon]: ...
    @equipped_weapon.setter
    def equipped_weapon(self, weapon: Optional[IWeapon]) -> None: ...
    def attack_performed(self, target: ICharacter) -> bool: ...
    def equip_weapon(self, weapon_name: str) -> bool: ...
    def healing_item_used(self, slot_index: int) -> bool: ...


class IPlayer(ICharacter, Protocol):
    """
    Player specific interface composed of cash + inventory.
    Defines player-specific attributes and actions such as
    health management and equipped weapon handling.
    """

    @property
    def name(self) -> str: ...
    @property
    def max_health_points(self) -> int: ...
    def get_equipped_weapon(self) -> Optional[IWeapon]: ...
    def equip_weapon(self, weapon_name: str) -> bool: ...
    def unequip_weapon(self) -> None: ...
    def attack(self, target: ICharacter) -> bool: ...
    def get_health_points(self) -> int: ...
    def use_healing_item(self, index: int) -> bool: ...
    def update_health_points(self, amount: int) -> None: ...

    @property
    def inventory(self) -> IInventory: ...
    @property
    def cash(self) -> ICash: ...


class IMerchantTransaction(Protocol):
    """Interface for merchant transaction operations."""

    def show_items(self, player: IPlayer) -> list[str]: ...
    def show_player_cash(self, player: IPlayer) -> str: ...


class IItemFormatter(Protocol):
    """Interface for formatting items for display."""

    def format_for_purchase(
        self, items: list[IItem], player: IPlayer, max_healing_items: int
    ) -> list[str]: ...
    def format_for_sale(self, items_with_qty: list[tuple[IItem, int]]) -> list[str]: ...
