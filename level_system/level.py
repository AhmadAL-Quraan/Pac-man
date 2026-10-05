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
        self._maze_surface.fill((7, 18, 24))

        def draw_wall(start: tuple[int, int], end: tuple[int, int]) -> None:
            pygame.draw.line(self._maze_surface, (10, 57, 67), start, end, 8)
            pygame.draw.line(self._maze_surface, (36, 190, 174), start, end, 4)
            pygame.draw.line(
                self._maze_surface, (134, 245, 207), start, end, 1
            )

        for row, col in self.maze.all_positions():
            position = (row, col)
            px = col * cell_size
            py = row * cell_size

            if self.maze.has_wall(position, Direction.UP):
                draw_wall((px, py), (px + cell_size, py))
            if self.maze.has_wall(position, Direction.DOWN):
                draw_wall(
                    (px, py + cell_size), (px + cell_size, py + cell_size)
                )
            if self.maze.has_wall(position, Direction.LEFT):
                draw_wall((px, py), (px, py + cell_size))
            if self.maze.has_wall(position, Direction.RIGHT):
                draw_wall(
                    (px + cell_size, py), (px + cell_size, py + cell_size)
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

                if pacgum.is_super:
                    pygame.draw.circle(
                        screen, (255, 126, 104), (center_x, center_y), 9, 2
                    )
                    pygame.draw.circle(
                        screen, (255, 231, 166), (center_x, center_y), 4
                    )
                else:
                    pygame.draw.circle(
                        screen, (246, 238, 184), (center_x, center_y), 3
                    )

        # Draw Ghosts
        ghost_colors = (
            (246, 91, 119),
            (66, 205, 207),
            (255, 157, 84),
            (181, 135, 245),
        )
        for ghost_index, ghost in enumerate(self.ghosts):
            row, col = ghost.position
            center_x = col * cell_size + cell_size // 2
            top = row * cell_size + 3
            eye_y = top + 12

            if ghost.state == GhostState.EATEN:
                for eye_x in (center_x - 4, center_x + 4):
                    pygame.draw.ellipse(
                        screen, (242, 249, 239), (eye_x - 3, eye_y - 4, 6, 9)
                    )
                    pygame.draw.circle(
                        screen, (51, 159, 221), (eye_x, eye_y), 2
                    )
                continue

            if ghost.state == GhostState.EDIBLE:
                color = (65, 142, 229)
                pupil_color = (42, 97, 181)
            else:
                color = ghost_colors[ghost_index % len(ghost_colors)]
                pupil_color = (29, 39, 53)

            pygame.draw.circle(screen, color, (center_x, top + 10), 11)
            pygame.draw.rect(screen, color, (center_x - 11, top + 10, 22, 12))
            for foot_x in (center_x - 7, center_x, center_x + 7):
                pygame.draw.circle(screen, (7, 18, 24), (foot_x, top + 22), 4)

            for eye_x in (center_x - 4, center_x + 4):
                pygame.draw.ellipse(
                    screen, (248, 250, 235), (eye_x - 3, eye_y - 4, 6, 9)
                )
                pygame.draw.circle(screen, pupil_color, (eye_x + 1, eye_y), 2)

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
                player.change_pacman_speed(0.140)

    def is_complete(self) -> bool:
        """Return whether every pacgum in the level has been eaten."""
        return all(pacgum.eaten for pacgum in self.pacgums.values())

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
            i.update(
                dt,
                player._position,
                self.maze,
                player,
                cheat_mode.ghosts_frozen,
            )

        self.check_collision(player, cheat_mode)
        self.check_eaten_pacgums(player)
