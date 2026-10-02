from dataclasses import dataclass

from pacman.pacman import Pacman
from .maze import Maze
from .ghost import Ghost
from .pacgum import Pacgum
from .ghost_state import GhostState
from Game_system.cheat_mode import CheatMode

from level_system import ghost


@dataclass
class Level:
    maze: Maze
    ghosts: list[Ghost]
    pacgums: dict[tuple[int, int], Pacgum]
    _time_remaining: float
    level_number: int

    def _reset_position(self, player: Pacman) -> None:
        """Reset the position of all entities when the game start or resets.

        Args:
            player: pacman position

        """
        player.respawn()
        for i in self.ghosts:
            i.respawn()

    def _check_collision(self, player: Pacman, cheat_mode: CheatMode) -> None:

        for i in self.ghosts:
            if i.position == player.position:
                if (
                    i.state == GhostState.CHASING
                    and cheat_mode.invincible == False
                ):
                    self._reset_position(player)
                    player.lost_life()
                    break
                elif i.state == GhostState.EDIBLE:
                    i.get_eaten()

    def is_complete(self) -> bool:
        """Check if the game is finished correctly by eaten all pacgums"""
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
        if player.remaining_lives == 0:
            return True

        if self.time_remaining <= 0:
            return True
        return False

    def update(self, dt: float, player: Pacman, cheat_mode: CheatMode) -> None:
        """Update the level action state and flow by update the pacman, ghosts
        Args:
            dt: Time of indivisual frame in second
            player: Pacman position
            cheat_mode: CheatMode instance

        """
        self.time_remaining -= dt

        player.update(dt, cheat_mode.speed_multiplier)

        for i in self.ghosts:
            i.update(dt, player._position, self.maze, cheat_mode.ghosts_frozen)

        self._check_collision(player, cheat_mode)

    @property
    def time_remaining(self):
        return self._time_remaining

    @time_remaining.setter
    def time_remaining(self, value: float):
        self._time_remaining -= value
