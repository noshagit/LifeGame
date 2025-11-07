# Advanced Game of Life - Implementation Guide

## Project Structure

```
game_of_life/
├── config.py          # Global configuration and constants
├── terrain.py         # Terrain and environment management
├── species.py         # Species definitions and parameters
├── creature.py        # Individual creature logic and AI
├── simulation.py      # Main simulation manager
├── visualizer.py      # Tkinter-based visualization
├── main.py           # Entry point
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Installation

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** Not all packages in `requirements.txt` are required for basic functionality. For minimal setup (GUI only):

```bash
pip install numpy scipy Pillow matplotlib
```

## Usage

### Graphical Mode (Default)

Run the simulation with visual interface:

```bash
python main.py
```

**Controls:**
- **Start/Pause**: Toggle simulation running
- **Step**: Advance one tick manually
- **Reset**: Restart with new random terrain
- **Space**: Play/Pause shortcut
- **Esc**: Quit application

### Headless Mode

Run without graphics for data collection:

```bash
python main.py --headless --ticks 5000
```

This will simulate 5000 ticks and display statistics every 100 ticks.

### Benchmark Mode

Test performance:

```bash
python main.py --benchmark --ticks 1000
```

### Command Line Options

```bash
python main.py [OPTIONS]

Options:
  --headless          Run without GUI
  --benchmark         Run performance benchmark
  --width WIDTH       Grid width (default: 100)
  --height HEIGHT     Grid height (default: 100)
  --ticks TICKS       Number of ticks for headless mode (default: 1000)
  --quiet             Suppress periodic statistics
  -h, --help          Show help message
```

### Examples

```bash
# Large grid with GUI
python main.py --width 200 --height 200

# Long headless simulation
python main.py --headless --ticks 10000 --quiet

# Performance test on large grid
python main.py --benchmark --width 150 --height 150 --ticks 2000
```

## Features Implemented

### |Core Systems
- **Terrain Generation**: Multiple terrain types (plains, forests, water, mountains)
- **Plant Growth**: Dynamic vegetation system
- **Energy & Metabolism**: Creatures consume energy and food
- **Movement System**: Speed influenced by terrain and creature state
- **Vision & Perception**: Creatures detect food and threats within range
- **Hunting & Predation**: Carnivores and omnivores hunt prey
- **Reproduction**: Age-based mating with offspring
- **Aging & Death**: Natural lifespan and starvation mechanics
- **Social Behavior**: Species-specific social structures

### |Species Implemented
1. **Herbivore #1** - Fast, small herbivore with high reproduction
2. **Herbivore #2** - Large herd animal with defensive behavior
3. **Omnivore #1** - Opportunistic hunter and forager
4. **Carnivore #1** - Solitary ambush predator

### 🔄 Advanced Features (Framework Ready)
- Flight mechanics (framework in place, not fully implemented)
- Mutation system (basic implementation)
- Advanced AI behaviors (pathfinding, memory)
- Weather system
- Seasonal changes
- Data export and analysis

## Architecture

### Module Descriptions

**config.py**
- Global constants and configuration
- Terrain types, diet types, social behaviors
- Visual color definitions

**terrain.py**
- `Terrain` class managing the environment grid
- Procedural terrain generation
- Plant growth and consumption

**species.py**
- `SpeciesConfig` dataclass defining all species parameters
- Predefined species configurations
- Species registry for easy access

**creature.py**
- `Creature` class representing individual entities
- AI decision making (survival, reproduction, exploration)
- Movement, hunting, fleeing, and feeding behaviors
- Energy and health management

**simulation.py**
- `Simulation` class orchestrating all components
- Main update loop
- Reproduction handling
- Statistics tracking

**visualizer.py**
- `Visualizer` class using Tkinter
- Real-time rendering of terrain, plants, and creatures
- Control panel with start/pause/step/reset
- Statistics display

**main.py**
- Entry point with command-line interface
- Multiple execution modes (graphical, headless, benchmark)

## Extending the Simulation

### Adding a New Species

Edit `species.py`:

```python
NEW_SPECIES = SpeciesConfig(
    name="new_species",
    maxHealth=50,
    maxEnergy=50,
    metabolism=1.0,
    dietType=DIET_OMNIVORE,
    dietPreferences=[FOOD_PLANTS, FOOD_SMALL_ANIMALS],
    foodCapacity=20,
    starvationTime=150,
    baseSpeed=1.2,
    terrainSpeed={
        TERRAIN_PLAIN: 1.0,
        TERRAIN_FOREST: 0.8,
        TERRAIN_WATER: 0.5,
        TERRAIN_MOUNTAIN: 0.7
    },
    canFly=False,
    visionRange=6,
    visionAngle=270,
    soundPerception=0.6,
    size=10,
    socialBehavior=SOCIAL_GROUP,
    maturityAge=30,
    reproductionCooldown=100,
    litterSize=3,
    aggression=0.3,
    attackPower=7,
    defense=5,
    lifespan=120,
    behavior="flexible"
)

# Add to registry
SPECIES_REGISTRY["new_species"] = NEW_SPECIES
```

Add color to `config.py`:

```python
COLORS = {
    # ... existing colors ...
    "new_species": (150, 75, 200),
}
```

Update initial population in `simulation.py` `_initializeCreatures()`:

```python
initialPopulations = {
    "herbivore_1": 30,
    "herbivore_2": 15,
    "omnivore_1": 10,
    "carnivore_1": 5,
    "new_species": 8,  # Add your species
}
```

### Customizing Behavior

Modify the `_makeDecision()` method in `creature.py` to change AI behavior priorities.

### Adjusting Parameters

Edit `config.py` to change global simulation parameters like grid size, plant spawn rate, or metabolism rates.

## Development Best Practices

### Code Style
- Variables: camelCase (`myVariable`)
- Classes: PascalCase (`MyClass`)
- Constants: UPPER_SNAKE_CASE (`MY_CONSTANT`)
- All code in English
- Comprehensive docstrings

### Testing

Run tests (when implemented):

```bash
pytest tests/
```

### Code Formatting

```bash
# Format code
black *.py

# Check style
flake8 *.py
```

## Performance Considerations

- **Grid Size**: Larger grids increase computation time significantly
- **Population**: More creatures = slower simulation
- **Optimization**: Consider using `numba` JIT compilation for critical loops
- **Headless Mode**: Much faster than graphical mode for large simulations

## Known Limitations

- Flight mechanics defined but not fully implemented
- No save/load functionality yet
- Limited mutation system
- Simple AI behaviors (no pathfinding or learning)
- No weather or seasonal systems yet

## Future Enhancements

- [ ] Complete flight mechanics implementation
- [ ] Advanced pathfinding (A* algorithm)
- [ ] Memory system for creatures
- [ ] Weather and seasonal effects
- [ ] Data export to CSV/HDF5
- [ ] Advanced statistics and graphs
- [ ] Save/load simulations
- [ ] GUI configuration panel
- [ ] Pygame renderer as alternative
- [ ] Multi-threading for performance
- [ ] Genetic algorithm optimization
- [ ] Ecosystem balance analysis tools

## Contributing

This is an educational project implementing the specifications from your README. Feel free to extend and modify as needed!

## License

Open source - use and modify freely for learning and experimentation.