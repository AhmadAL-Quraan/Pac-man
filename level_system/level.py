from dataclasses import dataclass

from pacman import pacman
from .maze import Maze
from .ghost import Ghost
from .pacgum import Pacgum
from pacman.pacman import Pacman
from .ghost_state import GhostState


@dataclass
class Level:
    maze: Maze
    ghosts: list[Ghost]
    pacgums: dict[tuple[int, int], Pucgum]
    time_remaining: float
    level_number: int

    def reset_position(self, player: Pacman):
        player._position = player._start_position

    def check_collision(self, player: Pacman):
        for i in self.ghosts:
            if i.position == player._position:
                if i.state == GhostState.CHASING:
                    self.reset_position(player)
                elif i.state == GhostState.EDIBLE:
                    i.respawn()

    def is_complete(self) -> bool:
        if len(self.pacgums) == 0:
            return True

        return False

    def check_failed(self, player: Pacman) -> bool:
        """Check if the level has failed, either the pacman life ends or the time has end

        Args:
            player: The pacman instance
        return:
            True if failed
            False if it didn't failed
        """
        if player._remaining_lives == 0:
            return True

        if self.time_remaining <= 0:
            return True
        return False
