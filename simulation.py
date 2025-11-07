"""
Simulation module managing the game state and main loop.

This module contains the Simulation class that orchestrates all
components of the game.
"""

import numpy as np
from typing import List, Dict
from terrain import Terrain
from creature import Creature
from species import SPECIES_REGISTRY, SpeciesConfig
from config import *


class Simulation:
    """
    Main simulation manager coordinating all game components.
    
    Attributes:
        terrain (Terrain): The environment terrain
        creatures (List[Creature]): All living creatures
        tick (int): Current simulation tick
        statistics (Dict): Statistics tracking
    """
    
    def __init__(self, width: int = GRID_WIDTH, height: int = GRID_HEIGHT):
        """
        Initialize the simulation.
        
        Args:
            width (int): Grid width
            height (int): Grid height
        """
        self.terrain = Terrain(width, height)
        self.creatures: List[Creature] = []
        self.tick = 0
        self.statistics = {
            "population": {},
            "births": 0,
            "deaths": 0,
            "totalCreatures": 0
        }
        
        self._initializeCreatures()
    
    def _initializeCreatures(self):
        """Spawn initial population of creatures."""
        # Spawn initial populations
        initialPopulations = {
            "herbivore_1": 30,
            "herbivore_2": 15,
            "omnivore_1": 10,
            "carnivore_1": 5
        }
        
        for speciesName, count in initialPopulations.items():
            species = SPECIES_REGISTRY[speciesName]
            for _ in range(count):
                x = np.random.randint(0, self.terrain.width)
                y = np.random.randint(0, self.terrain.height)
                self.spawnCreature(species, x, y)
    
    def spawnCreature(self, species: SpeciesConfig, x: float, y: float) -> Creature:
        """
        Spawn a new creature at specified position.
        
        Args:
            species (SpeciesConfig): Species configuration
            x (float): X coordinate
            y (float): Y coordinate
            
        Returns:
            Creature: The newly created creature
        """
        creature = Creature(species, x, y)
        self.creatures.append(creature)
        self.statistics["totalCreatures"] += 1
        return creature
    
    def update(self):
        """Execute one simulation tick."""
        self.tick += 1
        
        # Update terrain (plant growth)
        self.terrain.updatePlants()
        
        # Track reproduction requests
        reproductionPairs = []
        
        # Update all creatures
        for creature in self.creatures:
            if creature.isAlive:
                # Store state before update
                couldReproduce = (creature.age >= creature.species.maturityAge and creature.reproductionCooldown == 0)
                
                creature.update(self.terrain, self.creatures)
                
                # Check if reproduction occurred
                if (couldReproduce and 
                    creature.reproductionCooldown == creature.species.reproductionCooldown):
                    reproductionPairs.append(creature)
        
        # Handle reproductions
        self._handleReproductions(reproductionPairs)
        
        # Remove dead creatures
        deadCount = 0
        aliveCreatures = []
        for creature in self.creatures:
            if creature.isAlive:
                aliveCreatures.append(creature)
            else:
                deadCount += 1
        
        self.creatures = aliveCreatures
        self.statistics["deaths"] += deadCount
        
        # Update statistics
        self._updateStatistics()
    
    def _handleReproductions(self, parents: List[Creature]):
        """
        Create offspring from reproducing parents.
        
        Args:
            parents (List[Creature]): List of creatures that reproduced
        """
        # Group parents by species
        speciesGroups: Dict[str, List[Creature]] = {}
        for parent in parents:
            speciesName = parent.species.name
            if speciesName not in speciesGroups:
                speciesGroups[speciesName] = []
            speciesGroups[speciesName].append(parent)
        
        # Create offspring for each pair
        for speciesName, parentList in speciesGroups.items():
            # Process pairs
            for i in range(0, len(parentList) - 1, 2):
                parent1 = parentList[i]
                
                # Create offspring
                litterSize = parent1.species.litterSize
                for _ in range(litterSize):
                    # Spawn near parents
                    offsetX = np.random.randint(-2, 3)
                    offsetY = np.random.randint(-2, 3)
                    x = parent1.x + offsetX
                    y = parent1.y + offsetY
                    
                    # Keep within bounds
                    x = max(0, min(self.terrain.width - 1, x))
                    y = max(0, min(self.terrain.height - 1, y))
                    
                    offspring = self.spawnCreature(parent1.species, x, y)
                    self.statistics["births"] += 1
                    
                    # Apply mutations (simplified for now)
                    if np.random.random() < REPRODUCTION_MUTATION_RATE:
                        offspring.health = min(offspring.species.maxHealth,
                                              offspring.health * np.random.uniform(0.9, 1.1))
    
    def _updateStatistics(self):
        """Update population statistics."""
        populationCount: Dict[str, int] = {}
        
        for creature in self.creatures:
            speciesName = creature.species.name
            if speciesName not in populationCount:
                populationCount[speciesName] = 0
            populationCount[speciesName] += 1
        
        self.statistics["population"] = populationCount
    
    def getStatistics(self) -> Dict:
        """
        Get current simulation statistics.
        
        Returns:
            Dict: Statistics dictionary
        """
        stats = self.statistics.copy()
        stats["tick"] = self.tick
        stats["totalAlive"] = len(self.creatures)
        return stats
    
    def getCreaturesByPosition(self) -> Dict[tuple, List[Creature]]:
        """
        Get creatures organized by grid position.
        
        Returns:
            Dict[tuple, List[Creature]]: Dictionary mapping positions to creatures
        """
        positionMap: Dict[tuple, List[Creature]] = {}
        
        for creature in self.creatures:
            pos = creature.getPosition()
            if pos not in positionMap:
                positionMap[pos] = []
            positionMap[pos].append(creature)
        
        return positionMap
    
    def run(self, ticks: int = 1000, verbose: bool = True):
        """
        Run simulation for specified number of ticks.
        
        Args:
            ticks (int): Number of ticks to simulate
            verbose (bool): Whether to print statistics
        """
        for _ in range(ticks):
            self.update()
            
            if verbose and self.tick % 100 == 0:
                stats = self.getStatistics()
                print(f"\n=== Tick {stats['tick']} ===")
                print(f"Total Alive: {stats['totalAlive']}")
                print(f"Births: {stats['births']}")
                print(f"Deaths: {stats['deaths']}")
                print("Population by species:")
                for species, count in stats['population'].items():
                    print(f"  {species}: {count}")