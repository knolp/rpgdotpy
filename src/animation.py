import curses
import helper

def test_animation():
    frames = []
    frames.append([
        "#########",
        "#########",
        "#########",
        "#########",
        "#########",
    ])
    frames.append([
        "         ",
        "         ",
        "         ",
        "         ",
        "         ",
    ])
    frames.append([
        "#########",
        "#########",
        "##DFGWA##",
        "#########",
        "#########",
    ])

    return frames

def boat_animation():
    with open("animations/boat.txt") as f:
        text = f.readlines()

    frames = []
    counter = 0
    while True:
        try:
            frames.append(text[counter:counter+48])
            counter += 49
            if counter > len(text):
                break
        except:
            break
    frames.pop()# Delete
    frames.pop()# Useless
    frames.pop()# Frames
    return frames

@helper.add_ungetch
def play(frames, state):
    screen = state.stdscr
    height, width = screen.getmaxyx()
    curses.halfdelay(1)
    k = -1

    offset_x = 0
    offset_y = 4

    frame = 0

    color_map = {
        " " : 162,
        "#" : 163,
        "W" : 96,
        "F" : 54,
        "G" : 42,
        "D" : 209,
        "U" : 240,
        "A" : 21
    }



    while k != ord("q"):
        screen.clear()
        if frame == len(frames):
            break
        for x, row in enumerate(frames[frame]):
            for y, char in enumerate(row):
                if char == "\n":
                    continue
                state.log_info(color_map[char])
                screen.addstr(offset_x + x, offset_y + y, char, curses.color_pair(color_map[char]))

        screen.addstr(45,50,str(frame), curses.color_pair(138))


        k = screen.getch()

        frame += 1
    curses.cbreak()
    return


if __name__ == "__main__":
    boat_animation()