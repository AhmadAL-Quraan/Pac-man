from dataclasses import dataclass, field

from pacman.pacman import Pacman
from .ghost_state import GhostState
from .maze import Maze
from collections import deque


@dataclass
class Ghost:
    """Class representing Ghost."""

    position: tuple[int, int]
    state: GhostState
    # How much time before the ghost stop being ediable
    # How much time after to respawn after gets eaten
    state_timer: float
    corner: tuple[int, int]
    """
      The running total of accumulated `dt's`, checked against
      `_move_interval`, each frame to decide whether enough time has passed
      for the ghost to take its next step. So basically move player a step
      every x seconds.
    """
    # Every value here is in seconds
    move_timer: float = 0
    _move_interval: float = 0.6
    EDIBLE_DURATION_SECONDS: float = 5.0
    EATEN_DURATION_SECONDS: float = 5.0
    _render_position: tuple[float, float] = field(init=False, repr=False)
    _planned_key: tuple[tuple[int, int], GhostState] | None = field(
        default=None, init=False, repr=False
    )
    _planned_step: tuple[int, int] | None = field(
        default=None, init=False, repr=False
    )

    def __post_init__(self) -> None:
        self._render_position = (
            float(self.position[0]),
            float(self.position[1]),
        )

    #
    def _flee_step(
        self, maze: Maze, player_position: tuple[int, int]
    ) -> tuple[int, int]:
        """Determines the next step to flee away from the player.
        Simulate the state of the ghost on each neighbor cell"""
        neighbors = maze.get_neighbors(self.position)

        if not neighbors:
            return self.position

        best_step = self.position
        max_distance = -1

        for neighbor in neighbors:
            # We don't care about the 'next step' *from* the neighbor,
            # we only care about how far that neighbor is from the player.
            _, distance = self._bfs(maze, neighbor, player_position)

            if distance > max_distance:
                max_distance = distance
                best_step = neighbor

        return best_step

    def _bfs(
        self, maze: Maze, start: tuple[int, int], goal: tuple[int, int]
    ) -> tuple[tuple[int, int], int]:
        """Finds both the next tile to move to and total distance to goal.

        Returns:
            A tuple of (next_step_coordinate, total_distance_in_steps)
        """
        if start == goal:
            return start, 0

        came_from: dict[tuple[int, int], tuple[int, int]] = {start: (-1, -1)}
        queue = deque([start])

        while queue:
            current = queue.popleft()

            if current == goal:
                break

            for neighbor in maze.get_neighbors(current):
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    queue.append(neighbor)

        if goal not in came_from:
            return start, 999999  # No path exists

        distance = 0
        step = goal

        # Child: parent
        # step-child : came_from[step] - parent
        while came_from[step] != start:
            step = came_from[step]
            distance += 1

        distance += 1

        return (
            step,
            distance,
        )

    def _next_step(
        self, maze: Maze, player_position: tuple[int, int]
    ) -> tuple[int, int]:
        key = (self.position, self.state)
        if key != self._planned_key:
            if self.state == GhostState.CHASING:
                self._planned_step, _ = self._bfs(
                    maze, self.position, player_position
                )
            elif self.state == GhostState.EDIBLE:
                self._planned_step = self._flee_step(maze, player_position)
            else:
                self._planned_step = self.position
            self._planned_key = key

        return self._planned_step or self.position

    def update(
        self,
        dt: float,
        player_position: tuple[int, int],
        maze: Maze,
        player: Pacman,
        frozen: bool,
    ) -> None:
        """update the state of the ghost at each frame

        Args:
            dt: How much real time (in seconds) passed since the last frame.
            player_position: Countdown to how much time a ghost stays in its
                current state (like "edible").
            frozen: A cheat_mode option that freezes ghosts
        """

        if frozen:
            return
        if self.state in (GhostState.EATEN, GhostState.EDIBLE):
            self.state_timer -= dt
            if self.state_timer <= 0:
                if self.state == GhostState.EATEN:
                    self.respawn()  # Sets position = corner, state = CHASING
                    return  # Fresh respawn ghost shouldn't move on revive
                elif self.state == GhostState.EDIBLE:
                    self.state = GhostState.CHASING

        self.move_timer += dt
        while self.move_timer >= self._move_interval:
            self.move_timer -= self._move_interval
            self.position = self._next_step(maze, player_position)
            self._planned_key = None

        if self.state in (GhostState.CHASING, GhostState.EDIBLE):
            target_row, target_col = self._next_step(maze, player_position)
            row, col = self.position
            progress = min(self.move_timer / self._move_interval, 1.0)
            self._render_position = (
                row + (target_row - row) * progress,
                col + (target_col - col) * progress,
            )
        else:
            self._render_position = (
                float(self.position[0]),
                float(self.position[1]),
            )

    def become_edible(self) -> None:
        """Switch the state of the ghost to edible and start counting down"""
        self.state = GhostState.EDIBLE
        self.state_timer = self.EDIBLE_DURATION_SECONDS
        self._planned_key = None

    def respawn(self) -> None:
        """respawn the ghost"""
        self.position = self.corner
        self.state = GhostState.CHASING
        self.state_timer = 0.0
        self._render_position = (
            float(self.position[0]),
            float(self.position[1]),
        )
        self._planned_key = None

    def get_eaten(self) -> None:
        """Switch to eaten state and start Countdown for respawn"""
        self.state = GhostState.EATEN
        self.state_timer = self.EATEN_DURATION_SECONDS
        self._render_position = (
            float(self.position[0]),
            float(self.position[1]),
        )
        self._planned_key = None

    @property
    def render_position(self) -> tuple[float, float]:
        return self._render_position
