# Risk Analysis & Mitigation

During the planning phase, the following risks were identified and actively managed throughout the project lifecycle:

| Risk | Impact | Probability | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Maze Generator Incompatibility** | High | Medium | The required `A-Maze-ing` package interface might change. We abstracted the maze generator behind our own `Maze` wrapper class in `level_system/maze.py` so that only one file needs to be updated if the external library changes. |
| **Pygame Performance Bottlenecks** | Medium | High | Frame drops due to heavy BFS pathfinding calculations for 4 ghosts every frame. Mitigation: Cap framerate to 60 FPS using `pygame.time.Clock().tick(60)` and optimize grid-based coordinate matching instead of heavy pixel-perfect collision masks. |
| **Invalid Config Files Crashing the Game** | High | High | Users providing malformed JSON files. Mitigation: Created a robust static validation class (`config.py`) that strictly clamps invalid types, out-of-bounds dimensions, and missing keys to safe defaults instead of throwing Python tracebacks. |
| **Memory Leaks from Improper Shutdowns** | Medium | Low | Exiting the game abruptly might leave Pygame processes hanging. Mitigation: Implemented a top-level `try/finally` block in the game loop and a `try/except` around the entry point to guarantee `pygame.quit()` and `sys.exit()` are called gracefully on `KeyboardInterrupt` or unexpected fatal errors. |
| **Loss of Highscore Data** | Low | Low | Simultaneous read/write errors on `highscores.json`. Mitigation: Highscores are loaded to memory at start and only dumped to the JSON text file cleanly upon Game Over. |
