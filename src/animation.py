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

@helper.add_ungetch
def play(frames, state):
    screen = state.stdscr
    height, width = screen.getmaxyx()
    curses.halfdelay(4)
    k = -1

    offset_x = 0

    frame = 0

    color_map = {
        " " : 133,
        "#" : 138,
        "W" : 96,
        "F" : 54,
        "G" : 42,
        "D" : 209,
        "U" : 240,
        "A" : 21
    }



    while k  != ord("q"):
        screen.clear()
        if frame == len(frames):
            break
        for x, row in enumerate(frames[frame]):
            for y, char in enumerate(row):
                screen.addch(offset_x + x, 0 + y, char, curses.color_pair(color_map[char]))

        screen.addstr(45,50,str(frame))


        k = screen.getch()

        frame += 1
    curses.nocbreak()
    return
