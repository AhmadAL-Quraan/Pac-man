# Project Timeline & Progress Tracking

## Milestone 1: Planning and Architecture (Days 1-2)
* **Status:** COMPLETED
* **Tasks:**
  * Define UML Class Diagram (`pic/class_diagram.png`).
  * Define System Context Diagram (`pic/system_context_diagram.png`).
  * Scaffold repository and set up `Makefile`, `.gitignore`, and `requirements.txt`.

## Milestone 2: Core Engine & Data Validation (Days 3-5)
* **Status:** COMPLETED
* **Tasks:**
  * Build robust JSON config loader and validation (`config.py`).
  * Implement Pygame display loop and event handling in `game_system/game.py`.
  * Set up modular state machines (`GameState`, `GhostState`).

## Milestone 3: Maze Generation & Environment (Days 6-8)
* **Status:** COMPLETED
* **Tasks:**
  * Integrate the `A-Maze-ing` package.
  * Map generator outputs to the internal `Maze` class.
  * Scatter Pacgums and Super-Pacgums.

## Milestone 4: Entities and Artificial Intelligence (Days 9-12)
* **Status:** COMPLETED
* **Tasks:**
  * Build `Pacman` movement and grid alignment logic.
  * Implement Breadth-First Search (BFS) for Ghost chasing behavior.
  * Implement Flee behavior for edible ghosts.
  * Create collision detection system.

## Milestone 5: UI, Polish, and Packaging (Days 13-14)
* **Status:** COMPLETED
* **Tasks:**
  * Build Main Menu and Highscore display.
  * Add cheat mode toggles for reviewers.
  * Finalize `README.md` to perfectly adhere to the curriculum specifications.
  * Verify full cross-platform compatibility and graceful crash handling.
