import sys,os,time
import curses
import curses.textpad as textpad
import curses.ascii as asc
from pprint import pprint

map_list = []

class object():
	def __init__(self, x, y, symbol):
		self.x = x
		self.y = y
		self.symbol = symbol

def init_map():
	with open("map1.txt") as f:
			count = 0
			for line in f:
				for i, item in enumerate(line):
					try:
						map_list.append(object(count,i, item))
					except:
						pass
				count += 1
	print("init_map complete")

def draw_menu(stdscr):
	for item in map_list[0:10]:
		print(item.x, item.y, item.symbol)
	k = 0
	cursor_x = 0
	cursor_y = 0

	# Clear and refresh the screen for a blank canvas
	stdscr.clear()
	stdscr.refresh()

	# Start colors in curses
	curses.start_color()
	curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_RED)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLUE)
	curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_GREEN)


	time.sleep(2)

	# Loop where k is the last character pressed
	while (k != ord('q')):

		stdscr.clear()
		map_box = stdscr.derwin(40,100,0,0)
		line_box = stdscr.derwin(40,2,0,100)
		command_box = stdscr.derwin(36,48,0,102)
		text_box = stdscr.derwin(1,48,38, 101)
		text_box_info = stdscr.derwin(1,48,37,101)
		text_pad = textpad.Textbox(text_box)
		#pprint(vars(curses))

		# Initialization
		height, width = map_box.getmaxyx()

		if k == curses.KEY_DOWN:
			cursor_y = cursor_y + 1
		elif k == curses.KEY_UP:
			cursor_y = cursor_y - 1
		elif k == curses.KEY_RIGHT:
			cursor_x = cursor_x + 1
		elif k == curses.KEY_LEFT:
			cursor_x = cursor_x - 1

		cursor_x = max(0, cursor_x)
		cursor_x = min(width-1, cursor_x)

		cursor_y = max(0, cursor_y)
		cursor_y = min(height-1, cursor_y)

		text_box_info.addch(curses.ACS_BLOCK)

		if k == ord("a"):
			text_pad.edit()

		# Declaration of strings
		statusbarstr = "Press 'q' to exit | Map Editor | Pos: {}, {} | {}x{}".format(cursor_x, cursor_y, width, height)
		if k == 0:
			keystr = "No key press detected..."[:width-1]

		for i in range(40):
			line_box.addstr(i,0,"|")

		# Print commands
		command_box.addstr(0,0,"T: Add Tree")
		command_box.addstr(2,0,"W: Add Wall")
		command_box.addstr(4,0,"E: Erase")

		#if k == ord("t"):

			#map_list.append(object(cursor_x, cursor_y, "A"))

		# Render status bar
		stdscr.attron(curses.color_pair(3))
		stdscr.addstr(height-1, 0, statusbarstr)
		stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
		stdscr.attroff(curses.color_pair(3))

		for item in map_list:
			if item.symbol == "#":
				map_box.attron(curses.color_pair(4))
				map_box.addch(item.x, item.y, ord(item.symbol))
				map_box.attroff(curses.color_pair(4))
			elif item.symbol == "G":
				map_box.attron(curses.color_pair(5))
				map_box.addch(item.x, item.y, ord(item.symbol))
				map_box.attroff(curses.color_pair(5))
			elif item.symbol == "W":
				map_box.attron(curses.color_pair(1))
				map_box.addch(item.x, item.y, curses.ACS_CKBOARD)
				map_box.attroff(curses.color_pair(1))
			elif item.symbol == "F":
				map_box.attron(curses.color_pair(1))
				map_box.addch(item.x, item.y, curses.ACS_BTEE)
				map_box.attroff(curses.color_pair(1))
			
			else:
				map_box.addch(item.x, item.y, ord(item.symbol))

		# Print rest of text
		map_box.move(cursor_y, cursor_x)

		map_box.attron(curses.color_pair(2))
		map_box.addch(cursor_y, cursor_x, "@")
		map_box.attroff(curses.color_pair(2))
		# Refresh the screen
		#stdscr.refresh()

		# Wait for next input
		k = stdscr.getch()

def main():
	init_map()
	curses.wrapper(draw_menu)

if __name__ == "__main__":
	main()