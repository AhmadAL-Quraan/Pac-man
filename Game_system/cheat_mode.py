from dataclasses import dataclass


@dataclass
class CheatMode:
    invincible: bool = False
    ghosts_frozen: bool = False
    speed_multiplier: float = 0.0
