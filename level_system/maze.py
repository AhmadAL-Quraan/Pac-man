from dataclasses import dataclass
from mazegenerator import MazeGenerator


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
        print(self.raw_grid)

    def _has_wall(self, position: tuple[int, int], direction: str) -> bool:
        """Return True if the position has a close direction, False otherwise

        Args:
            position: the index of the cell -> tuple[int,int]
            direction: "north","south","east","west"
        return:
            True if it's 1 means wall.
            False otherwise.
        """
        if (
            position[0] < 0
            or position[1] < 0
            or position[0] >= self.width
            or position[1] >= self.height
        ):
            return False
        num: int = self.raw_grid[position[0]][position[1]]
        if direction == "north":
            return True if num & (1 << 0) else False
        if direction == "south":
            return True if num & (1 << 2) else False
        if direction == "east":
            return True if num & (1 << 1) else False
        if direction == "west":
            return True if num & (1 << 3) else False
        return False

    def can_move(self, position: tuple[int, int], direction: str) -> bool:
        if self._has_wall(position, direction) == True:
            return False
        return True

    def get_neighbors(
        self, position: tuple[int, int]
    ) -> list[tuple[int, int]]:
        neighbors: list[tuple[int, int]] = []
        dx = [1, -1, 0, 0]
        dy = [0, 0, 1, -1]
        directions: list[str] = ["north", "east", "south", "west"]
        for i in range(4):
            new_x = position[0] + dx[i]
            new_y = position[1] + dy[i]
            if self.can_move((new_x, new_y), directions[i]):
                neighbors.append((new_x, new_y))
