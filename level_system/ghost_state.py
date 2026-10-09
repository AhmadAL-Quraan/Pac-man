from enum import Enum, auto


class GhostState(Enum):
    """Class representing GhostState."""

    CHASING = auto()
    EDIBLE = auto()
    EATEN = auto()
