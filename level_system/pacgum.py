from dataclasses import dataclass


@dataclass
class Pacgum:
    position: tuple[int, int]
    is_super: bool
    eaten: bool = False
