import curses
import random

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
					curses.init_pair(i + 1, 7, i)

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

			if k == ord("t"):
				print(chr(97))
				for i in range(220):
					stdscr.addstr(chr(i))

			if k == ord("l"):
				lis = [
					["UL","HW","HW","HW","HW","HW","HW","HW","HW","UR"],
					["VW","FF","FF","FF","FF","FF","FF","FF","FF","VW"],
					["VW","FF","FF","FF","FF","FF","FF","FF","FF","VW"],
					["VW","FF","FF","FF","FF","FF","FF","FF","FF","VW"],
					["VW","FF","FF","FF","FF","SS","FF","FF","FF","VW"],
					["VW","FF","FF","FF","FF","FF","FF","FF","FF","VW"],
					["VW","FF","FF","FF","FF","FF","FF","FF","FF","VW"],
					["VW","FF","FF","FF","FF","FF","FF","FF","FF","VW"],
					["VW","FF","FF","FF","FF","FF","FF","FF","FF","VW"],
					["LL","HW","HW","HW","HW","HW","HW","HW","HW","LR"]
				]

				for i in range(len(lis)):
					for j in range(len(lis[0])):
						if lis[i][j] == "HW":
							stdscr.addch(i,j,curses.ACS_HLINE)
						if lis[i][j] == "VW":
							stdscr.addch(i,j,curses.ACS_VLINE)
						if lis[i][j] == "UL":
							stdscr.addch(i,j,curses.ACS_ULCORNER)
						if lis[i][j] == "UR":
							stdscr.addch(i,j,curses.ACS_URCORNER)
						if lis[i][j] == "LL":
							stdscr.addch(i,j,curses.ACS_LLCORNER)
						if lis[i][j] == "LR":
							stdscr.addch(i,j,curses.ACS_LRCORNER)
						if lis[i][j] == "FF":
							stdscr.addch(i,j,"=")
						if lis[i][j] == "SS":
							stdscr.addch(i,j,">")

			if k == ord("r"):
				lista = [curses.ACS_URCORNER, curses.ACS_LRCORNER, curses.ACS_LLCORNER, curses.ACS_ULCORNER, curses.ACS_VLINE, curses.ACS_HLINE,curses.ACS_LTEE, curses.ACS_RTEE, curses.ACS_BTEE, curses.ACS_TTEE]
				for i in range(10):
					for j in range(50):
						stdscr.addch(i, j, random.choice(lista))			
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

			curses.init_pair(1, 136, 40)
			curses.init_pair(2, 28, 40)

			stdscr.attron(curses.color_pair(1))
			stdscr.addch(31,0,"}", curses.A_BOLD)
			stdscr.addch(31,1,"{")
			stdscr.attroff(curses.color_pair(1))
			stdscr.attron(curses.color_pair(2))		
			stdscr.addch(30,0, "#")
			stdscr.addch(30,1, "#")
			stdscr.addch(29,0, "#")
			stdscr.addch(29,1, "#")
			stdscr.attroff(curses.color_pair(2))

		except curses.ERR:
			# End of screen reached
			pass
		k = stdscr.getch()

curses.wrapper(main)