"""
Terrain module for managing the environment grid.

This module handles terrain types, plant growth, and environmental features.
"""

import numpy as np
from config import *


class Terrain:
    """
    Manages the terrain grid and environmental features.
    
    Attributes:
        width (int): Grid width in cells
        height (int): Grid height in cells
        grid (np.ndarray): 2D array storing terrain types
        plants (np.ndarray): 2D array storing plant food values
    """
    
    def __init__(self, width: int, height: int):
        """
        Initialize the terrain with specified dimensions.
        
        Args:
            width (int): Grid width
            height (int): Grid height
        """
        self.width = width
        self.height = height
        self.grid = np.full((height, width), TERRAIN_PLAIN, dtype=object)
        self.plants = np.zeros((height, width), dtype=float)
        
        self._generateTerrain()
    
    def _generateTerrain(self):
        """Generate varied terrain with forests, water, and mountains."""
        # Add water bodies
        for _ in range(5):
            centerX = np.random.randint(10, self.width - 10)
            centerY = np.random.randint(10, self.height - 10)
            radius = np.random.randint(3, 8)
            self._createCircularFeature(centerX, centerY, radius, TERRAIN_WATER)
        
        # Add forests
        for _ in range(8):
            centerX = np.random.randint(5, self.width - 5)
            centerY = np.random.randint(5, self.height - 5)
            radius = np.random.randint(4, 12)
            self._createCircularFeature(centerX, centerY, radius, TERRAIN_FOREST)
        
        # Add mountains
        for _ in range(3):
            centerX = np.random.randint(5, self.width - 5)
            centerY = np.random.randint(5, self.height - 5)
            radius = np.random.randint(3, 7)
            self._createCircularFeature(centerX, centerY, radius, TERRAIN_MOUNTAIN)
    
    def _createCircularFeature(self, centerX: int, centerY: int, radius: int, terrainType: str):
        """
        Create a circular terrain feature.
        
        Args:
            centerX (int): Center X coordinate
            centerY (int): Center Y coordinate
            radius (int): Feature radius
            terrainType (str): Type of terrain to place
        """
        for y in range(max(0, centerY - radius), min(self.height, centerY + radius + 1)):
            for x in range(max(0, centerX - radius), min(self.width, centerX + radius + 1)):
                distance = np.sqrt((x - centerX)**2 + (y - centerY)**2)
                if distance <= radius:
                    self.grid[y, x] = terrainType
    
    def getTerrainType(self, x: int, y: int) -> str:
        """
        Get terrain type at specified coordinates.
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            
        Returns:
            str: Terrain type at position
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y, x]
        return TERRAIN_PLAIN
    
    def updatePlants(self, spawnRate: float = DEFAULT_PLANT_SPAWN_RATE):
        """
        Update plant growth across the terrain.
        
        Args:
            spawnRate (float): Probability of plant growth per cell
        """
        # Plants grow better in plains and forests
        for y in range(self.height):
            for x in range(self.width):
                terrainType = self.grid[y, x]
                
                if terrainType == TERRAIN_WATER or terrainType == TERRAIN_MOUNTAIN:
                    continue
                
                # Growth rate modifier based on terrain
                growthModifier = 1.5 if terrainType == TERRAIN_FOREST else 1.0
                
                if np.random.random() < spawnRate * growthModifier:
                    self.plants[y, x] = min(self.plants[y, x] + PLANT_FOOD_VALUE, 
                                           PLANT_FOOD_VALUE * 3)
    
    def consumePlant(self, x: int, y: int, amount: float) -> float:
        """
        Consume plant food at specified position.
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            amount (float): Amount to consume
            
        Returns:
            float: Actual amount consumed
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            consumed = min(self.plants[y, x], amount)
            self.plants[y, x] -= consumed
            return consumed
        return 0.0
    
    def getPlantFood(self, x: int, y: int) -> float:
        """
        Get available plant food at position.
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            
        Returns:
            float: Available plant food
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.plants[y, x]
        return 0.0