import curses

def numb_gen():
	for item in range(255):
		yield item

def main(stdscr):
	curses.start_color()
	curses.use_default_colors()
	k = ord("a")
	nums = numb_gen()
	while k != ord("q"):
		stdscr.clear()
		try:
			
			if k == ord("a"):
				for i in range(0, curses.COLORS - 1):
					curses.init_pair(i + 1, i, i)

				for i in range(0, 255):
					stdscr.attron(curses.color_pair(i + 1))
					stdscr.addstr(str(i))
					stdscr.attroff(curses.color_pair(i + 1))
			
			if k == ord("s"):
				for i in range(0, curses.COLORS - 1):
					curses.init_pair(i + 1, 255 - i, i)

				for i in range(0, 255):
					stdscr.attron(curses.color_pair(i + 1))
					stdscr.addstr(str(i))
					stdscr.attroff(curses.color_pair(i + 1))
			
			if k == ord("d"):
				for i in range(0, curses.COLORS - 1):
					curses.init_pair(i + 1, i, 130)

				for i in range(0, 255):
					stdscr.attron(curses.color_pair(i + 1))
					stdscr.addstr(str(i))
					stdscr.attroff(curses.color_pair(i + 1))

			if k == ord(" "):
				next_num = nums.__next__()
				print(next_num)
				for i in range(0, curses.COLORS - 1):
					curses.init_pair(i + 1, next_num, i)
				for i in range(0, 255):
					stdscr.attron(curses.color_pair(i + 1))
					stdscr.addstr(str(i))
					stdscr.attroff(curses.color_pair(i + 1))

			if k == ord("p"):
				curses.init_pair(130, 15 , 245)
				stdscr.attron(curses.color_pair(130))
				stdscr.addstr(".")
				stdscr.attroff(curses.color_pair(130))
			
			stdscr.addstr(15,0, "BLINK", curses.A_BLINK)
			stdscr.addstr(16,0, "BOLD", curses.A_BOLD)
			stdscr.addstr(17,0, "DIM", curses.A_DIM)
			stdscr.addstr(18,0, "REVERSE", curses.A_REVERSE)
			stdscr.addstr(19,0, "STANDOUT", curses.A_STANDOUT)
			stdscr.addstr(20,0, "UNDERLINE", curses.A_UNDERLINE)


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

		except curses.ERR:
			# End of screen reached
			pass
		k = stdscr.getch()

curses.wrapper(main)