"""
project: maze generation DFS

bugs:
not noticing that if after you move up you move right one of the walls won't
disappear
"""

from random import randint, choice
import logging
import pygame
import sys

# logging.basicConfig(level=logging.DEBUG)  # < logging

# needed variables:
grid = [[(True, True, True, True) for _ in range(16)] for _ in range(16)]  # (up, down, left, right)
visited = [[False for _ in range(16)] for _ in range(16)]

pos = (randint(0, 15), randint(0, 15))  # start pos
visited[pos[0]][pos[1]] = True  # start tile
move_stack = [pos]  # move list
perm_move_stack = [pos]  # move list, no popping items
logging.debug(f'initial player position: {pos}')

# pygame
wn = pygame.display.set_mode((850, 850))
clock = pygame.time.Clock()

# colors:
black = (0, 0, 0)
green = (114, 50, 242)
blue = (32, 17, 91)
light_blue = (200, 118, 255)


def get_adjacent_cells(matrix: list, row: int, col: int) -> list:
    directions = {
        (-1, 0): "up",
        (1, 0): "down",
        (0, -1): "left",
        (0, 1): "right"
    }

    rows = len(matrix)
    cols = len(matrix[0])

    adjacent_cells = []

    for (r, c), direction in directions.items():
        new_row = row + r
        new_col = col + c

        if 0 <= new_row < rows and 0 <= new_col < cols and not visited[new_row][new_col]:
            adjacent_cells.append(((new_row, new_col), direction))
    logging.debug(f'Adjacent cells for position ({row}, {col}): {adjacent_cells}')
    return adjacent_cells


def move_character_dfs(matrix: list, pos: tuple, moves: list, perm_moves: list) -> int | tuple:
    logging.debug(f'Current position: {pos}')
    adjacent_cells = get_adjacent_cells(matrix, pos[0], pos[1])

    if not adjacent_cells:
        if moves:
            new_pos = moves.pop()
            logging.debug(f'No adjacent cells, backtracking to: {new_pos}')
            return new_pos
        else:
            logging.debug('No adjacent cells and move stack is empty, staying in the same position.')
            return pos

    move = choice(adjacent_cells)
    logging.debug(f'Moving to: {move[0]} in direction: {move[1]}')
    moves.append(pos)
    perm_moves.append(move[0])

    row, col = pos
    new_row, new_col = move[0]
    direction = move[1]

    # tuples can't be modified...
    current_cell = list(matrix[row][col])
    new_cell = list(matrix[new_row][new_col])

    # set walls
    if direction == "up":
        current_cell[0] = False
        new_cell[1] = False
    elif direction == "down":
        current_cell[1] = False
        new_cell[0] = False
    elif direction == "left":
        current_cell[2] = False
        new_cell[3] = False
    elif direction == "right":
        current_cell[3] = False
        new_cell[2] = False

    # back to tuples
    matrix[row][col] = tuple(current_cell)
    matrix[new_row][new_col] = tuple(new_cell)

    visited[new_row][new_col] = True
    logging.debug(f'Updated grid at new position {new_row}, {new_col}: {matrix[new_row][new_col]}')
    logging.debug(f'Updated grid at current position {row}, {col}: {matrix[row][col]}')

    return new_row, new_col


def draw(matrix: list, tile_size: int) -> None:
    wn.fill(light_blue)

    # bg
    for move in perm_move_stack:
        pygame.draw.rect(wn, black, (move[1] * tile_size + 25, move[0] * tile_size + 25, tile_size, tile_size))

    # grid lines
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            top, bottom, left, right = matrix[row][col]
            x, y = col * tile_size + 25, row * tile_size + 25
            if top:
                pygame.draw.line(wn, green, (x, y), (x + tile_size, y), 3)
            if bottom:
                pygame.draw.line(wn, green, (x, y + tile_size), (x + tile_size, y + tile_size), 3)
            if left:
                pygame.draw.line(wn, green, (x, y), (x, y + tile_size), 3)
            if right:
                pygame.draw.line(wn, green, (x + tile_size, y), (x + tile_size, y + tile_size), 3)

    # Draw the current position in blue
    if move_stack:
        pygame.draw.rect(wn, blue, (move_stack[-1][1] * tile_size + 25, move_stack[-1][0] * tile_size + 25, tile_size, tile_size))


while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pos = move_character_dfs(grid, pos, move_stack, perm_move_stack)
    logging.debug(f'New position: {pos}')
    draw(grid, 50)
    pygame.display.update()

