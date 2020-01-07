import random

WIDTH = 96
HEIGHT = 37

CHANCE = 0.4

DEATH_LIMIT = 4
BIRTH_LIMIT = 4
NUMBER_OF_STEPS = 4



def create_grid(width, height):
    """ Create a two-dimensional grid of specified size. """
    return [[0 for _x in range(width)] for _y in range(height)]


def init_grid(grid, seed):
    """ Randomly set grid locations to on/off based on chance. """
    height = len(grid)
    width = len(grid[0])
    for row in range(height):
        for column in range(width):
            random.seed(seed)
            seed -= 1
            if random.random() <= CHANCE:
                grid[row][column] = 1


def count_alive_neighbors(grid, x, y):
    """ Count neighbors that are alive. """
    height = len(grid)
    width = len(grid[0])
    alive_count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            neighbor_x = x + i
            neighbor_y = y + j
            if i == 0 and j == 0:
                continue
            elif neighbor_x < 0 or neighbor_y < 0 or neighbor_y >= height or neighbor_x >= width:
                # Edges are considered alive. Makes map more likely to appear naturally closed.
                alive_count += 1
            elif grid[neighbor_y][neighbor_x] == 1:
                alive_count += 1
    return alive_count


def step(old_grid):
    """ Run a step of the cellular automaton. """
    height = len(old_grid)
    width = len(old_grid[0])
    new_grid = create_grid(width, height)
    for x in range(width):
        for y in range(height):
            alive_neighbors = count_alive_neighbors(old_grid, x, y)
            if old_grid[y][x] == 1:
                if alive_neighbors < DEATH_LIMIT:
                    new_grid[y][x] = 0
                else:
                    new_grid[y][x] = 1
            else:
                if alive_neighbors > BIRTH_LIMIT:
                    new_grid[y][x] = 1
                else:
                    new_grid[y][x] = 0
    return new_grid


def create_map(seed):
    grid = create_grid(96,37)
    init_grid(grid, seed)
    for i in range(NUMBER_OF_STEPS):
        grid = step(grid)

    _ret_list = []
    for item in grid:
        _ret_list.append("".join([str(x) for x in item]).replace("0","F").replace("1","W"))
    
    return _ret_list








if __name__ == "__main__":
    mapp = create_map(3552)
    for item in mapp:
        print(item)