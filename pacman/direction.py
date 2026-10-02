from enum import Enum


class Direction(Enum):
    """Enumeration representing the possible directions Pacman can move."""

    RIGHT = (0, 1)
    LEFT = (0, -1)
    UP = (-1, 0)
    DOWN = (1, 0)
