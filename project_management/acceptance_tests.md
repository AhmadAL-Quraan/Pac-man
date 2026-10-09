# Acceptance Test Plan

This document outlines the core functional requirements and the manual tests performed to verify their completion.

## 1. Config Loading & Fault Tolerance
* **Test:** Launch `python pac-man.py config.json` with a perfectly valid config.
  * **Expected:** Game starts successfully with provided values.
  * **Result:** PASS
* **Test:** Launch with an invalid/missing value (e.g., `{"width": "hello"}`).
  * **Expected:** Program does not crash; it warns the user and falls back to safe default dimensions (e.g., 21x21).
  * **Result:** PASS
* **Test:** Launch without arguments or with a non-existent file.
  * **Expected:** Graceful error message printed to console, `sys.exit(1)` called. No tracebacks.
  * **Result:** PASS

## 2. Gameplay Mechanics
* **Test:** Pac-Man navigation using Arrow Keys/WASD.
  * **Expected:** Pac-Man stops at walls, turns correctly in corridors, cannot phase through blocks.
  * **Result:** PASS
* **Test:** Eating regular Pacgums.
  * **Expected:** Score increases by `points_per_pacgum` (10). Pacgum disappears.
  * **Result:** PASS
* **Test:** Eating Super-Pacgums.
  * **Expected:** Score increases by `points_per_super_pacgum` (50). Ghosts switch to `EDIBLE` state (fleeing).
  * **Result:** PASS

## 3. Enemy AI (Ghosts)
* **Test:** Ghost Chasing (Normal state).
  * **Expected:** Ghosts use BFS to find the shortest path to Pac-Man and relentlessly pursue.
  * **Result:** PASS
* **Test:** Ghost Collision (Normal state).
  * **Expected:** Pac-Man loses a life (`lives - 1`), game pauses momentarily, entities reset to spawn points. Game Over triggers if lives reach 0.
  * **Result:** PASS
* **Test:** Ghost Eaten (Edible state).
  * **Expected:** Score increases by `points_per_ghost` (200). Ghost instantly respawns at its designated corner.
  * **Result:** PASS

## 4. UI and Highscores
* **Test:** End of game sequence.
  * **Expected:** Victory/Defeat screen shows up. Prompt asks for player name.
  * **Result:** PASS
* **Test:** Name input validation.
  * **Expected:** Only accepts alphanumeric characters and spaces. Rejects names longer than 10 characters.
  * **Result:** PASS
* **Test:** Highscore persistence.
  * **Expected:** Closing the game and reopening it correctly displays the saved score in the Main Menu's "Top 10" list.
  * **Result:** PASS

## 5. Cheat Mode (Peer Review)
* **Test:** Toggle Invincibility / Freeze.
  * **Expected:** Ghosts can no longer damage Pac-Man, or ghosts stop moving entirely. Used purely for reviewer demonstration.
  * **Result:** PASS
