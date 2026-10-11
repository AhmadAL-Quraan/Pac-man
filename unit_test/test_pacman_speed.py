import sys
import types
import unittest

try:
    import pygame  # noqa: F401
except ModuleNotFoundError:
    sys.modules["pygame"] = types.ModuleType("pygame")

from pacman.pacman import Pacman
from pacman.direction import Direction


class BlockedMaze:
    def can_move(self, position: tuple[int, int], direction: object) -> bool:
        return False


class OpenMaze:
    def can_move(self, position: tuple[int, int], direction: Direction) -> bool:
        return True


class PacmanSpeedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.pacman = Pacman((1, 1))
        self.maze = BlockedMaze()

    def test_super_pacgum_speed_is_faster_than_normal(self) -> None:
        self.pacman.activate_super_pacgum_speed()

        self.assertLess(
            self.pacman._move_interval, Pacman.DEFAULT_MOVE_INTERVAL
        )
        self.assertEqual(
            self.pacman._move_interval, Pacman.SUPER_PACGUM_MOVE_INTERVAL
        )

    def test_speed_returns_to_normal_when_boost_expires(self) -> None:
        self.pacman.activate_super_pacgum_speed()
        self.pacman.update(
            Pacman.SUPER_PACGUM_DURATION_SECONDS - 0.1, 1.0, self.maze
        )
        self.assertEqual(
            self.pacman._move_interval, Pacman.SUPER_PACGUM_MOVE_INTERVAL
        )

        self.pacman.update(0.1, 1.0, self.maze)

        self.assertEqual(
            self.pacman._move_interval, Pacman.DEFAULT_MOVE_INTERVAL
        )

    def test_reactivating_boost_refreshes_its_duration(self) -> None:
        self.pacman.activate_super_pacgum_speed()
        self.pacman.update(4.0, 1.0, self.maze)
        self.pacman.activate_super_pacgum_speed()
        self.pacman.update(4.0, 1.0, self.maze)

        self.assertEqual(
            self.pacman._move_interval, Pacman.SUPER_PACGUM_MOVE_INTERVAL
        )

    def test_respawn_restores_normal_speed(self) -> None:
        self.pacman.activate_super_pacgum_speed()
        self.pacman.respawn()

        self.assertEqual(
            self.pacman._move_interval, Pacman.DEFAULT_MOVE_INTERVAL
        )

    def test_boost_expiry_restores_custom_normal_speed(self) -> None:
        pacman = Pacman((1, 1), move_interval=0.12)
        pacman.activate_super_pacgum_speed()
        pacman.update(
            Pacman.SUPER_PACGUM_DURATION_SECONDS, 1.0, self.maze
        )

        self.assertEqual(pacman._move_interval, 0.12)

    def test_direction_changes_immediately_at_tile_center(self) -> None:
        pacman = Pacman((1, 1))

        pacman.set_direction(Direction.UP)

        self.assertEqual(pacman.direction, Direction.UP)
        pacman.update(0.01, 1.0, OpenMaze())
        self.assertLess(pacman._render_position[0], 1.0)

    def test_mid_tile_turn_stays_queued_without_snapping(self) -> None:
        pacman = Pacman((1, 1))
        pacman.update(pacman._move_interval / 2, 1.0, OpenMaze())
        position_before_turn = pacman._render_position

        pacman.set_direction(Direction.UP)

        self.assertEqual(pacman.direction, Direction.RIGHT)
        self.assertEqual(pacman._next_direction, Direction.UP)
        pacman.update(pacman._move_interval / 2, 1.0, OpenMaze())
        self.assertEqual(pacman.position, (1, 2))
        self.assertEqual(pacman._render_position, (1.0, 2.0))
        self.assertNotEqual(position_before_turn, pacman._render_position)


if __name__ == "__main__":
    unittest.main()