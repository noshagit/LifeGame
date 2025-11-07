"""
Configuration module for the Advanced Game of Life.

This module contains all global constants and configuration parameters
for the simulation environment.
"""

# Environment Configuration
GRID_WIDTH = 100
GRID_HEIGHT = 100
TICK_DURATION = 0.1  # seconds per simulation tick

# Terrain Types
TERRAIN_PLAIN = "plain"
TERRAIN_FOREST = "forest"
TERRAIN_WATER = "water"
TERRAIN_MOUNTAIN = "mountain"

# Diet Types
DIET_HERBIVORE = "herbivore"
DIET_CARNIVORE = "carnivore"
DIET_OMNIVORE = "omnivore"
DIET_SCAVENGER = "scavenger"

# Food Types
FOOD_PLANTS = "plants"
FOOD_SMALL_ANIMALS = "small_animals"
FOOD_MEDIUM_ANIMALS = "medium_animals"
FOOD_CARCASSES = "carcasses"

# Social Behaviors
SOCIAL_SOLITARY = "solitary"
SOCIAL_GROUP = "group"
SOCIAL_PACK = "pack"
SOCIAL_HERD = "herd"

# Simulation Parameters
DEFAULT_PLANT_SPAWN_RATE = 0.01  # probability per cell per tick
PLANT_FOOD_VALUE = 10
CARCASS_DECAY_TIME = 100  # ticks before carcass disappears
REPRODUCTION_MUTATION_RATE = 0.1  # probability of mutation in offspring

# Visual Configuration (for future implementation)
CELL_SIZE = 8
COLORS = {
    "herbivore_1": (100, 200, 100),
    "herbivore_2": (50, 150, 50),
    "omnivore_1": (200, 150, 100),
    "carnivore_1": (200, 50, 50),
    "plant": (0, 255, 0),
    "water": (50, 100, 200),
    "plain": (200, 200, 150),
    "forest": (34, 139, 34),
    "mountain": (128, 128, 128),
}