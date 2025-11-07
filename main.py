"""
Main entry point for the Advanced Game of Life simulation.

This module provides different execution modes for the simulation:
- Graphical mode with Tkinter visualization
- Headless mode for data collection
- Benchmark mode for performance testing
"""

import argparse
import sys
from simulation import Simulation
from visualizer import Visualizer
from config import GRID_WIDTH, GRID_HEIGHT


def runGraphical(width: int = GRID_WIDTH, height: int = GRID_HEIGHT):
    """
    Run the simulation with graphical interface.
    
    Args:
        width (int): Grid width
        height (int): Grid height
    """
    print("Starting Advanced Game of Life - Graphical Mode")
    print(f"Grid size: {width}x{height}")
    print("\nControls:")
    print("  Space: Play/Pause")
    print("  Step: Advance one tick")
    print("  Reset: Restart simulation")
    print("  Esc: Quit")
    print("\nInitializing...")
    
    simulation = Simulation(width, height)
    visualizer = Visualizer(simulation)
    
    print("Ready! Press Start to begin.")
    visualizer.run()


def runHeadless(width: int = GRID_WIDTH, height: int = GRID_HEIGHT, ticks: int = 1000, verbose: bool = True):
    """
    Run the simulation without graphics (headless mode).
    
    Args:
        width (int): Grid width
        height (int): Grid height
        ticks (int): Number of ticks to simulate
        verbose (bool): Whether to print statistics
    """
    print("Starting Advanced Game of Life - Headless Mode")
    print(f"Grid size: {width}x{height}")
    print(f"Simulating {ticks} ticks...\n")
    
    simulation = Simulation(width, height)
    simulation.run(ticks, verbose)
    
    print("\n=== Final Statistics ===")
    stats = simulation.getStatistics()
    print(f"Total ticks: {stats['tick']}")
    print(f"Total creatures spawned: {stats['totalCreatures']}")
    print(f"Total births: {stats['births']}")
    print(f"Total deaths: {stats['deaths']}")
    print(f"Survivors: {stats['totalAlive']}")
    print("\nFinal population by species:")
    for species, count in stats['population'].items():
        print(f"  {species}: {count}")


def runBenchmark(width: int = GRID_WIDTH, height: int = GRID_HEIGHT, ticks: int = 1000):
    """
    Run performance benchmark.
    
    Args:
        width (int): Grid width
        height (int): Grid height
        ticks (int): Number of ticks to benchmark
    """
    import time
    
    print("Starting Advanced Game of Life - Benchmark Mode")
    print(f"Grid size: {width}x{height}")
    print(f"Benchmarking {ticks} ticks...\n")
    
    simulation = Simulation(width, height)
    
    startTime = time.time()
    simulation.run(ticks, verbose=False)
    endTime = time.time()
    
    elapsed = endTime - startTime
    ticksPerSecond = ticks / elapsed if elapsed > 0 else 0
    
    print("\n=== Benchmark Results ===")
    print(f"Total time: {elapsed:.2f} seconds")
    print(f"Ticks per second: {ticksPerSecond:.2f}")
    print(f"Average tick duration: {(elapsed / ticks * 1000):.2f} ms")
    
    stats = simulation.getStatistics()
    print(f"\nFinal population: {stats['totalAlive']}")


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Advanced Game of Life Simulation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py                          # Run with GUI
    python main.py --headless               # Run without GUI
    python main.py --headless --ticks 5000  # Run 5000 ticks
    python main.py --benchmark              # Performance test
    python main.py --width 200 --height 200 # Larger grid
        """
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run without graphical interface'
    )
    
    parser.add_argument(
        '--benchmark',
        action='store_true',
        help='Run performance benchmark'
    )
    
    parser.add_argument(
        '--width',
        type=int,
        default=GRID_WIDTH,
        help=f'Grid width (default: {GRID_WIDTH})'
    )
    
    parser.add_argument(
        '--height',
        type=int,
        default=GRID_HEIGHT,
        help=f'Grid height (default: {GRID_HEIGHT})'
    )
    
    parser.add_argument(
        '--ticks',
        type=int,
        default=1000,
        help='Number of ticks to simulate in headless mode (default: 1000)'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress periodic statistics output'
    )
    
    args = parser.parse_args()
    
    try:
        if args.benchmark:
            runBenchmark(args.width, args.height, args.ticks)
        elif args.headless:
            runHeadless(args.width, args.height, args.ticks, not args.quiet)
        else:
            runGraphical(args.width, args.height)
    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()