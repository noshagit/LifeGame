"""
Creature module defining individual entity behavior and state.

This module contains the Creature class representing individual animals
in the simulation with their stats, behaviors, and AI.
"""

import numpy as np
from typing import Optional, Tuple, List
from species import SpeciesConfig
from config import *


class Creature:
    """
    Represents an individual creature in the simulation.
    
    Attributes:
        species (SpeciesConfig): Species configuration
        x (float): X coordinate position
        y (float): Y coordinate position
        health (float): Current health points
        energy (float): Current energy points
        food (float): Current food storage
        age (int): Current age in ticks
        reproductionCooldown (int): Ticks until can reproduce again
        isAlive (bool): Whether creature is alive
    """
    
    def __init__(self, species: SpeciesConfig, x: float, y: float):
        """
        Initialize a new creature.
        
        Args:
            species (SpeciesConfig): Species configuration
            x (float): Initial X position
            y (float): Initial Y position
        """
        self.species = species
        self.x = x
        self.y = y
        self.health = species.maxHealth
        self.energy = species.maxEnergy
        self.food = species.foodCapacity / 2  # Start with half food
        self.age = 0
        self.reproductionCooldown = 0
        self.isAlive = True
        self.lastDirection = (0, 0)
        
    def update(self, terrain, creatures: List['Creature']):
        """
        Update creature state for one simulation tick.
        
        Args:
            terrain: Terrain object for environment queries
            creatures (List[Creature]): List of all creatures for interaction
        """
        if not self.isAlive:
            return
        
        # Age and lifespan check
        self.age += 1
        if self.age >= self.species.lifespan:
            self.die()
            return
        
        # Metabolism: consume energy and food
        self._consumeMetabolism()
        
        # Check starvation
        if self.food <= 0:
            self._handleStarvation()
        
        # Death check
        if self.health <= 0:
            self.die()
            return
        
        # Decrease reproduction cooldown
        if self.reproductionCooldown > 0:
            self.reproductionCooldown -= 1
        
        # AI decision making
        self._makeDecision(terrain, creatures)
    
    def _consumeMetabolism(self):
        """Handle metabolic energy and food consumption."""
        # Consume energy
        self.energy = max(0, self.energy - self.species.metabolism)
        
        # Consume food to restore energy if needed
        if self.energy < self.species.maxEnergy * 0.5 and self.food > 0:
            energyNeeded = self.species.maxEnergy - self.energy
            foodToConsume = min(self.food, energyNeeded / 2)
            self.food -= foodToConsume
            self.energy = min(self.species.maxEnergy, self.energy + foodToConsume * 2)
    
    def _handleStarvation(self):
        """Handle effects of starvation."""
        # Lose health when starving
        starvationDamage = self.species.maxHealth / self.species.starvationTime
        self.health = max(0, self.health - starvationDamage)
    
    def _makeDecision(self, terrain, creatures: List['Creature']):
        """
        AI decision making for creature behavior.
        
        Args:
            terrain: Terrain object
            creatures (List[Creature]): All creatures in simulation
        """
        # Priority: survival > reproduction > exploration
        
        # 1. Check if need food urgently
        if self.food < self.species.foodCapacity * 0.3:
            self._searchForFood(terrain, creatures)
            return
        
        # 2. Check if can reproduce
        if (self.age >= self.species.maturityAge and 
            self.reproductionCooldown == 0 and
            self.energy > self.species.maxEnergy * 0.6):
            if self._attemptReproduction(creatures):
                return
        
        # 3. Check for threats
        nearbyThreats = self._detectThreats(creatures)
        if nearbyThreats:
            self._flee(nearbyThreats[0])
            return
        
        # 4. Random exploration
        self._randomMove(terrain)
    
    def _searchForFood(self, terrain, creatures: List['Creature']):
        """
        Search for and move towards food sources.
        
        Args:
            terrain: Terrain object
            creatures (List[Creature]): All creatures
        """
        if FOOD_PLANTS in self.species.dietPreferences:
            # Search for plants
            bestPlantPos = self._findNearestPlant(terrain)
            if bestPlantPos:
                self._moveTowards(bestPlantPos[0], bestPlantPos[1], terrain)
                # Try to eat if close enough
                if abs(self.x - bestPlantPos[0]) < 1 and abs(self.y - bestPlantPos[1]) < 1:
                    self._eatPlant(terrain, int(bestPlantPos[0]), int(bestPlantPos[1]))
                return
        
        if FOOD_SMALL_ANIMALS in self.species.dietPreferences:
            # Hunt for prey
            prey = self._findPrey(creatures)
            if prey:
                self._hunt(prey, terrain)
                return
        
        # No food found, random move
        self._randomMove(terrain)
    
    def _findNearestPlant(self, terrain) -> Optional[Tuple[int, int]]:
        """
        Find nearest plant within vision range.
        
        Args:
            terrain: Terrain object
            
        Returns:
            Optional[Tuple[int, int]]: Position of nearest plant or None
        """
        bestPos = None
        bestDistance = float('inf')
        
        for dy in range(-self.species.visionRange, self.species.visionRange + 1):
            for dx in range(-self.species.visionRange, self.species.visionRange + 1):
                x = int(self.x + dx)
                y = int(self.y + dy)
                
                if terrain.getPlantFood(x, y) > 0:
                    distance = np.sqrt(dx**2 + dy**2)
                    if distance < bestDistance:
                        bestDistance = distance
                        bestPos = (x, y)
        
        return bestPos
    
    def _findPrey(self, creatures: List['Creature']) -> Optional['Creature']:
        """
        Find suitable prey within detection range.
        
        Args:
            creatures (List[Creature]): All creatures
            
        Returns:
            Optional[Creature]: Target prey or None
        """
        for creature in creatures:
            if creature is self or not creature.isAlive:
                continue
            
            # Can only hunt smaller creatures
            if creature.species.size >= self.species.size * 0.8:
                continue
            
            distance = np.sqrt((creature.x - self.x)**2 + (creature.y - self.y)**2)
            
            if distance <= self.species.visionRange:
                return creature
        
        return None
    
    def _hunt(self, prey: 'Creature', terrain):
        """
        Chase and attack prey.
        
        Args:
            prey (Creature): Target prey
            terrain: Terrain object
        """
        # Move towards prey
        self._moveTowards(prey.x, prey.y, terrain)
        
        # Attack if close enough
        distance = np.sqrt((prey.x - self.x)**2 + (prey.y - self.y)**2)
        if distance < 1.5:
            self._attack(prey)
    
    def _attack(self, target: 'Creature'):
        """
        Attack another creature.
        
        Args:
            target (Creature): Target to attack
        """
        damage = max(0, self.species.attackPower - target.species.defense)
        target.health = max(0, target.health - damage)
        
        # Consume energy for attacking
        self.energy = max(0, self.energy - self.species.metabolism * 2)
        
        # If target dies, gain food
        if target.health <= 0:
            target.die()
            foodGained = min(target.species.size * 5, self.species.foodCapacity - self.food)
            self.food += foodGained
    
    def _detectThreats(self, creatures: List['Creature']) -> List['Creature']:
        """
        Detect nearby predators.
        
        Args:
            creatures (List[Creature]): All creatures
            
        Returns:
            List[Creature]: List of threatening creatures
        """
        threats = []
        
        for creature in creatures:
            if creature is self or not creature.isAlive:
                continue
            
            # Threat if larger and carnivorous/omnivorous
            if (creature.species.size > self.species.size * 1.2 and
                creature.species.aggression > 0.3):
                
                distance = np.sqrt((creature.x - self.x)**2 + (creature.y - self.y)**2)
                
                if distance <= self.species.visionRange:
                    threats.append(creature)
        
        return threats
    
    def _flee(self, threat: 'Creature'):
        """
        Flee from a threat.
        
        Args:
            threat (Creature): Creature to flee from
        """
        # Move in opposite direction
        dx = self.x - threat.x
        dy = self.y - threat.y
        
        # Normalize and move
        distance = np.sqrt(dx**2 + dy**2)
        if distance > 0:
            dx /= distance
            dy /= distance
            
            newX = self.x + dx * self.species.baseSpeed * 1.5
            newY = self.y + dy * self.species.baseSpeed * 1.5
            
            self._moveTo(newX, newY)
        
        # Consume extra energy for fleeing
        self.energy = max(0, self.energy - self.species.metabolism * 1.5)
    
    def _moveTowards(self, targetX: float, targetY: float, terrain):
        """
        Move towards a target position.
        
        Args:
            targetX (float): Target X coordinate
            targetY (float): Target Y coordinate
            terrain: Terrain object
        """
        dx = targetX - self.x
        dy = targetY - self.y
        
        distance = np.sqrt(dx**2 + dy**2)
        if distance > 0:
            dx /= distance
            dy /= distance
            
            # Get terrain speed modifier
            currentTerrain = terrain.getTerrainType(int(self.x), int(self.y))
            speedModifier = self.species.terrainSpeed.get(currentTerrain, 1.0)
            
            newX = self.x + dx * self.species.baseSpeed * speedModifier
            newY = self.y + dy * self.species.baseSpeed * speedModifier
            
            self._moveTo(newX, newY)
    
    def _randomMove(self, terrain):
        """
        Move in a random direction.
        
        Args:
            terrain: Terrain object
        """
        angle = np.random.random() * 2 * np.pi
        dx = np.cos(angle)
        dy = np.sin(angle)
        
        currentTerrain = terrain.getTerrainType(int(self.x), int(self.y))
        speedModifier = self.species.terrainSpeed.get(currentTerrain, 1.0)
        
        newX = self.x + dx * self.species.baseSpeed * speedModifier
        newY = self.y + dy * self.species.baseSpeed * speedModifier
        
        self._moveTo(newX, newY)
    
    def _moveTo(self, newX: float, newY: float):
        """
        Move to a new position with bounds checking.
        
        Args:
            newX (float): New X coordinate
            newY (float): New Y coordinate
        """
        self.x = max(0, min(GRID_WIDTH - 1, newX))
        self.y = max(0, min(GRID_HEIGHT - 1, newY))
    
    def _eatPlant(self, terrain, x: int, y: int):
        """
        Consume plant food at position.
        
        Args:
            terrain: Terrain object
            x (int): X coordinate
            y (int): Y coordinate
        """
        availableFood = terrain.getPlantFood(x, y)
        canEat = min(availableFood, self.species.foodCapacity - self.food)
        
        if canEat > 0:
            consumed = terrain.consumePlant(x, y, canEat)
            self.food += consumed
    
    def _attemptReproduction(self, creatures: List['Creature']) -> bool:
        """
        Attempt to reproduce with nearby mate.
        
        Args:
            creatures (List[Creature]): All creatures
            
        Returns:
            bool: True if reproduction occurred
        """
        # Find nearby mate of same species
        for creature in creatures:
            if (creature is not self and 
                creature.isAlive and
                creature.species.name == self.species.name and
                creature.age >= creature.species.maturityAge and
                creature.reproductionCooldown == 0):
                
                distance = np.sqrt((creature.x - self.x)**2 + (creature.y - self.y)**2)
                
                if distance < 3:
                    # Reproduce!
                    self.reproductionCooldown = self.species.reproductionCooldown
                    creature.reproductionCooldown = creature.species.reproductionCooldown
                    
                    # Offspring will be created by simulation manager
                    return True
        
        return False
    
    def die(self):
        """Mark creature as dead."""
        self.isAlive = False
        self.health = 0
    
    def getPosition(self) -> Tuple[int, int]:
        """
        Get integer grid position.
        
        Returns:
            Tuple[int, int]: Grid coordinates
        """
        return (int(self.x), int(self.y))