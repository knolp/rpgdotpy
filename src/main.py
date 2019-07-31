import sys,os
import curses



def draw_menu(stdscr):
	k = 0
	cursor_x = 0
	cursor_y = 0

	# Clear and refresh the screen for a blank canvas
	stdscr.clear()
	stdscr.refresh()

	# Start colors in curses
	curses.start_color()
	curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

	# Loop where k is the last character pressed
	while (k != ord('q')):

		# Initialization
		stdscr.clear()
		height, width = stdscr.getmaxyx()

		inv_box = stdscr.derwin(40,50,0,00)
		eq_box = stdscr.derwin(40,50,0,50)
		info_box = stdscr.derwin(40,50,0,100)

		if k == curses.KEY_DOWN:
			cursor_y = cursor_y + 1
		elif k == curses.KEY_UP:
			cursor_y = cursor_y - 1
		elif k == curses.KEY_RIGHT:
			cursor_x = cursor_x + 1
		elif k == curses.KEY_LEFT:
			cursor_x = cursor_x - 1


		draw_commands(state, command_box)

		cursor_x = max(0, cursor_x)
		cursor_x = min(width-1, cursor_x)

		cursor_y = max(0, cursor_y)
		cursor_y = min(height-1, cursor_y)

		# Declaration of strings
		statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {} | {}x{}".format(cursor_x, cursor_y, width, height)
		if k == 0:
			keystr = "No key press detected..."[:width-1]

		# Render status bar
		stdscr.attron(curses.color_pair(3))
		stdscr.addstr(height-1, 0, statusbarstr)
		stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
		stdscr.attroff(curses.color_pair(3))

		# Print rest of text
		stdscr.move(cursor_y, cursor_x)

		# Refresh the screen
		stdscr.refresh()

		# Wait for next input
		k = stdscr.getch()

def main():
	curses.wrapper(draw_menu)

if __name__ == "__main__":
	main()