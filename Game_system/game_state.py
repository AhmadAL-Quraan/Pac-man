from enum import Enum, auto


class GameState(Enum):
    GAME_OVER = auto()
    VICTORY = auto()
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    ENTERING_NAME = auto()
