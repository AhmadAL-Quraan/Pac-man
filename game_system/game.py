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
        self.title_font = pygame.font.SysFont(None, 48)
        self.menu_font = pygame.font.SysFont(None, 36)
        self.hud_font = pygame.font.SysFont(None, 32)
        self.brand_font = pygame.font.SysFont(None, 76)
        self.status_font = pygame.font.SysFont(None, 24)
        self._level_index = 0
        self.menu_page = "main"
        self.menu_selection = 0
        self.menu_button_rects: list[pygame.Rect] = []
        self.running = False

        # Tracking variables for the Game Over / Name Entry screen
        self.player_name_input: str = ""
        self.won_last_game: bool = False

    def run(self) -> None:
        """Main game loop — owns the pygame event/render cycle."""
        self.running = True
        while self.running:
            dt: float = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.handle_input(event)

            self._update(dt)
            self._render()

        pygame.quit()

    def _render_menu(self) -> None:
        self.screen.fill((7, 18, 24))
        panel = pygame.Rect(
            32, 32, self.screen.get_width() - 64, self.screen.get_height() - 64
        )
        pygame.draw.rect(self.screen, (10, 35, 42), panel)
        pygame.draw.rect(self.screen, (36, 190, 174), panel, 2)

        title = self.brand_font.render("PAC-MAN", True, (255, 211, 52))
        self.screen.blit(title, title.get_rect(center=(panel.centerx, 112)))
        subtitle = self.menu_font.render(
            "A MAZE OF YOUR OWN MAKING", True, (134, 245, 207)
        )
        self.screen.blit(subtitle, subtitle.get_rect(center=(panel.centerx, 164)))
        pygame.draw.line(
            self.screen,
            (36, 190, 174),
            (panel.left + 40, 200),
            (panel.right - 40, 200),
            2,
        )

        self.menu_button_rects = []
        if self.menu_page == "main":
            options = ("Start Game", "High Scores", "Controls", "Quit")
            button_width = min(440, panel.width - 64)
            button_height = 58
            gap = 16
            for index, label in enumerate(options):
                rect = pygame.Rect(
                    panel.centerx - button_width // 2,
                    228 + index * (button_height + gap),
                    button_width,
                    button_height,
                )
                selected = index == self.menu_selection
                pygame.draw.rect(
                    self.screen,
                    (30, 103, 103) if selected else (13, 51, 58),
                    rect,
                )
                pygame.draw.rect(
                    self.screen,
                    (255, 211, 52) if selected else (36, 112, 112),
                    rect,
                    2,
                )
                text = self.menu_font.render(
                    label, True, (255, 241, 192) if selected else (200, 224, 216)
                )
                self.screen.blit(text, text.get_rect(center=rect.center))
                self.menu_button_rects.append(rect)

            hint = self.status_font.render(
                "UP / DOWN SELECT     ENTER CHOOSE",
                True,
                (134, 174, 169),
            )
            self.screen.blit(
                hint, hint.get_rect(center=(panel.centerx, panel.bottom - 44))
            )
            return

        if self.menu_page == "scores":
            heading = self.title_font.render("HIGH SCORES", True, (255, 211, 52))
            self.screen.blit(heading, heading.get_rect(center=(panel.centerx, 242)))
            scores = self.score_storage.show_top()
            if not scores:
                scores = [("No scores yet", 0)]
            for index, (name, score) in enumerate(scores[:10]):
                text = self.menu_font.render(
                    f"{index + 1:>2}. {name}  -  {score}",
                    True,
                    (220, 236, 223),
                )
                self.screen.blit(text, (panel.centerx - 160, 284 + index * 34))
        else:
            heading = self.title_font.render("CONTROLS", True, (255, 211, 52))
            self.screen.blit(heading, heading.get_rect(center=(panel.centerx, 242)))
            controls = (
                "Move: Arrow keys or W A S D",
                "Pause / resume: P",
                "Toggle cheat mode: C during a game",
                "With cheats enabled: I invincible, F freeze ghosts",
                "K skip level, L extra life, O increase speed",
            )
            for index, label in enumerate(controls):
                text = self.status_font.render(label, True, (220, 236, 223))
                self.screen.blit(
                    text,
                    text.get_rect(center=(panel.centerx, 302 + index * 38)),
                )

        back_hint = self.status_font.render("ESC TO RETURN", True, (134, 174, 169))
        self.screen.blit(
            back_hint,
            back_hint.get_rect(center=(panel.centerx, panel.bottom - 44)),
        )

    def _activate_menu_selection(self) -> None:
        if self.menu_page != "main":
            return
        if self.menu_selection == 0:
            self.start_new_game()
        elif self.menu_selection == 1:
            self.menu_page = "scores"
        elif self.menu_selection == 2:
            self.menu_page = "controls"
        else:
            self.running = False

    def _return_to_menu(self) -> None:
        self.state = GameState.MENU
        self.menu_page = "main"
        self.menu_selection = 0
        self.screen = pygame.display.set_mode((800, 800))

    def _handle_menu_input(self, event: pygame.event.Event) -> None:
        if self.menu_page != "main":
            if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                self.menu_page = "main"
                self.menu_selection = 0
            return
        if event.key == pygame.K_UP:
            self.menu_selection = (self.menu_selection - 1) % 4
        elif event.key == pygame.K_DOWN:
            self.menu_selection = (self.menu_selection + 1) % 4
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self._activate_menu_selection()

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
            self._render_menu()

        elif self.state == GameState.ENTERING_NAME:
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

            title = self.title_font.render(msg, True, color)
            score_text = self.title_font.render(
                f"Final Score: {final_score}", True, (255, 255, 255)
            )
            prompt = self.title_font.render(
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

            hud_y = self.current_level.maze.height * self.config.CELL_SIZE
            hud_left = 12
            hud_right = self.screen.get_width() // 2
            pygame.draw.rect(
                self.screen,
                (7, 18, 24),
                (0, hud_y, self.screen.get_width(), self.screen.get_height() - hud_y),
            )
            pygame.draw.line(
                self.screen,
                (36, 112, 112),
                (0, hud_y),
                (self.screen.get_width(), hud_y),
                2,
            )

            assert self.player is not None
            assert self.current_level is not None
            score_txt = self.status_font.render(
                f"Score: {self.player.score}", True, (220, 236, 223)
            )
            lives_txt = self.status_font.render(
                f"Lives: {self.player.remaining_lives}", True, (220, 236, 223)
            )
            time_txt = self.status_font.render(
                f"Time: {int(self.current_level.time_remaining)}",
                True,
                (220, 236, 223),
            )
            lvl_txt = self.status_font.render(
                f"Level: {self.current_level.level_number}",
                True,
                (255, 211, 52),
            )
            cheats_txt = self.status_font.render(
                f"Cheats: {'ON' if self.cheat_mode.enabled else 'OFF'} (C)",
                True,
                (134, 245, 207) if self.cheat_mode.enabled else (134, 174, 169),
            )

            self.screen.blit(score_txt, (hud_left, hud_y + 5))
            self.screen.blit(lives_txt, (hud_right, hud_y + 5))
            self.screen.blit(lvl_txt, (hud_left, hud_y + 27))
            self.screen.blit(time_txt, (hud_right, hud_y + 27))
            self.screen.blit(cheats_txt, (hud_left, hud_y + 49))

        elif self.state == GameState.PAUSED:
            text = self.title_font.render(
                "PAUSED - Press P to Resume", True, (255, 255, 255)
            )
            text_rect = text.get_rect(
                center=(
                    self.screen.get_width() // 2,
                    self.screen.get_height() // 2,
                )
            )
            self.screen.blit(text, text_rect)

        elif self.state == GameState.VICTORY:
            text = self.title_font.render(
                "ALL MAZES CLEARED! Press ENTER", True, (255, 211, 52)
            )
            self.screen.blit(
                text,
                text.get_rect(
                    center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
                ),
            )

        pygame.display.flip()

    def start_new_game(self) -> None:
        """Start a fresh game: reset player/score, build level 1."""
        self._level_index = 0
        self.cheat_mode = CheatMode()
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
        if self.state == GameState.MENU and event.type == pygame.MOUSEMOTION:
            if self.menu_page == "main":
                for index, rect in enumerate(self.menu_button_rects):
                    if rect.collidepoint(event.pos):
                        self.menu_selection = index
                        break
            return

        if self.state == GameState.MENU and event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_page == "main" and event.button == 1:
                for index, rect in enumerate(self.menu_button_rects):
                    if rect.collidepoint(event.pos):
                        self.menu_selection = index
                        self._activate_menu_selection()
                        break
            return

        if event.type != pygame.KEYDOWN:
            return

        if self.state == GameState.MENU:
            self._handle_menu_input(event)
            return

        if self.state == GameState.VICTORY:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._return_to_menu()
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
                self._return_to_menu()
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
            elif event.key == pygame.K_c:
                self.cheat_mode.toggle_enabled()
            elif event.key == pygame.K_i and self.cheat_mode.enabled:
                self.cheat_mode.toggle_invincibility()
            elif event.key == pygame.K_f and self.cheat_mode.enabled:
                self.cheat_mode.toggle_ghosts_freeze()
            elif event.key == pygame.K_k and self.cheat_mode.enabled:
                self.cheat_mode.skip_level(self)
            elif event.key == pygame.K_l and self.cheat_mode.enabled:
                self.cheat_mode.add_life(self.player)
            elif event.key == pygame.K_o and self.cheat_mode.enabled:
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

        hud_height = 78

        new_width = maze_width * cell_size
        new_height = (maze_height * cell_size) + hud_height

        self.screen = pygame.display.set_mode((new_width, new_height))

    @staticmethod
    def _level_center(maze: Maze) -> tuple[int, int]:
        """Return the (x, y) cell at the middle of the given maze."""
        return (maze.height // 2, maze.width // 2)
