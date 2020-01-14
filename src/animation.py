import curses

def test_animation():
    frames = []
    with open("test.txt") as f:
        lines = f.read().split("\n")
        print(len(lines))
        print(len(lines[0]))
        frames.append(lines[1:45])

    return frames

def play(frames, state):
    screen = state.stdscr
    height, width = screen.getmaxyx()
    curses.halfdelay(44)
    k = -1

    offset_x = 0

    frame = 0

    color_map = {
        " " : 133,
        "#" : 138,
        "W" : 96,
        "F" : 54,
        "G" : 42,
        "D" : 209
    }



    while k  != ord("q"):
        screen.clear()
        if frame == len(frames):
            break
        for x, row in enumerate(frames[frame]):
            for y, char in enumerate(row):
                screen.addch(offset_x + x, 0 + y, curses.ACS_BLOCK, curses.color_pair(color_map[char]))

        screen.addstr(45,50,str(frame))


        k = screen.getch()

        frame += 1
    curses.nocbreak()
    return
