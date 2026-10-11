# Pac-Man Game Quick Start

## Run the game

```bash
python3 pac-man.py config.json
```

The game expects exactly one argument: the path to the JSON configuration file.

## Main menu

The menu includes:

- Start Game
- High Scores
- Controls
- Quit

Use:

- Up / Down to move through the menu
- Enter / Space to select
- Escape to return from score/control screens
- Mouse click also works on the main menu buttons

## In-game controls

- Move: Arrow keys or W A S D
- Pause / resume: P
- Toggle cheat mode: C

Cheats are only active while cheat mode is enabled, and then these keys work:

- I: invincibility
- F: freeze ghosts
- K: skip level
- L: extra life
- O: increase speed

## Configuration

The JSON config file controls maze setup, scoring, and game timing. Comments are allowed because the loader strips lines beginning with `#` or `//`.

Example:

```json
{
  "highscore_filename": "test.txt",
  "lives": 3,
  "pacgum": 42,
  "points_per_pacgum": 10,
  "points_per_super_pacgum": 50,
  "points_per_ghost": 200,
  "seed": 42,
  "level_max_time": 90,
  "level": [
    {"width": 21, "height": 21},
    {"width": 21, "height": 21},
    {"width": 21, "height": 21}
  ]
}
```

### Supported fields

- `highscore_filename`: file used to save high scores
- `lives`: starting lives for Pac-Man
- `pacgum`: target number of pacgums to place per level (clamped by maze size)
- `points_per_pacgum`: score for a normal pacgum
- `points_per_super_pacgum`: score for a super pacgum
- `points_per_ghost`: bonus for eating a ghost
- `seed`: fixed seed for maze generation
- `level_max_time`: time limit for each level
- `level`: array of level definitions, each containing `width` and `height`

### Level sizing rules

- Each level entry must include `width` and `height`
- Values are clamped to a safe minimum and to the screen-fit maximum
- The loader pads the list to at least 10 levels if needed

## Notes

- The game window resizes to the current maze and HUD
- The default score file is `highscores.txt` if no filename is given
- The built-in game loop runs at about 60 FPS
