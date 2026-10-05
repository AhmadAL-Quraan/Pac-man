import random
import sys

import pygame

from .game_state import GameState
from game_system.cheat_mode import CheatMode
from level_system.ghost import Ghost, GhostState
from level_system.level import Level
from level_system.maze import Maze
from level_system.pacgum import Pacgum
from pacman.direction import Direction
from pacman.pacman import Pacman
from config import Config
from score_system.player_score import PlayerScore


class Game:
    """Owns the pygame window, the game loop, and top-level game state.

    Attributes:
        config: The loaded, validated game configuration.
        player: The current Pacman instance, or None before a game starts.
        current_level: The current Level instance, or None before a game starts.
        state: The current high-level game state (menu, playing, etc.).
        score_storage: Handles loading/saving the persistent highscore list.
        cheat_mode: Tracks cheat toggles (invincibility, speed, etc.).
        screen: The pygame display surface.
        clock: The pygame clock, used to cap the frame rate and compute dt.
    """

    def __init__(self, config: Config) -> None:
        """Initializes pygame and the game's starting state."""
        pygame.init()

        self.config = config
        self.player: Pacman | None = None
        self.current_level: Level | None = None
        self.state: GameState = GameState.MENU
        self.score_storage: PlayerScore = PlayerScore(
            config.highscore_filename
        )
        self.cheat_mode: CheatMode = CheatMode()
        self.screen: pygame.Surface = pygame.display.set_mode((800, 800))
        self.clock = pygame.time.Clock()
        self._level_index = 0

        # Tracking variables for the Game Over / Name Entry screen
        self.player_name_input: str = ""
        self.won_last_game: bool = False

    def run(self) -> None:
        """Main game loop — owns the pygame event/render cycle."""
        running = True
        while running:
            dt: float = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.handle_input(event)

            self._update(dt)
            self._render()

        pygame.quit()

    def _update(self, dt: float) -> None:
        """Advance game logic by dt seconds, depending on the current state."""
        if self.state != GameState.PLAYING:
            return

        assert self.player is not None
        assert self.current_level is not None

        self.current_level.update(dt, self.player, self.cheat_mode)

        if self.current_level.check_failed(self.player):
            self.end_game(won=False)
        elif self.current_level.is_complete():
            self.load_next_level()

    def _render(self) -> None:
        """Draw the current frame based on game state."""
        self.screen.fill((0, 0, 0))

        if self.state == GameState.MENU:
            font = pygame.font.SysFont(None, 48)
            title = font.render(
                "Pac-Man: Press SPACE to Start", True, (255, 255, 0)
            )
            self.screen.blit(title, (50, 50))

            small_font = pygame.font.SysFont(None, 36)
            hs_title = small_font.render(
                "Top 10 Highscores:", True, (255, 255, 255)
            )
            self.screen.blit(hs_title, (50, 120))

            for i, (name, score) in enumerate(self.score_storage.show_top()):
                score_text = small_font.render(
                    f"{i+1}. {name} - {score} pts", True, (200, 200, 200)
                )
                self.screen.blit(score_text, (50, 160 + (i * 30)))

        elif self.state == GameState.ENTERING_NAME:
            font = pygame.font.SysFont(None, 48)
            msg = (
                "VICTORY!"
                if getattr(self, "won_last_game", False)
                else "GAME OVER!"
            )
            color = (
                (0, 255, 0)
                if getattr(self, "won_last_game", False)
                else (255, 0, 0)
            )

            # Safely get the score to satisfy Pyright
            final_score = self.player.score if self.player is not None else 0

            title = font.render(msg, True, color)
            score_text = font.render(
                f"Final Score: {final_score}", True, (255, 255, 255)
            )
            prompt = font.render(
                f"Enter Name (Press Enter): {self.player_name_input}_",
                True,
                (255, 255, 0),
            )

            self.screen.blit(title, (50, 50))
            self.screen.blit(score_text, (50, 120))
            self.screen.blit(prompt, (50, 190))

        elif (
            self.state == GameState.PLAYING and self.current_level is not None
        ):
            self.current_level.draw(self.screen)
            if self.player is not None:
                self.player.draw(self.screen)

            # Draw In-Game HUD at the bottom of the screen
            hud_y = self.current_level.maze.height * self.config.CELL_SIZE + 15
            font = pygame.font.SysFont(None, 32)

            assert self.player is not None
            assert self.current_level is not None
            score_txt = font.render(
                f"Score: {self.player.score}", True, (255, 255, 255)
            )
            lives_txt = font.render(
                f"Lives: {self.player.remaining_lives}", True, (255, 255, 255)
            )
            time_txt = font.render(
                f"Time: {int(self.current_level.time_remaining)}",
                True,
                (255, 255, 255),
            )
            lvl_txt = font.render(
                f"Level: {self.current_level.level_number}",
                True,
                (255, 255, 255),
            )

            self.screen.blit(score_txt, (20, hud_y))
            self.screen.blit(lives_txt, (200, hud_y))
            self.screen.blit(time_txt, (350, hud_y))
            self.screen.blit(lvl_txt, (500, hud_y))

        elif self.state == GameState.PAUSED:
            font = pygame.font.SysFont(None, 48)
            text = font.render(
                "PAUSED - Press P to Resume", True, (255, 255, 255)
            )
            text_rect = text.get_rect(
                center=(
                    self.screen.get_width() // 2,
                    self.screen.get_height() // 2,
                )
            )
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def start_new_game(self) -> None:
        """Start a fresh game: reset player/score, build level 1."""
        self._level_index = 0
        self.current_level = self._build_level(self._level_index)
        self._resize_screen_for_level()

        center = self._level_center(self.current_level.maze)
        self.player = Pacman(start_position=center)

        self.state = GameState.PLAYING

    def load_next_level(self) -> None:
        """Advance to the next level, or declare victory if that was
        the last one. Keeps the same Pacman (score/lives persist)."""
        assert self.player is not None

        self._level_index += 1
        if self._level_index >= len(self.config.levels_hight_width):
            self.state = GameState.VICTORY
            return

        self.current_level = self._build_level(self._level_index)
        self._resize_screen_for_level()
        center: tuple[int, int] = self._level_center(self.current_level.maze)
        self.player.start_position = center
        self.player.respawn()

    def pause(self) -> None:
        """Pause the game if currently playing."""
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED

    def resume(self) -> None:
        """Resume the game if currently paused."""
        if self.state == GameState.PAUSED:
            self.state = GameState.PLAYING

    def end_game(self, won: bool) -> None:
        """End the current game and move to the name entry state."""
        self.won_last_game = won
        self.player_name_input = ""
        self.state = GameState.ENTERING_NAME

    def handle_input(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        if self.state == GameState.MENU:
            if event.key == pygame.K_SPACE:
                self.start_new_game()
            return

        if self.state == GameState.ENTERING_NAME:
            # Handle typing name and saving
            assert self.player is not None
            if event.key == pygame.K_RETURN:
                name = self.player_name_input.strip()
                if name == "":
                    name = "Unknown"
                # Save the score and return to menu
                self.score_storage.add_score(name, self.player.score)
                self.score_storage.save()
                self.state = GameState.MENU
            elif event.key == pygame.K_BACKSPACE:
                self.player_name_input = self.player_name_input[:-1]
            else:
                # Max 10 chars, alphanumeric and spaces only
                if len(self.player_name_input) < 10 and (
                    event.unicode.isalnum() or event.unicode == " "
                ):
                    self.player_name_input += event.unicode
            return

        # ... (Keep your existing PLAYING and PAUSED checks here) ...
        if self.state == GameState.PLAYING:
            assert self.player is not None
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.player.set_direction(Direction.UP)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.player.set_direction(Direction.DOWN)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.player.set_direction(Direction.LEFT)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.player.set_direction(Direction.RIGHT)
            elif event.key == pygame.K_p:
                self.pause()
            elif event.key == pygame.K_i:
                self.cheat_mode.toggle_invincibility()
            elif event.key == pygame.K_f:
                self.cheat_mode.toggle_ghosts_freeze()
            elif event.key == pygame.K_k:
                self.cheat_mode.skip_level(self)
            elif event.key == pygame.K_l:
                self.cheat_mode.add_life(self.player)
            elif event.key == pygame.K_o:
                self.cheat_mode.increase_speed()
            return

        if self.state == GameState.PAUSED:
            if event.key == pygame.K_p:
                self.resume()
            return

    def _build_level(self, level_index: int) -> Level:
        # ... (Keep the beginning of the method exactly the same) ...
        level_data = self.config.levels_hight_width[level_index]
        width = level_data["width"]
        height = level_data["height"]
        seed = self.config.seed if level_index == 0 else 0

        maze_obj = Maze(width, height, seed)
        maze_obj.load_from_amazing()

        corners: list[tuple[int, int]] = [
            (1, 1),
            (1, width - 2),
            (height - 2, 1),
            (height - 2, width - 2),
        ]
        ghost_list = [
            Ghost(
                position=corner,
                corner=corner,
                state=GhostState.CHASING,
                state_timer=0.0,
            )
            for corner in corners
        ]

        # Pass the corners to generate the Super Pacgums
        pacgums = self._place_pacgums(maze_obj, self.config.pacgum, corners)

        return Level(
            maze=maze_obj,
            ghosts=ghost_list,
            pacgums=pacgums,
            level_number=level_index + 1,
            time_remaining=float(self.config.level_max_time),
            config=self.config,
        )

    @staticmethod
    def _place_pacgums(
        maze: Maze, count: int, corners: list[tuple[int, int]]
    ) -> dict[tuple[int, int], Pacgum]:
        """Place 4 super pacgums in corners, then scatter regular pacgums."""
        pacgums = {}

        # 1. Place Super Pacgums in the corners
        for corner in corners:
            if not maze.is_wall(corner):
                pacgums[corner] = Pacgum(
                    position=corner, eaten=False, is_super=True
                )

        # 2. Place regular pacgums in remaining corridors
        corridors = [
            pos
            for pos in maze.all_positions()
            if not maze.is_wall(pos)
            and pos not in pacgums
            and not maze.pattern_42_wall(pos)
        ]
        actual_count = min(count, len(corridors))
        chosen = random.sample(corridors, actual_count)

        for pos in chosen:
            pacgums[pos] = Pacgum(position=pos, eaten=False, is_super=False)

        return pacgums

    def _resize_screen_for_level(self) -> None:
        """Resizes the pygame window to perfectly fit the current maze and HUD."""
        if self.current_level is None:
            return

        cell_size = self.config.CELL_SIZE
        maze_width = self.current_level.maze.width
        maze_height = self.current_level.maze.height

        hud_height = 60  # Extra space at the bottom for the HUD

        new_width = maze_width * cell_size
        new_height = (maze_height * cell_size) + hud_height

        self.screen = pygame.display.set_mode((new_width, new_height))

    @staticmethod
    def _level_center(maze: Maze) -> tuple[int, int]:
        """Return the (x, y) cell at the middle of the given maze."""
        return (maze.height // 2, maze.width // 2)
