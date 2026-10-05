from dataclasses import dataclass, field
import pygame
import config
from pacman.pacman import Pacman
from .maze import Maze
from .ghost import Ghost
from .pacgum import Pacgum
from .ghost_state import GhostState
from game_system.cheat_mode import CheatMode
from config import Config
from pacman.direction import Direction


@dataclass
class Level:
    maze: Maze
    ghosts: list[Ghost]
    pacgums: dict[tuple[int, int], Pacgum]
    time_remaining: float
    level_number: int
    config: Config
    _maze_surface: pygame.Surface = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Pre-render maze walls, which remain unchanged during a level."""
        cell_size = Config.CELL_SIZE
        self._maze_surface = pygame.Surface(
            (self.maze.width * cell_size, self.maze.height * cell_size)
        )
        self._maze_surface.fill((0, 0, 0))

        wall_color = (33, 33, 255)
        for row, col in self.maze.all_positions():
            position = (row, col)
            px = col * cell_size
            py = row * cell_size

            if self.maze.has_wall(position, Direction.UP):
                pygame.draw.line(
                    self._maze_surface,
                    wall_color,
                    (px, py),
                    (px + cell_size, py),
                    2,
                )
            if self.maze.has_wall(position, Direction.DOWN):
                pygame.draw.line(
                    self._maze_surface,
                    wall_color,
                    (px, py + cell_size),
                    (px + cell_size, py + cell_size),
                    2,
                )
            if self.maze.has_wall(position, Direction.LEFT):
                pygame.draw.line(
                    self._maze_surface,
                    wall_color,
                    (px, py),
                    (px, py + cell_size),
                    2,
                )
            if self.maze.has_wall(position, Direction.RIGHT):
                pygame.draw.line(
                    self._maze_surface,
                    wall_color,
                    (px + cell_size, py),
                    (px + cell_size, py + cell_size),
                    2,
                )

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the maze, pacgums, and ghosts."""
        cell_size = Config.CELL_SIZE
        screen.blit(self._maze_surface, (0, 0))

        # Draw Pacgums
        for pos, pacgum in self.pacgums.items():
            if not pacgum.eaten:
                row, col = pos
                # Calculate the exact center of the cell
                center_x = col * cell_size + cell_size // 2
                center_y = row * cell_size + cell_size // 2

                # Make super pacgums larger
                radius = 8 if pacgum.is_super else 4
                pygame.draw.circle(
                    screen, (255, 255, 102), (center_x, center_y), radius
                )

        # Draw Ghosts
        for ghost in self.ghosts:
            row, col = ghost.position

            # Draw ghosts slightly smaller than the cell bounds so they fit nicely
            rect = pygame.Rect(
                col * cell_size + 4,
                row * cell_size + 4,
                cell_size - 8,
                cell_size - 8,
            )

            # Assign colors based on the current state of the ghost
            if ghost.state == GhostState.CHASING:
                color = (255, 0, 0)  # Red (Dangerous)
            elif ghost.state == GhostState.EDIBLE:
                color = (0, 0, 255)  # Blue (Can be eaten)
            elif ghost.state == GhostState.EATEN:
                color = (100, 100, 100)  # Gray (Returning to spawn)
            else:
                color = (255, 255, 255)  # Fallback

            pygame.draw.rect(screen, color, rect)

    def _reset_position(self, player: Pacman) -> None:
        """Reset the position of all entities when the game start or resets.

        Args:
            player: pacman position

        """
        player.respawn()
        for i in self.ghosts:
            i.respawn()

    def check_collision(self, player: Pacman, cheat_mode: CheatMode) -> None:

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

    def check_eaten_pacgums(self, player: Pacman):

        pacgum_position = self.pacgums.get(
            player.position, Pacgum((-1, -1), False, False)
        )
        if pacgum_position.position == (-1, -1):
            return
        if pacgum_position.is_super == False:
            if not pacgum_position.eaten:
                pacgum_position.eaten = True
                player.add_points(self.config.points_per_pacgum)

        if pacgum_position.is_super == True:
            if not pacgum_position.eaten:
                pacgum_position.eaten = True
                player.add_points(self.config.points_per_super_pacgum)
                for i in self.ghosts:
                    i.become_edible()

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

        player.update(dt, cheat_mode.speed_multiplier, self.maze)

        for i in self.ghosts:
            i.update(dt, player._position, self.maze, cheat_mode.ghosts_frozen)

        self.check_collision(player, cheat_mode)
        self.check_eaten_pacgums(player)
