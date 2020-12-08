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
	curses.init_pair(1,53, 53)
	curses.init_pair(2,51,-1)

	while k != ord("q"):
		stdscr.erase()
		if k == ord("l"):
			stdscr.addch(0,0,curses.ACS_ULCORNER, curses.color_pair(2))
			stdscr.addch(1,0,curses.ACS_VLINE, curses.color_pair(2))
			stdscr.addch(2,0,curses.ACS_VLINE, curses.color_pair(2))

			stdscr.addch(0,1,curses.ACS_HLINE, curses.color_pair(2))
			stdscr.addch(0,2,curses.ACS_TTEE, curses.color_pair(2))
			stdscr.addch(0,3,curses.ACS_HLINE, curses.color_pair(2))
			stdscr.addch(0,4,curses.ACS_TTEE, curses.color_pair(2))
			stdscr.addch(0,5,curses.ACS_HLINE, curses.color_pair(2))

			stdscr.addch(0,6,curses.ACS_URCORNER, curses.color_pair(2))
			stdscr.addch(1,6,curses.ACS_VLINE, curses.color_pair(2))
			stdscr.addch(2,6,curses.ACS_VLINE, curses.color_pair(2))

			
			stdscr.addch(1,2,"#",curses.color_pair(1))
			#stdscr.addch(2,2,"#",curses.color_pair(1))
			stdscr.addch(1,4,"#",curses.color_pair(1))
			#stdscr.addch(2,4,"#",curses.color_pair(1))


		lista = [
			curses.ACS_ULCORNER,
			curses.ACS_LLCORNER,
			curses.ACS_URCORNER,
			curses.ACS_LRCORNER,
			curses.ACS_LTEE,
			curses.ACS_RTEE,
			curses.ACS_BTEE,
			curses.ACS_TTEE,
			curses.ACS_HLINE,
			curses.ACS_VLINE,
			curses.ACS_PLUS,
			curses.ACS_S1,
			curses.ACS_S3,
			curses.ACS_S7,
			curses.ACS_S9,
			curses.ACS_DIAMOND,
			curses.ACS_CKBOARD,
			curses.ACS_DEGREE,
			curses.ACS_PLMINUS,
			curses.ACS_BULLET,
			curses.ACS_LARROW,
			curses.ACS_RARROW,
			curses.ACS_DARROW,
			curses.ACS_UARROW,
			curses.ACS_BOARD,
			curses.ACS_LANTERN,
			curses.ACS_BLOCK,
			curses.ACS_LEQUAL,
			curses.ACS_GEQUAL,
			curses.ACS_PI,
			curses.ACS_NEQUAL,
			curses.ACS_STERLING
		]
		x = 22
		y = 0
		for item in lista:
			stdscr.addch(x,y,item)
			y += 1
		x = 23
		y = 0
		for i in range(255):
			stdscr.addch(x,y, chr(i))
			if i % 100 == 0:
				x += 1
				y = 0
			else:
				y += 1
		
		k = stdscr.getch()

curses.wrapper(main)