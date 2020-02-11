import sys,os,time
import curses
import mapper

class Cursor():
	def __init__(self):
		self.x = 0
		self.y = 0

class player():
	def __init__(self):
		self.ascii = False

class State():
	def __init__(self, screen):
		self.game_box = screen
		self.player = player()
def draw_menu(stdscr):
	k = 0
	state = State(stdscr)
	mapp = mapper.GameMap("BrownBearInn copy.txt", [])
	cursor = Cursor()

	curses.curs_set(0)
	curses.cbreak()
	curses.mousemask(curses.ALL_MOUSE_EVENTS)
	stdscr.keypad(1)

	#init a lot of colors
	curses.start_color()

	curses.use_default_colors()
	for i in range(0, curses.COLORS - 1):
		curses.init_pair(i + 1, i, i - 1)

	curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_RED)
	curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
	curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLUE)
	curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_GREEN)
	curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
	curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_YELLOW)
	curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_CYAN)

	#Color range 131 -> 147 reserved

	curses.init_pair(131, 232, 165)
	curses.init_pair(132, curses.COLOR_YELLOW, curses.COLOR_GREEN)
	curses.init_pair(133, curses.COLOR_RED, -1)
	curses.init_pair(134, curses.COLOR_GREEN, -1)
	curses.init_pair(135, curses.COLOR_CYAN, -1)
	curses.init_pair(136, curses.COLOR_YELLOW, -1)
	curses.init_pair(137, curses.COLOR_BLUE, - 1)
	curses.init_pair(138, 130, -1) # Enhanced Dialogue
	curses.init_pair(139, 238 , 242) #Cobblestone
	curses.init_pair(140, 237, 242) #Fence
	curses.init_pair(141, 240, 40) #Grass Fence
	curses.init_pair(142, 136, 40) #Tree Bot
	curses.init_pair(143, 22, 40) #Tree Top
	curses.init_pair(144, 220, 94) #Beer
	curses.init_pair(145, 94, 52) #Wooden Chair
	curses.init_pair(146, 237, 52) #floor fence
	curses.init_pair(147, curses.COLOR_WHITE, -1)
	curses.init_pair(148, curses.COLOR_YELLOW, 238) #Wall torch
	curses.init_pair(149,94,-1) #brown fg, black bg
	curses.init_pair(150,242,-1) #grey fg, black bg
	curses.init_pair(151,curses.COLOR_WHITE,247)
	curses.init_pair(152, curses.COLOR_WHITE, curses.COLOR_RED)
	curses.init_pair(153,curses.COLOR_RED, 52) #Farming patch not planted
	curses.init_pair(154,curses.COLOR_YELLOW,52) #Farming patch planted
	curses.init_pair(155,curses.COLOR_GREEN,52) #Farming patch planted
	curses.init_pair(156, curses.COLOR_YELLOW, 40) #Yellow fg on grass bg (initally for AriamBush)
	curses.init_pair(157, curses.COLOR_YELLOW, 185) #Wheat
	curses.init_pair(158, 208,208) # Fire?
	curses.init_pair(159, curses.COLOR_CYAN, curses.COLOR_CYAN) #Window?
	curses.init_pair(160, 130, curses.COLOR_RED)


	while k != ord("q"):
		stdscr.erase()
		mapp.draw_map(state)

		stdscr.addch(cursor.x, cursor.y, "X")


		#Get input
		k = stdscr.getch()

		if k == curses.KEY_UP:
			cursor.x -= 1
			if cursor.x < 0:
				cursor.x = 0
		
		elif k == curses.KEY_DOWN:
			cursor.x += 1
			if cursor.x > 38:
				cursor.x = 38

		elif k == curses.KEY_RIGHT:
			cursor.y += 1
			if cursor.y > 150:
				cursor.y = 150

		elif k == curses.KEY_LEFT:
			cursor.y -= 1
			if cursor.y < 0:
				cursor.y = 0

		elif k == ord("4"):
			state.player.ascii = not state.player.ascii

		elif k == ord("G"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.grass(cursor.x, cursor.y)
		elif k == ord("W"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.wall(cursor.x, cursor.y)
		elif k == ord("T"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.tree(cursor.x, cursor.y)
		elif k == ord("A"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.water(cursor.x, cursor.y)
		elif k == ord("F"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.floor(cursor.x, cursor.y)
		elif k == ord("D"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.door(cursor.x, cursor.y)
		elif k == ord("b"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.bridge(cursor.x, cursor.y)
		elif k == ord("g"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.tall_grass(cursor.x, cursor.y)
		elif k == ord("h"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.hole(cursor.x, cursor.y)
		elif k == ord("w"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.false_wall(cursor.x, cursor.y)
		elif k == ord("c"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.castle_wall(cursor.x, cursor.y)
		elif k == ord("C"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.cobblestone(cursor.x, cursor.y)
		elif k == ord("("):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.fence_left(cursor.x, cursor.y)
		elif k == ord(")"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.fence_right(cursor.x, cursor.y)
		elif k == ord("-"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.fence_middle(cursor.x, cursor.y)
		elif k == ord("{"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.grass_fence_left(cursor.x, cursor.y)
		elif k == ord("}"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.grass_fence_right(cursor.x, cursor.y)
		elif k == ord("_"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.grass_fence_middle(cursor.x, cursor.y)
		elif k == ord("<"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.tree_bot_left(cursor.x, cursor.y)
		elif k == ord(">"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.tree_bot_right(cursor.x, cursor.y)
		elif k == ord("*"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.wooden_chair(cursor.x, cursor.y)
		elif k == ord("m"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.beer(cursor.x, cursor.y)
		elif k == ord("+"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.floor_fence_middle(cursor.x, cursor.y)
		elif k == ord("d"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.visble_door(cursor.x, cursor.y)
		elif k == ord("U"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.under_wall(cursor.x, cursor.y)
		elif k == ord("u"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.under_wall_torch(cursor.x, cursor.y)
		elif k == ord("s"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.sign(cursor.x, cursor.y)
		elif k == ord("f"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.wheat(cursor.x, cursor.y)
		elif k == ord("e"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.fire(cursor.x, cursor.y)
		elif k == ord("E"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.window(cursor.x, cursor.y)
		elif k == ord("7"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.carpetUL(cursor.x, cursor.y)
		elif k == ord("9"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.carpetUR(cursor.x, cursor.y)
		elif k == ord("1"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.carpetLL(cursor.x, cursor.y)
		elif k == ord("3"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.carpetLR(cursor.x, cursor.y)
		elif k == ord("4"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.carpetVLINE(cursor.x, cursor.y)
		elif k == ord("8"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.carpetHLINE(cursor.x, cursor.y)
		elif k == ord("5"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.carpet(cursor.x, cursor.y)
		elif k == ord("0"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.carpetdiamond(cursor.x, cursor.y)
		elif k == ord("R"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.castle_wall_walkable(cursor.x, cursor.y)
		elif k == ord("r"):
			mapp.background2[cursor.x - 1][cursor.y - 1] = mapper.MapObject.under_wall_walkable(cursor.x, cursor.y)


if __name__ == "__main__":
	curses.wrapper(draw_menu)