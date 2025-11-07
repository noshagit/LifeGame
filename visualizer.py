"""
Visualization module using Tkinter for rendering the simulation.

This module provides a graphical interface to visualize the game state
in real-time.
"""

import tkinter as tk
from typing import Optional
from simulation import Simulation
from config import *


class Visualizer:
    """
    Tkinter-based visualizer for the simulation.
    
    Attributes:
        simulation (Simulation): The simulation instance to visualize
        window (tk.Tk): Main window
        canvas (tk.Canvas): Drawing canvas
        isRunning (bool): Whether simulation is running
        updateInterval (int): Milliseconds between updates
    """
    
    def __init__(self, simulation: Simulation, cellSize: int = CELL_SIZE):
        """
        Initialize the visualizer.
        
        Args:
            simulation (Simulation): Simulation instance
            cellSize (int): Size of each cell in pixels
        """
        self.simulation = simulation
        self.cellSize = cellSize
        self.isRunning = False
        self.updateInterval = int(TICK_DURATION * 1000)
        
        # Create window
        self.window = tk.Tk()
        self.window.title("Advanced Game of Life")
        
        # Calculate canvas size
        canvasWidth = simulation.terrain.width * cellSize
        canvasHeight = simulation.terrain.height * cellSize
        
        # Create main frame
        mainFrame = tk.Frame(self.window)
        mainFrame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas with scrollbars
        self.canvas = tk.Canvas(
            mainFrame,
            width=min(canvasWidth, 1200),
            height=min(canvasHeight, 800),
            bg="white"
        )
        
        vScrollbar = tk.Scrollbar(mainFrame, orient=tk.VERTICAL, command=self.canvas.yview)
        hScrollbar = tk.Scrollbar(mainFrame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        self.canvas.config(
            yscrollcommand=vScrollbar.set,
            xscrollcommand=hScrollbar.set,
            scrollregion=(0, 0, canvasWidth, canvasHeight)
        )
        
        # Pack widgets
        vScrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        hScrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create control panel
        self._createControlPanel()
        
        # Create statistics display
        self._createStatisticsPanel()
        
        # Bind keyboard shortcuts
        self.window.bind('<space>', lambda e: self.togglePause())
        self.window.bind('<Escape>', lambda e: self.window.quit())
    
    def _createControlPanel(self):
        """Create control buttons panel."""
        controlFrame = tk.Frame(self.window)
        controlFrame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        self.startButton = tk.Button(
            controlFrame,
            text="Start",
            command=self.start,
            width=10
        )
        self.startButton.pack(side=tk.LEFT, padx=5)
        
        self.pauseButton = tk.Button(
            controlFrame,
            text="Pause",
            command=self.pause,
            width=10,
            state=tk.DISABLED
        )
        self.pauseButton.pack(side=tk.LEFT, padx=5)
        
        self.stepButton = tk.Button(
            controlFrame,
            text="Step",
            command=self.step,
            width=10
        )
        self.stepButton.pack(side=tk.LEFT, padx=5)
        
        self.resetButton = tk.Button(
            controlFrame,
            text="Reset",
            command=self.reset,
            width=10
        )
        self.resetButton.pack(side=tk.LEFT, padx=5)
        
        self.quitButton = tk.Button(
            controlFrame,
            text="Quit",
            command=self.window.quit,
            width=10
        )
        self.quitButton.pack(side=tk.RIGHT, padx=5)
    
    def _createStatisticsPanel(self):
        """Create statistics display panel."""
        statsFrame = tk.Frame(self.window, relief=tk.SUNKEN, borderwidth=2)
        statsFrame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        self.statsLabel = tk.Label(
            statsFrame,
            text="Statistics will appear here",
            font=("Courier", 10),
            justify=tk.LEFT,
            anchor=tk.W
        )
        self.statsLabel.pack(fill=tk.X, padx=5, pady=5)
    
    def draw(self):
        """Draw the current simulation state."""
        self.canvas.delete("all")
        
        # Draw terrain
        self._drawTerrain()
        
        # Draw plants
        self._drawPlants()
        
        # Draw creatures
        self._drawCreatures()
    
    def _drawTerrain(self):
        """Draw the terrain grid."""
        for y in range(self.simulation.terrain.height):
            for x in range(self.simulation.terrain.width):
                terrainType = self.simulation.terrain.getTerrainType(x, y)
                color = self._getTerrainColor(terrainType)
                
                x1 = x * self.cellSize
                y1 = y * self.cellSize
                x2 = x1 + self.cellSize
                y2 = y1 + self.cellSize
                
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline=""
                )
    
    def _drawPlants(self):
        """Draw plant food sources."""
        for y in range(self.simulation.terrain.height):
            for x in range(self.simulation.terrain.width):
                plantFood = self.simulation.terrain.getPlantFood(x, y)
                
                if plantFood > 0:
                    # Draw plant with intensity based on food value
                    intensity = min(255, int(plantFood * 25))
                    color = f"#{0:02x}{intensity:02x}{0:02x}"
                    
                    x1 = x * self.cellSize + self.cellSize // 4
                    y1 = y * self.cellSize + self.cellSize // 4
                    x2 = x1 + self.cellSize // 2
                    y2 = y1 + self.cellSize // 2
                    
                    self.canvas.create_oval(
                        x1, y1, x2, y2,
                        fill=color,
                        outline=""
                    )
    
    def _drawCreatures(self):
        """Draw all living creatures."""
        for creature in self.simulation.creatures:
            if not creature.isAlive:
                continue
            
            x = int(creature.x * self.cellSize)
            y = int(creature.y * self.cellSize)
            
            # Get species color
            color = self._getCreatureColor(creature.species.name)
            
            # Size based on creature size parameter
            sizeMultiplier = min(1.5, max(0.3, creature.species.size / 20))
            radius = int(self.cellSize * 0.4 * sizeMultiplier)
            
            # Draw creature
            self.canvas.create_oval(
                x - radius, y - radius,
                x + radius, y + radius,
                fill=color,
                outline="black",
                width=1
            )
            
            # Draw health bar
            healthPercent = creature.health / creature.species.maxHealth
            barWidth = self.cellSize
            barHeight = 3
            
            barX = x - barWidth // 2
            barY = y - radius - 5
            
            # Background
            self.canvas.create_rectangle(
                barX, barY,
                barX + barWidth, barY + barHeight,
                fill="red",
                outline=""
            )
            
            # Health
            self.canvas.create_rectangle(
                barX, barY,
                barX + int(barWidth * healthPercent), barY + barHeight,
                fill="green",
                outline=""
            )
    
    def _getTerrainColor(self, terrainType: str) -> str:
        """
        Get color for terrain type.
        
        Args:
            terrainType (str): Type of terrain
            
        Returns:
            str: Hex color string
        """
        colorMap = {
            TERRAIN_PLAIN: "#c8c896",
            TERRAIN_FOREST: "#228b22",
            TERRAIN_WATER: "#3264c8",
            TERRAIN_MOUNTAIN: "#808080"
        }
        return colorMap.get(terrainType, "#ffffff")
    
    def _getCreatureColor(self, speciesName: str) -> str:
        """
        Get color for species.
        
        Args:
            speciesName (str): Species name
            
        Returns:
            str: Hex color string
        """
        if speciesName in COLORS:
            rgb = COLORS[speciesName]
            return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        return "#000000"
    
    def _updateStatistics(self):
        """Update statistics display."""
        stats = self.simulation.getStatistics()
        
        text = f"Tick: {stats['tick']}  |  "
        text += f"Total Alive: {stats['totalAlive']}  |  "
        text += f"Births: {stats['births']}  |  "
        text += f"Deaths: {stats['deaths']}\n"
        text += "Population: "
        
        for species, count in stats['population'].items():
            text += f"{species}: {count}  "
        
        self.statsLabel.config(text=text)
    
    def start(self):
        """Start the simulation."""
        if not self.isRunning:
            self.isRunning = True
            self.startButton.config(state=tk.DISABLED)
            self.pauseButton.config(state=tk.NORMAL)
            self._runLoop()
    
    def pause(self):
        """Pause the simulation."""
        self.isRunning = False
        self.startButton.config(state=tk.NORMAL)
        self.pauseButton.config(state=tk.DISABLED)
    
    def togglePause(self):
        """Toggle pause state."""
        if self.isRunning:
            self.pause()
        else:
            self.start()
    
    def step(self):
        """Execute one simulation step."""
        self.simulation.update()
        self.draw()
        self._updateStatistics()
    
    def reset(self):
        """Reset the simulation."""
        self.pause()
        self.simulation = Simulation(
            self.simulation.terrain.width,
            self.simulation.terrain.height
        )
        self.draw()
        self._updateStatistics()
    
    def _runLoop(self):
        """Main simulation loop."""
        if self.isRunning:
            self.step()
            self.window.after(self.updateInterval, self._runLoop)
    
    def run(self):
        """Start the visualization window."""
        self.draw()
        self._updateStatistics()
        self.window.mainloop()