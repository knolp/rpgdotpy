import curses
import random


def main(stdscr):
	curses.start_color()
	curses.use_default_colors()
	k = ord("a")
	x = 0
	y = 0
	x_start = 0
	max_x = 40
	y_start = 0
	for i in range(1, curses.COLORS - 1):
		curses.init_color(i, int(i / 0.255), 0, 500)
		curses.init_pair(i + 1, curses.COLOR_WHITE, i)
	while k != ord("q"):
		stdscr.clear()
		if k == ord("l"):
			for i in range(255):
				if x == max_x:
					x = 0
					y += 3
				try:
					stdscr.addstr(x_start + x, y_start + y, f"{'   '}", curses.color_pair(i))
				except:
					print(x_start + x)
					print(y_start + y)
				x += 1


#		lista = [
#			curses.ACS_ULCORNER,
#			curses.ACS_LLCORNER,
#			curses.ACS_URCORNER,
#			curses.ACS_LRCORNER,
#			curses.ACS_LTEE,
#			curses.ACS_RTEE,
#			curses.ACS_BTEE,
#			curses.ACS_TTEE,
#			curses.ACS_HLINE,
#			curses.ACS_VLINE,
#			curses.ACS_PLUS,
#			curses.ACS_S1,
#			curses.ACS_S3,
#			curses.ACS_S7,
#			curses.ACS_S9,
#			curses.ACS_DIAMOND,
#			curses.ACS_CKBOARD,
#			curses.ACS_DEGREE,
#			curses.ACS_PLMINUS,
#			curses.ACS_BULLET,
#			curses.ACS_LARROW,
#			curses.ACS_RARROW,
#			curses.ACS_DARROW,
#			curses.ACS_UARROW,
#			curses.ACS_BOARD,
#			curses.ACS_LANTERN,
#			curses.ACS_BLOCK,
#			curses.ACS_LEQUAL,
#			curses.ACS_GEQUAL,
#			curses.ACS_PI,
#			curses.ACS_NEQUAL,
#			curses.ACS_STERLING
#		]
#		x = 22
#		y = 0
#		for item in lista:
#			stdscr.addch(x,y,item)#

#			y += 1
		k = stdscr.getch()

curses.wrapper(main)