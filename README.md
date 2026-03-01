# 🗡️ Dungeon Explorer

A terminal-based RPG adventure game where you battle enemies, collect loot, and survive through increasingly challenging dungeon levels. Built with Python and designed with clean architecture principles.

## 🎮 Game Overview

Dungeon Explorer is a text-based dungeon crawler where you navigate through 4 dangerous levels, each filled with crypts containing enemies, treasures, and healing items. Make strategic decisions about which crypts to enter, manage your inventory wisely, and trade with merchants between levels to maximize your chances of defeating the final boss.

### Key Features

- **4 Progressive Levels**: Each level increases in difficulty with unique enemy encounters
- **Dynamic Combat System**: Strategic turn-based combat with weapon management
- **Inventory Management**: Collect, equip, and use items strategically
- **Merchant Trading**: Buy powerful weapons and sell unwanted items between levels
- **Multiple Difficulty Modes**: Choose between Medium and Hard difficulty settings
- **Rich Visual Feedback**: Emoji-enhanced UI for better gaming experience
- **Boss Battles**: Face mini-bosses at the end of each level and a final boss showdown

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- No external dependencies required (uses only Python standard library)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/RishabhSinghal04/Dungeon_Explorer.git
cd Dungeon_Explorer
```

2. Run the game:
```bash
python main.py
```

That's it! The game runs entirely in your terminal.

## 🎯 How to Play

### Game Flow

1. **Start Menu**: Choose to start a new game, read about the game, or exit
2. **Character Creation**: Enter your character name and select difficulty
3. **Level Exploration**: 
   - Each level has 9 crypts to explore
   - Choose which crypt to enter (numbered 1-9)
   - Press `i` anytime to check your inventory
   - Press `0` to exit the game
4. **Combat**: When encountering enemies, choose to:
   - Attack with your equipped weapon
   - Open inventory to equip different weapons or use healing items
   - Exit the game
5. **Merchant Trading**: After clearing all crypts, visit the merchant to:
   - Buy powerful weapons and healing items
   - Sell items you no longer need
6. **Boss Battle**: Defeat the level boss to progress
7. **Victory**: Survive all 4 levels and defeat the final boss to win!

### Controls

- **Main Game**: `1-9` (select crypt), `i` (inventory), `0` (exit)
- **Combat**: `1` (attack), `2` (inventory), `0` (exit)
- **Inventory**: `1` (equip/use), `2` (view description), `3` (discard), `0` (back)
- **Merchant**: `1` (buy), `2` (sell), `0` (exit)

## 🏗️ Architecture

The project follows SOLID principles and clean architecture patterns:

```
Dungeon_Explorer/
├── characters/           # Player and enemy classes
│   ├── factories/       # Factory pattern for character creation
│   └── managers/        # Combat and cash management
├── config/              # Game configuration and enums
├── core/                # Core interfaces and protocols
├── game_flow/           # Game state and flow management
├── input_output/        # User input/output handling
├── inventory/           # Inventory system (storage, manager, facade)
├── items/               # Item definitions and factories
├── loaders/             # Configuration file loaders
├── merchant/            # Trading system
└── ui/                  # User interface and display formatting
```

### Design Patterns Used

- **Factory Pattern**: For creating players, enemies, and items
- **Facade Pattern**: Inventory system combines storage and management
- **Protocol Pattern**: Interface-based design for flexibility and testability
- **Strategy Pattern**: Different enemy behaviors and item types

### Key Design Principles

- ✅ **SOLID Principles**: Single Responsibility, Open/Closed, Dependency Inversion
- ✅ **DRY**: Don't Repeat Yourself - shared logic extracted into reusable components
- ✅ **Interface Segregation**: Small, focused protocols for different concerns
- ✅ **Type Safety**: Full type hints with Protocol-based interfaces
- ✅ **Separation of Concerns**: Clear boundaries between game logic, UI, and data

## 🎲 Game Mechanics

### Combat System

- Turn-based combat where you alternate attacks with enemies
- Weapon determines your attack damage
- No weapon = no ability to attack
- Healing items restore health during combat

### Inventory System

- Limited inventory space (configurable slots)
- Stackable items (healing items) vs. non-stackable (weapons)
- Only one weapon can be equipped at a time
- Items can be discarded to make room for better loot

### Economy

- Earn cash by defeating enemies
- Items have both purchase and selling prices (50% resale value)
- Limited weapon stock at merchants (1 per weapon type)
- Strategic decisions: save cash or buy powerful weapons early?

### Difficulty Scaling

- **Medium**: Balanced challenge for most players
- **Hard**: Increased enemy stats and reduced resources

## 🛠️ Configuration

Game settings can be modified in the `config/` directory:

- `game.json`: Total levels, inventory keys
- `enemies.json`: Enemy stats per difficulty level
- `player.json`: Starting player stats
- `merchant.json`: Shop inventory and prices (can be extended)

## 🔧 Development

### Code Quality

- Full type hints throughout codebase
- Protocol-based interfaces for testability
- Comprehensive docstrings
- Modular, maintainable architecture

### Testing

The architecture supports easy testing through dependency injection and interface-based design:

```python
# Example: Testing with mock objects
mock_output = MockOutputHandler()
mock_input = MockInputHandler(["1", "1", "0"])
game = Game("TestPlayer", Difficulty.MEDIUM, mock_output, mock_input)
```

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:

- 🐛 Report bugs or gameplay issues
- 💡 Suggest new features or game mechanics
- 🎨 Improve UI/UX
- 📝 Enhance documentation
- 🧪 Add tests

Please ensure your code follows the existing architecture patterns and includes type hints.

## 📝 License

This project is open source and available under the MIT License.

## 🎓 Learning Outcomes

This project demonstrates:

- Advanced OOP concepts in Python
- Design patterns and architectural principles
- Type safety with Protocols
- Clean code practices
- Game development fundamentals
- CLI application development

## 👨‍💻 Author

**Rishabh Singhal**

- GitHub: [@RishabhSinghal04](https://github.com/RishabhSinghal04)

## 🙏 Acknowledgments

- Inspired by classic roguelike dungeon crawlers
- Built as a learning project to demonstrate clean architecture in Python
- Emoji support for enhanced terminal experience

---

**Enjoy your adventure in the dungeons! May your blade stay sharp and your health potions plentiful.** ⚔️🛡️
