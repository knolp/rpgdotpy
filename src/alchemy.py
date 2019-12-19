import curses

def make_potion(state):
    screen = state.stdscr
    player = state.player
    height, width = screen.getmaxyx()
    screen.clear()

    