import curses

def test(state):
    screen = state.gamebox
    height, width = screen.getmaxyx()

    k = -1
    done = False

    while(not done):
        screen.erase()
        break