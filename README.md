*This activity has been created as part of the 42 curriculum by aqoraan, atahtamo.*

## Description
This project is a Python implementation of the classic Pac-Man game. The goal of the activity is to recreate the arcade experience with multiple levels, increasingly difficult mazes, and intelligent enemy ghosts. Players must navigate Pac-Man through a maze, eating all the Pacgums while avoiding four ghosts that start at the corners of the map. Eating Super Pacgums allows Pac-Man to temporarily eat the ghosts. The game tracks high scores and features level-based progression.

## Instructions
**Installation:**
The project includes a `Makefile` to simplify the installation process. Ensure you have Python 3 installed.
```bash
# Install required dependencies (pygame, flake8, mypy, mazegenerator)
make install
```

**Execution:**
You can run the game using the Makefile or directly via Python:
```bash
# Using Makefile
make run

# Using Python directly
python3 pac-man.py config.json
```

**Linting and Formatting:**
```bash
make lint    # Runs flake8 and mypy checks
make format  # Formats code using black
make clean   # Cleans up cache directories
```

## Resources
* **Pygame Documentation:** [https://www.pygame.org/docs/](https://www.pygame.org/docs/) - Used for the main game loop, rendering graphics, and handling user input.
* **Pathfinding Algorithms (BFS):** [Wikipedia - Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search) - Used for ghost AI to chase and flee.
* **AI Usage:** An AI coding assistant (Gemini/Antigravity) was used during this project to refactor the initial codebase into a more modular structure, generate the cross-platform `Makefile`, resolve static typing issues (`mypy`), fix PEP-8 linting errors, and structure this README. It was specifically helpful in fixing Python 3 boolean comparisons and implementing the `Pacman` class directly from the UML class diagram.

## Configuration
The game settings are loaded from a JSON configuration file (`config.json`), which is validated by `config.py`.
**Structure and Default Values:**
* `highscore_filename` (string): File to save highscores (default: `"highscores.json"`).
* `lives` (int): Number of starting lives for Pac-Man (default: `3`).
* `pacgum` (int): Max number of pacgums placed in the maze (default: `42`).
* `points_per_pacgum` (int): Score per regular pacgum (default: `10`).
* `points_per_super_pacgum` (int): Score per super pacgum (default: `50`).
* `points_per_ghost` (int): Score for eating a vulnerable ghost (default: `200`).
* `seed` (int): Fixed seed for maze generation ensuring reproducibility (default: `42`).
* `level_max_time` (int): Maximum time allowed per level in seconds (default: `90`).
* `level` (list of objects): An array defining the `width` and `height` dimensions for each sequential level (dimensions should be odd numbers).

## Highscore
The highscore system is implemented using the `PlayerScore` and `PlayerScoreStorage` classes. 
**How it works:** Whenever a game ends, the player's score is checked against the saved highscores. 
**Design Choice:** We decided to implement this by serializing the scores to a simple JSON text file (defined by `highscore_filename`). This approach was chosen because it's lightweight, doesn't require setting up a local SQL database, and is easily editable/readable for testing purposes.

## Maze Generation
The project uses the `A-Maze-ing` package (`mazegenerator`) to dynamically generate levels. 
Instead of hardcoding map layouts, we pass the `width`, `height`, and `seed` from the `config.json` into the `MazeGenerator` class. This algorithm generates a perfect maze grid (a grid with exactly one path between any two points). Our `Maze` class wraps this generation logic to identify walkable paths and walls, allowing for infinite level variations while ensuring the maps remain solvable.

## Implementation
The implementation relies heavily on object-oriented programming principles. The main game loop operates at a fixed framerate via Pygame's clock. 
* **State Management:** The game uses enumerations (`GameState`, `GhostState`) to control transitions (e.g., Playing, Paused, Game Over, Edible Ghosts).
* **Ghost AI:** Ghosts recalculate their paths continuously. In `CHASING` state, they perform a Breadth-First Search (BFS) to find the shortest path to Pac-Man's current grid position. In `EDIBLE` (Flee) state, the algorithm calculates paths to all open cells and selects the one furthest from Pac-Man.
* **Collision Detection:** Implemented using grid-based coordinate matching rather than pixel-perfect bounding boxes, which perfectly suits the discrete grid nature of Pac-Man.

## General Software Architecture
The software is divided into discrete modules handling specific domains:
* **`pacman/`**: Contains the core `Pacman` class and `Direction` enum.
* **`level_system/`**: Manages the environment and entities. Contains `Maze` (wraps maze generation), `Level` (manages pacgums, walls, and level state), and `Ghost`/`GhostState` (enemy AI).
* **`score_system/`**: Contains `PlayerScore` and `PlayerScoreStorage` for managing and persisting scores.
* **`game_system/`**: The controller module. Contains `Game` (the main game loop, rendering, and input routing), `GameState`, and `CheatMode`.
* **`config.py`**: A robust configuration parser and validator that ensures the game never crashes due to bad JSON properties.

**Relationships:** The `Game` class aggregates `Config`, `Level`, `Pacman`, and `PlayerScore`. The `Level` class aggregates `Maze`, `Ghost`, and `Pacgum`. This keeps rendering and game logic decoupled from basic entity data.

## Project Management
We managed this activity using an agile iterative approach. We initially defined the UML class diagrams and System Context diagrams to agree on interfaces. Tasks were broken down into: Core Engine (Pygame loop), Entity Logic, AI/Pathfinding, and Polish (Menus, Highscores). 
For detailed tracking of issues, milestones, and task boards, please refer to the [Project Management Directory](./project_management/).

