from dataclasses import dataclass
from mazegenerator import MazeGenerator
from ..pacman.direction import Direction
from pacman import direction


@dataclass
class Maze:
    raw_grid: list[list[int]]
    width: int
    height: int
    seed: int

    def load_from_amazing(self) -> None:
        """Load the maze cells values from the mazegenerator"""
        maze: MazeGenerator = MazeGenerator(
            (self.width, self.height), False, (0, 0), (-1, -1), self.seed
        )
        self.raw_grid = maze._maze

    def _has_wall(
        self, position: tuple[int, int], direction: Direction
    ) -> bool:
        """Return True if the position has a close direction, False otherwise

        Args:
            position: the index of the cell -> tuple[int,int]
            direction: "north","south","east","west"
        return:
            True if it's 1 means wall.
            False otherwise.
        """
        num: int = self.raw_grid[position[0]][position[1]]
        if direction.name == "UP":
            return True if num & (1 << 0) else False
        if direction.name == "DOWN":
            return True if num & (1 << 2) else False
        if direction.name == "RIGHT":
            return True if num & (1 << 1) else False
        if direction.name == "LEFT":
            return True if num & (1 << 3) else False
        return False

    def can_move(
        self, position: tuple[int, int], direction: Direction
    ) -> bool:
        if (
            position[0] < 0
            or position[1] < 0
            or position[0] >= self.height
            or position[1] >= self.width
        ):
            print(f"Warning, the position is out of index {position}")
            return False

        if self._has_wall(position, direction) == True:
            return False
        return True

    def get_neighbors(
        self, position: tuple[int, int]
    ) -> list[tuple[int, int]]:
        neighbors: list[tuple[int, int]] = []
        directions: list[Direction] = [
            Direction.UP,
            Direction.RIGHT,
            Direction.DOWN,
            Direction.LEFT,
        ]
        for i in range(4):
            if self.can_move(position, directions[i]):
                neighbors.append(
                    (
                        position[0] + directions[i].value[0],
                        position[1] + directions[i].value[1],
                    )
                )

        return neighbors
