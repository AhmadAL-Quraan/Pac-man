from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
from enum import Enum
from typing import Tuple
from .direction import Direction
import pygame
from config import Config

# Prevent the module from beging imported at runtime
if TYPE_CHECKING:
    from level_system.maze import Maze


class Pacman:
    """Represents the Pacman character in the game.

    Attributes:
        _remaining_lives (int): The number of lives Pacman currently has.
        _position (tuple[int, int]): The current (x, y) coordinates of Pacman.
        _direction (Direction): The current direction Pacman is facing/moving.
        _next_direction (Direction): The queued direction from the player's
            latest input, applied as soon as it becomes a legal move.
        _score (int): The current score accumulated by Pacman.
        _start_position (tuple[int, int]): The initial spawn point of Pacman.
        _move_timer (float): Accumulated time (seconds) toward the next step.
        _move_interval (float): Seconds required to cross one grid cell.
    """

    def __init__(
        self,
        start_position: Tuple[int, int],
        initial_direction: Direction = Direction.RIGHT,
        move_interval: float = 0.2,
    ) -> None:
        """Initializes the Pacman instance.

        Args:
            start_position: The starting coordinate (x, y) for Pacman.
            initial_direction: The initial direction. Defaults to RIGHT.
            move_interval: Seconds required to cross one grid cell.
        """
        self._remaining_lives: int = 3
        self._score: int = 0
        self._start_position: tuple[int, int] = start_position

        self._position: Tuple[int, int] = start_position
        self._direction: Direction = initial_direction
        self._next_direction: Direction = initial_direction

        self._move_timer: float = 0.0
        self._move_interval: float = move_interval

    def respawn(self) -> None:
        """Resets Pacman's position, direction, and movement timer."""
        self._position = self._start_position
        self._direction = Direction.RIGHT
        self._next_direction = Direction.RIGHT
        self._move_timer = 0.0

    def update(self, dt: float, speed_multiplier: float, maze: Maze) -> None:
        """Advances Pacman by dt seconds, moving one grid cell once enough
        time has accumulated.

        Args:
            dt: The time elapsed (delta time) since the last update.
            speed_multiplier: The multiplier applied to Pacman's movement speed.
            maze: Used to check whether a move is legal (no wall in the way).
        """
        self._move_timer += dt * speed_multiplier

        if self._move_timer < self._move_interval:
            return

        self._move_timer -= self._move_interval

        if maze.can_move(self._position, self._next_direction):
            self._direction = self._next_direction

        if maze.can_move(self._position, self._direction):
            dx, dy = self._direction.value
            x, y = self._position
            self._position = (x + dx, y + dy)

    def set_direction(self, direction: Direction) -> None:
        """Queues the direction Pacman should turn toward next.

        Args:
            direction: The new direction requested by the player.
        """
        self._next_direction = direction

    def lost_life(self) -> None:
        """Decrements the number of remaining lives by one, floor at 0."""
        if self._remaining_lives > 0:
            self._remaining_lives -= 1

    def add_life(self) -> None:
        """Increments the number of remaining lives by one."""
        self._remaining_lives += 1

    def add_points(self, amount: int) -> None:
        """Increases the score by the given amount.

        Args:
            amount: Points to add (e.g. points_per_pacgum, points_per_ghost).
        """
        self._score += amount

    def draw(self, screen: pygame.Surface) -> None:
        """Draws Pacman as a yellow circle on the screen."""
        cell_size = Config.CELL_SIZE
        row, col = self._position

        # Calculate exact pixel center of the grid cell
        center_x = col * cell_size + cell_size // 2
        center_y = row * cell_size + cell_size // 2

        # Make the radius slightly smaller than the cell bounds
        radius = (cell_size // 2) - 2

        pygame.draw.circle(screen, (255, 255, 0), (center_x, center_y), radius)

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
        """Returns the current direction Pacman is facing."""
        return self._direction

    @property
    def start_position(self) -> tuple[int, int]:
        return self._start_position

    @start_position.setter
    def start_position(self, position: tuple[int, int]):
        self._start_position = position
