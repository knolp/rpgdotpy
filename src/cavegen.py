import random
import pathfinding

WIDTH = 96
HEIGHT = 37

CHANCE = 0.4

DEATH_LIMIT = 4
BIRTH_LIMIT = 4
NUMBER_OF_STEPS = 4

def pathfind(grid, door, player):
    d_x,d_y = door[0], door[1]
    p_x,p_y = player[1], player[0]
    grid_map = [[0 for _x in range(96)] for _y in range(37)]

    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] == 0:
                grid_map[x][y] = pathfinding.MapObject(x,y)
            else:
                grid_map[x][y] = pathfinding.MapObject(x,y, walkable=False)

    path = pathfinding.astar(grid_map,(d_x,d_y),(p_x,p_y))
    return path



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
            elif neighbor_x <= 0 or neighbor_y <= 0 or neighbor_y >= height - 1 or neighbor_x >= width - 1:
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


def create_door(grid, seed):
    height = len(grid)
    width = len(grid[0])
    possible_doors = []
    for i in range(width):
        for j in range(height):
            if 1 < count_alive_neighbors(grid,i,j) < 4 and grid[j][i] == 1:
                possible_doors.append((j,i))
    random.seed(seed)
    return random.choice(possible_doors)

def find_player_pos(grid, door):
    height = len(grid)
    width = len(grid[0])
    possible_player_pos = []
    score_list = []
    for i in range(width):
        for j in range(height):
            if grid[j][i] == 0 and count_alive_neighbors(grid, i, j) == 0:
                score = abs((i - door[0]) + (j - door[1]))
                score_list.append(score)
                possible_player_pos.append((i,j))
    
    path = False
    while not path:
        best_score = score_list.index(max(score_list))
        best_player_pos = possible_player_pos[best_score]
        path = pathfind(grid,door,best_player_pos)
        
        score_list.pop(score_list.index(max(score_list)))

    return (best_player_pos[1], best_player_pos[0])

def find_house(grid):
    height = len(grid)
    width = len(grid[0])
    possible_house_pos = []
    for i in range(4, width - 4):
        for j in range(4, height - 4):
            if count_alive_neighbors(grid, i, j) <= 3:
                continue
            #check north, northwest, northeast
            if grid[j - 1][i] == 1 and grid[j - 1][i - 1] == 1 and grid[j - 1][i + 1] == 1 and grid[j - 1][i + 2] == 1 and grid[j - 1][i - 2] == 1 and grid[j][i] == 0:
                #check one upper row more
                if grid[j - 2][i] == 1 and grid[j - 2][i - 1] == 1 and grid[j - 2][i + 1] == 1 and grid[j - 2][i + 2] == 1 and grid[j - 2][i + 2] == 1 :
                    possible_house_pos.append((i,j))
    if possible_house_pos:
        return random.choice(possible_house_pos)
    else:
        return False

def create_map(seed):
    grid = create_grid(96,37)
    init_grid(grid, seed)
    for _i in range(NUMBER_OF_STEPS):
        grid = step(grid)

    
    _ret_list = []
    x,y = create_door(grid, seed)
    player_pos = find_player_pos(grid, (x,y))
    house = find_house(grid)
    if house:
        print(house)
        #grid[house[1]][house[0]] = 2
        grid[house[1] - 1][house[0]] = 0  #
        grid[house[1]][house[0] - 1] = 3
        grid[house[1] - 1][house[0] - 1] = 0
        grid[house[1] - 1][house[0] + 1] = 0
        grid[house[1]][house[0] + 1] = 3
        grid[house[1] - 2][house[0] + 1] = 3
        grid[house[1] - 2][house[0] + 2] = 3
        grid[house[1] - 1][house[0] + 2] = 3
        grid[house[1]][house[0] + 2] = 3
        grid[house[1] - 2][house[0] - 1] = 3
        grid[house[1] - 2][house[0] - 2] = 3
        grid[house[1] - 2][house[0]] = 3
        grid[house[1] - 1][house[0] - 2] = 3
        grid[house[1]][house[0] - 2] = 3
    else:
        print("House not found")
    
    #if path:
    #    for item in path:
    #        grid[item[0]][item[1]] = 2
    #else:
    #    print("Path not found")
    grid[x][y] = 2

    raw_map = grid.copy()
    for item in grid:
        _ret_list.append("".join([str(x) for x in item]).replace("0","F").replace("1","W").replace("2","D").replace("3", "c"))
    
    return {
        "player_pos" : player_pos,
        "map" : _ret_list,
        "door_pos" : (x,y),
        "raw_map" : raw_map
        }








if __name__ == "__main__":
    mapp = create_map(random.randint(3554,12312312))
    #mapp = create_map(5199351)
    
    for item in mapp["map"]:
        print(item)