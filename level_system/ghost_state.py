from enum import Enum, auto


class GhostState(Enum):
    CHASING = auto()
    EDIBLE = auto()
    EATEN = auto()
