from dataclasses import dataclass
from .game import Game
from pacman.pacman import Pacman


@dataclass
class CheatMode:
    invincible: bool = False
    ghosts_frozen: bool = False
    speed_multiplier: float = 1.0

    def toggle_invincibility(self) -> None:
        """Flip invincibility on/off (cheat mode)."""
        self.invincible = not self.invincible

    def toggle_ghosts_freeze(self) -> None:
        """Flip ghost-freeze on/off (cheat mode)."""
        self.ghosts_frozen = not self.ghosts_frozen

    def skip_level(self, game: "Game") -> None:
        """Immediately advance to the next level (cheat mode)."""
        game.load_next_level()

    def add_life(self, player: Pacman) -> None:
        """Add one life to the player (cheat mode)."""
        player.add_life()

    def increase_speed(self) -> None:
        """Boost the player's movement speed, capped to avoid skipping
        grid cells entirely in a single frame."""
        self.speed_multiplier = min(self.speed_multiplier + 0.5, 3.0)
