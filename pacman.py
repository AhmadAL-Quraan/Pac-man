from enum import Enum, auto
from typing import Tuple

class Direction(Enum):
    """
    Enumeration representing the possible directions Pacman can move.
    """
    RIGHT = auto()
    LEFT = auto()
    UP = auto()
    DOWN = auto()

class Pacman:
    """
    Represents the Pacman character in the game.

    Attributes:
        _remaining_lives (int): The number of lives Pacman currently has. Defaults to 3.
        _position (tuple[int, int]): The current (x, y) coordinates of Pacman.
        _direction (Direction): The current direction Pacman is facing/moving.
        _score (int): The current score accumulated by Pacman. Defaults to 0.
        _start_position (tuple[int, int]): The initial spawn point (x, y) of Pacman.
    """

    def __init__(self, start_position: Tuple[int, int], initial_direction: Direction = Direction.RIGHT):
        """
        Initializes the Pacman instance.

        Args:
            start_position (tuple[int, int]): The starting coordinate (x, y) for Pacman.
            initial_direction (Direction, optional): The initial direction. Defaults to Direction.RIGHT.
        """
        self._remaining_lives: int = 3
        self._score: int = 0
        self._start_position: Tuple[int, int] = start_position
        
        self._position: Tuple[int, int] = start_position
        self._direction: Direction = initial_direction

    def respawn(self) -> None:
        """
        Resets Pacman's current position back to the starting position.
        """
        self._position = self._start_position

    def update(self, dt: float, speed_multiplier: float) -> None:
        """
        Updates Pacman's state (e.g., moving his position) based on the time elapsed and speed.

        Args:
            dt (float): The time elapsed (delta time) since the last update.
            speed_multiplier (float): The multiplier applied to Pacman's movement speed.
        """
        # Movement logic based on self._direction, dt, and speed_multiplier will be implemented here
        pass

    def set_direction(self, direction: Direction) -> None:
        """
        Changes the direction Pacman is currently facing.

        Args:
            direction (Direction): The new direction for Pacman to face.
        """
        self._direction = direction

    def lost_life(self) -> None:
        """
        Decrements the number of remaining lives by one.
        """
        if self._remaining_lives > 0:
            self._remaining_lives -= 1

    def add_life(self) -> None:
        """
        Increments the number of remaining lives by one.
        """
        self._remaining_lives += 1

    # Optional: Getters for accessing private attributes outside the class
    @property
    def score(self) -> int:
        """Returns the current score."""
        return self._score

    @property
    def position(self) -> Tuple[int, int]:
        """Returns the current position."""
        return self._position

    @property
    def remaining_lives(self) -> int:
        """Returns the number of remaining lives."""
        return self._remaining_lives

    @property
    def direction(self) -> Direction:
        """Returns the current direction."""
        return self._direction

