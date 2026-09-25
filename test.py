import pygame

CELL_SIZE = 32

maze = [
    [1, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 1],
]

pygame.init()
screen = pygame.display.set_mode((len(maze[0]) * CELL_SIZE, len(maze) * CELL_SIZE))
clock = pygame.time.Clock()

def draw_maze(screen: pygame.Surface, grid: list[list[int]]) -> None:
    for row_index, row in enumerate(grid):
        for col_index, value in enumerate(row):
            x = col_index * CELL_SIZE
            y = row_index * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            if value == 1:
                pygame.draw.rect(screen, (0, 0, 255), rect)   # wall = blue block
            else:
                pygame.draw.circle(
                    screen, (255, 255, 0),
                    rect.center, 4
                )  # path = small yellow dot (pacgum)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    draw_maze(screen, maze)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
