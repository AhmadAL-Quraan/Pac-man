from dataclasses import dataclass
from .ghost_state import GhostState
from .maze import Maze


@dataclass()
class Ghost:
    position: tuple[int, int]
    corner: tuple[int, int]
    state: GhostState
    # How much time before the ghost stop being ediable
    state_timer: float
    move_timer: float
    _move_interval: float = 0.2

    def update(
        self,
        dt: float,
        player_position: tuple[int, int],
        maze: Maze,
        frozen: bool,
    ) -> None:
        """update the state of the ghost at each frame

        Args:
            dt: How much real time (in seconds) passed since the last frame.
            player_position: Countdown to how much time a ghost stays in its current state (like "edible")
            frozen: The cheatmode status
        """

        self.state_timer -= dt
        if self.state_timer <= 0 and self.state == GhostState.EDIBLE:
            self.state = GhostState.CHASING

        if frozen:
            return

        if self.move_timer < self._move_interval:
            return

        self.move_timer -= self._move_interval

        if self.state == GhostState.CHASING:
            self.position = bfs_next_step(maze, self.position, player_position)
        elif self.state == GhostState.EDIBLE:
            self.position = self._flee_step(maze, player_position)
