def add_border():
    pass

def farming(state, identity):
    screen = state.stdscr
    player = state.player
    height, width = screen.getmaxyx()
    curses.halfdelay(3)
    k = -1

    current_plant = "Empty"
    for item in player.active_farms:
        if item[0] == identity:
            current_plant = item[1]

    while k != ord("q"):

        k = screen.getch()