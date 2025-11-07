"""
Species module defining creature characteristics and behaviors.

This module contains the SpeciesConfig class that defines all parameters
for different species in the simulation.
"""

from dataclasses import dataclass
from typing import Dict, List
from config import *


@dataclass
class SpeciesConfig:
    """
    Configuration class defining all parameters for a species.
    
    Attributes:
        name (str): Species identifier
        maxHealth (float): Maximum health points
        maxEnergy (float): Maximum energy points
        metabolism (float): Energy consumption per tick
        dietType (str): Type of diet (herbivore, carnivore, omnivore)
        dietPreferences (List[str]): Preferred food types
        foodCapacity (float): Maximum food storage
        starvationTime (int): Ticks before critical vitality loss
        baseSpeed (float): Base movement speed
        terrainSpeed (Dict[str, float]): Speed modifiers per terrain
        canFly (bool): Whether species can fly
        visionRange (int): Visual detection range
        visionAngle (int): Field of view in degrees
        soundPerception (float): Sound/smell detection sensitivity
        size (float): Physical size/mass
        socialBehavior (str): Social structure type
        maturityAge (int): Age for sexual maturity
        reproductionCooldown (int): Ticks between reproductions
        litterSize (int): Number of offspring per reproduction
        aggression (float): Aggression level (0-1)
        attackPower (float): Damage dealt in attacks
        defense (float): Damage reduction
        lifespan (int): Maximum age in ticks
        behavior (str): General behavioral pattern
    """
    
    name: str
    maxHealth: float
    maxEnergy: float
    metabolism: float
    dietType: str
    dietPreferences: List[str]
    foodCapacity: float
    starvationTime: int
    baseSpeed: float
    terrainSpeed: Dict[str, float]
    canFly: bool
    visionRange: int
    visionAngle: int
    soundPerception: float
    size: float
    socialBehavior: str
    maturityAge: int
    reproductionCooldown: int
    litterSize: int
    aggression: float
    attackPower: float
    defense: float
    lifespan: int
    behavior: str


# Predefined species from the README
HERBIVORE_1 = SpeciesConfig(
    name="herbivore_1",
    maxHealth=40,
    maxEnergy=40,
    metabolism=0.8,
    dietType=DIET_HERBIVORE,
    dietPreferences=[FOOD_PLANTS],
    foodCapacity=15,
    starvationTime=120,
    baseSpeed=1.8,
    terrainSpeed={
        TERRAIN_PLAIN: 1.0,
        TERRAIN_FOREST: 0.9,
        TERRAIN_WATER: 0.3,
        TERRAIN_MOUNTAIN: 0.6
    },
    canFly=False,
    visionRange=8,
    visionAngle=270,
    soundPerception=0.7,
    size=1.5,
    socialBehavior=SOCIAL_SOLITARY,
    maturityAge=20,
    reproductionCooldown=60,
    litterSize=4,
    aggression=0.1,
    attackPower=2,
    defense=3,
    lifespan=80,
    behavior="flee, forage, fast_reproduction"
)

HERBIVORE_2 = SpeciesConfig(
    name="herbivore_2",
    maxHealth=120,
    maxEnergy=120,
    metabolism=1.5,
    dietType=DIET_HERBIVORE,
    dietPreferences=[FOOD_PLANTS],
    foodCapacity=60,
    starvationTime=480,
    baseSpeed=0.8,
    terrainSpeed={
        TERRAIN_PLAIN: 1.0,
        TERRAIN_FOREST: 0.6,
        TERRAIN_WATER: 0.4,
        TERRAIN_MOUNTAIN: 0.5
    },
    canFly=False,
    visionRange=5,
    visionAngle=180,
    soundPerception=0.5,
    size=150,
    socialBehavior=SOCIAL_HERD,
    maturityAge=80,
    reproductionCooldown=300,
    litterSize=1,
    aggression=0.2,
    attackPower=10,
    defense=12,
    lifespan=300,
    behavior="group, territorial_defense, migration"
)

OMNIVORE_1 = SpeciesConfig(
    name="omnivore_1",
    maxHealth=60,
    maxEnergy=60,
    metabolism=1.1,
    dietType=DIET_OMNIVORE,
    dietPreferences=[FOOD_SMALL_ANIMALS, FOOD_PLANTS],
    foodCapacity=20,
    starvationTime=200,
    baseSpeed=1.4,
    terrainSpeed={
        TERRAIN_PLAIN: 1.0,
        TERRAIN_FOREST: 1.2,
        TERRAIN_WATER: 0.5,
        TERRAIN_MOUNTAIN: 0.7
    },
    canFly=False,
    visionRange=6,
    visionAngle=270,
    soundPerception=0.8,
    size=8,
    socialBehavior=SOCIAL_SOLITARY,
    maturityAge=40,
    reproductionCooldown=120,
    litterSize=3,
    aggression=0.4,
    attackPower=8,
    defense=6,
    lifespan=150,
    behavior="individual_hunt, opportunistic, food_storage"
)

CARNIVORE_1 = SpeciesConfig(
    name="carnivore_1",
    maxHealth=90,
    maxEnergy=90,
    metabolism=1.3,
    dietType=DIET_CARNIVORE,
    dietPreferences=[FOOD_SMALL_ANIMALS, FOOD_MEDIUM_ANIMALS],
    foodCapacity=25,
    starvationTime=240,
    baseSpeed=1.6,
    terrainSpeed={
        TERRAIN_PLAIN: 0.9,
        TERRAIN_FOREST: 1.1,
        TERRAIN_WATER: 0.3,
        TERRAIN_MOUNTAIN: 0.9
    },
    canFly=False,
    visionRange=7,
    visionAngle=240,
    soundPerception=0.7,
    size=25,
    socialBehavior=SOCIAL_SOLITARY,
    maturityAge=60,
    reproductionCooldown=180,
    litterSize=2,
    aggression=0.5,
    attackPower=12,
    defense=9,
    lifespan=200,
    behavior="ambush, territorial, solitary_hunter"
)

# Species registry for easy access
SPECIES_REGISTRY = {
    "herbivore_1": HERBIVORE_1,
    "herbivore_2": HERBIVORE_2,
    "omnivore_1": OMNIVORE_1,
    "carnivore_1": CARNIVORE_1,
}