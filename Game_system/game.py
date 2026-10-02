from dataclasses import dataclass

from .game_state import GameState
from Game_system.cheat_mode import CheatMode
from level_system.level import Level
from pacman.pacman import Pacman
from ..config import Config
from ..Score_system.player_score import PlayerScore
import pygame


@dataclass
class Game:
    config: Config
    player: Pacman
    current_level = Level
    state: GameState
    score_storage: PlayerScore
    cheat_mode: CheatMode

    def run(self) -> None:
        pass

    def start_new_game(self) -> None:
        pass

    def load_next_level(self) -> None:
        pass

    def pause(self) -> None:
        pass

    def resume(self) -> None:
        pass

    def end_game(self, won: bool) -> None:
        pass

    def handle_input(self, event) -> None:
        pass
