from dataclasses import dataclass
from mazegenerator import MazeGenerator
from pacman.direction import Direction
from pacman import direction


@dataclass
class Maze:
    width: int
    height: int
    seed: int

    def load_from_amazing(self) -> None:
        """Load the maze cells values from the mazegenerator"""
        maze: MazeGenerator = MazeGenerator(
            (self.width, self.height), False, (0, 0), (-1, -1), self.seed
        )
        self.raw_grid = maze._maze

    def has_wall(
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

        x, y = position
        num: int = self.raw_grid[x][y]
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

        if self.has_wall(position, direction) == True:
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

    def all_positions(self) -> list[tuple[int, int]]:
        """Return every (x, y) coordinate in the maze grid.

        Returns:
            A flat list of every (x, y) position, row by row.
        """
        return [(x, y) for x in range(self.height) for y in range(self.width)]

    def is_wall(self, position: tuple[int, int]) -> bool:
        """Return True if this cell is a solid wall (unplaceable), not a
        corridor cell where a pacgum or entity can sit.

        Args:
            position: (x, y) coordinates to check.

        Returns:
            True if the cell is the outer border wall, False if it's open.
        """
        x, y = position
        return x == 0 or y == 0 or x == self.height - 1 or y == self.width - 1
