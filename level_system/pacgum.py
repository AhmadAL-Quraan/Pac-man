from dataclasses import dataclass


@dataclass
class Pacgum:
    """Class representing Pacgum."""

    position: tuple[int, int]
    is_super: bool
    eaten: bool = False
