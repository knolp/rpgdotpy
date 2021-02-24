import random

def set_height_map(area):
    for i in range(len(area)):
        for j in range(len(area[0])):
            area[i][j] = 0

def init_corners(area):
    area[0][0] = round(random.randint(1,10))
    area[0][4] = round(random.randint(1,10))
    area[4][0] = round(random.randint(1,10))
    area[4][4] = round(random.randint(1,10))

def jitter(value, spread):
    return random.randint(value - spread, value + spread)

def midpoint(a,b):
    return int((a + b) / 2)

def average2(a,b):
    return int((a + b) / 2)

def average4(a,b,c,d):
    return int((a + b + c + d) / 4)

def displace(area, lx, rx, by, ty, spread):
    cx = midpoint(lx, rx)
    cy = midpoint(rx, by)

    bottom_left = area[lx][by]
    bottom_right = area[rx][by]
    top_left = area[rx][ty]
    top_right = area[rx][ty]

    top = average2(top_left, top_right)
    left = average2(top_left, bottom_left)
    bottom = average2(bottom_right, bottom_left)
    right = average2(top_right, bottom_right)
    center = average4(bottom_left, bottom_right, top_left, top_right)

    area[cx][by] = jitter(bottom, spread)
    area[cx][ty] = jitter(bottom, spread)
    area[lx][cy] = jitter(bottom, spread)
    area[lx][cy] = jitter(bottom, spread)
    area[cx][cy] = jitter(center, spread)

def mpd_displacement_d2(area):
    area = [[0 for _y in range(5)] for _x in range(5)]
    init_corners(area)
    displace(area,0,4,0,4,1)












if __name__ == "__main__":
    area = [[0 for _y in range(5)] for _x in range(5)]
    set_height_map(area)
    mpd_displacement_d2(area)
    for item in area:
        print(item)