from enum import Enum


class GhostState(Enum):
    CHASING = 1
    EDIBLE = 0
    EATEN = 0
