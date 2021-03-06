import curses
import random
import time
import os
import math

curses.initscr()
curses.start_color()
curses.use_default_colors()

# CHECK COLORS.PY FOR COLORS


class MapObject():
	def __init__(self, x, y, character, walkable=True, color=False, executable=False, colors=False, name=False, visible=True, over=False):
		self.x = x
		self.y = y
		self.character = character
		self.walkable = walkable
		self.color = color
		self.colors = colors
		self.executable = executable
		self.name = name
		self.visible = visible
		self.over = over

	@classmethod
	def tree(cls, x, y):
		return cls(x, y, "T", walkable=False, color=24, visible=False, name="Tree")

	@classmethod
	def wall(cls, x, y):
		return cls(x, y, "*", walkable=False, color=96, visible=False, name="Wall")

	@classmethod
	def floor(cls, x, y):
		return cls(x, y, " ", walkable=True, color=54, name="Floor")

	@classmethod
	def grass(cls, x, y):
		return cls(x, y, " ", walkable=True, color=42, name="Grass")

	@classmethod
	def water(cls, x, y):
		return cls(x, y, "~", walkable=False, color=22, name="Water")

	@classmethod
	def door(cls, x, y):
		return cls(x, y, "%", walkable=True, color=209, executable=True, visible=False, name="Door")

	@classmethod
	def bridge(cls, x, y):
		return cls(x, y, ".", walkable=True, color=96, name="Bridge")

	@classmethod
	def tall_grass(cls,x,y):
		return cls(x, y, "_", walkable=True, color=43, name="Tall Grass")

	@classmethod
	def hole(cls,x,y):
		return cls(x, y, " ", walkable=True, color=0, name="Hole")
	
	@classmethod
	def false_wall(cls,x,y):
		return cls(x, y, "#", walkable=True, color=96, visible=False, name="Wall")

	@classmethod
	def castle_wall(cls,x,y):
		return cls(x, y, "#", walkable=False, color=248, visible=False, name="Castle Wall")
	
	@classmethod
	def cobblestone(cls, x, y):
		return cls(x, y, ".", walkable=True, color=139, name="Cobblestone")

	@classmethod
	def fence_left(cls, x, y):
		return cls(x, y, curses.ACS_LTEE, walkable=False, color=140, name="Fence Left")

	@classmethod
	def fence_middle(cls, x, y):
		return cls(x, y, curses.ACS_PLUS, walkable=False, color=140, name="Fence middle")

	@classmethod
	def fence_right(cls, x, y):
		return cls(x, y, curses.ACS_RTEE, walkable=False, color=140, name="Fence middle")
	@classmethod
	def grass_fence_left(cls, x, y):
		return cls(x, y, curses.ACS_LTEE, walkable=False, color=141, name="Grass Fence Left")

	@classmethod
	def grass_fence_middle(cls, x, y):
		return cls(x, y, curses.ACS_PLUS, walkable=False, color=141, name="Grass Fence middle")

	@classmethod
	def grass_fence_right(cls, x, y):
		return cls(x, y, curses.ACS_RTEE, walkable=False, color=141, name="Grass Fence middle")

	@classmethod
	def tree_bot_left(cls, x, y):
		return cls(x, y, "}", walkable=False, color=142, name="Tree Bot Left")

	@classmethod
	def tree_bot_right(cls, x, y):
		return cls(x, y, "{", walkable=False, color=142, name="Tree Bot Right")

	@classmethod
	def tree_top(cls, x, y):
		return cls(x, y, curses.ACS_CKBOARD, walkable=True, color=143, name="Tree Top", over=True)

	@classmethod
	def wooden_chair(cls, x, y):
		return cls(x, y, curses.ACS_DIAMOND, walkable=True, color=145, name="Wooden Chair")

	@classmethod
	def beer(cls, x, y):
		return cls(x, y, curses.ACS_DIAMOND, walkable=False, color=144, name="Glass of beer")
	
	@classmethod
	def floor_fence_middle(cls, x, y):
		return cls(x, y, curses.ACS_PLUS, walkable=False, color=146, name="Floor Fence Middle")
	
	@classmethod
	def visble_door(cls, x, y):
		return cls(x, y, "%", walkable=True, color=209, executable=True, name="Door")

	@classmethod
	def under_wall(cls, x, y):
		return cls(x, y, curses.ACS_BOARD, walkable=False, color=240, name="Wall")

	@classmethod
	def under_wall_torch(cls, x, y):
		return cls(x,y, curses.ACS_DEGREE, walkable=False, color=148, name="Wall Torch")

	@classmethod
	def sign(cls,x,y):
		return cls(x,y, "#", walkable = True, color=96, name="Sign")
	
	@classmethod
	def wheat(cls,x,y):
		return cls(x,y, curses.ACS_BOARD, walkable = True, color=157, name="Wheat")

	@classmethod
	def fire(cls,x,y):
		return cls(x,y, "*", walkable = False, color=158, name="Fire")
	
	@classmethod
	def window(cls,x,y):
		return cls(x,y, " ", walkable = False, color=145, name="Window")

	@classmethod
	def carpetUR(cls,x,y):
		return cls(x,y, curses.ACS_URCORNER, walkable = True, color=160, name="Carpet")
	
	@classmethod
	def carpetLR(cls,x,y):
		return cls(x,y, curses.ACS_LRCORNER, walkable = True, color=160, name="Carpet")
	
	@classmethod
	def carpetUL(cls,x,y):
		return cls(x,y, curses.ACS_ULCORNER, walkable = True, color=160, name="Carpet")

	@classmethod
	def carpetLL(cls,x,y):
		return cls(x,y, curses.ACS_LLCORNER, walkable = True, color=160, name="Carpet")

	@classmethod
	def carpetHLINE(cls,x,y):
		return cls(x,y, curses.ACS_HLINE, walkable = True, color=160, name="Carpet")
	
	@classmethod
	def carpetVLINE(cls,x,y):
		return cls(x,y, curses.ACS_VLINE, walkable = True, color=160, name="Carpet")

	@classmethod
	def carpet(cls,x,y):
		return cls(x,y, " ", walkable = True, color=160, name="Carpet")

	@classmethod
	def carpetdiamond(cls,x,y):
		return cls(x,y, curses.ACS_DIAMOND, walkable = True, color=160, name="Carpet")

	@classmethod
	def castle_wall_walkable(cls,x,y):
		return cls(x, y, " ", walkable=True, color=248, visible=False, name="Floor")
	
	@classmethod
	def under_wall_walkable(cls, x, y):
		return cls(x, y, curses.ACS_BOARD, walkable=True, color=240, name="Floor")


	def draw(self, state, seen=False, inverted=False, character=False):
		screen = state.game_box
		player = state.player
		
		if type(self.color) == list:
			self.color = random.choice(self.color)

		char = self.character
		if character:
			char = character

		#if self.colors:
		#	if self.color == False:
		#		self.color, useless = self.colors
		#	if self.color == self.colors[1]:
		#		self.color, useless = self.colors
		#	elif self.color == self.colors[0]:
		#		useless, self.color = self.colors
		
		if not inverted:
			if self.color and seen == False:
				if player.ascii == False:
					screen.attron(curses.color_pair(self.color))
				screen.addch(self.x, self.y, char)
				if player.ascii == False:
					screen.attroff(curses.color_pair(self.color))
			elif self.color and seen == True:
				if player.ascii == False:
					screen.attron(curses.color_pair(self.color))
				screen.addch(self.x, self.y, char, curses.A_REVERSE)
				if player.ascii == False:
					screen.attroff(curses.color_pair(self.color))
			else:
				screen.addstr(self.x, self.y, char)
		else:
			if self.color and seen == False:
				if player.ascii == False:
					screen.attron(curses.color_pair(self.color))
				screen.addch(self.x, self.y, char,curses.A_REVERSE)
				if player.ascii == False:
					screen.attroff(curses.color_pair(self.color))
			elif self.color and seen == True:
				if player.ascii == False:
					screen.attron(curses.color_pair(self.color))
				screen.addch(self.x, self.y, char, curses.A_REVERSE)
				if player.ascii == False:
					screen.attroff(curses.color_pair(self.color))
			else:
				screen.addstr(self.x, self.y, char,curses.A_REVERSE)


class GameMap():
	def __init__(self, map_file, objects, events=False, file=True):
		if file:
			map_file = "{}/maps/{}".format(os.getcwd(),map_file)
			with open(map_file, "r") as f:
				self.raw_map = f.readlines()
				for i in range(len(self.raw_map)):
					self.raw_map[i] = self.raw_map[i].replace("\n", "")
		else:
			self.raw_map = map_file
		self.background = []
		self.background2 = [[0] * 96 for i in range(37)]
		self.make_background()
		self.objects = objects
		if events:
			self.events = events
		else:
			self.events = []
		self.objects_to_draw = []
		self.seen = []

	def make_background2(self):
		for x in range(len(self.raw_map)):
			if x > 36:
				continue
			for y in range(len(self.raw_map[x])):
				if y > 95:
					continue
				if self.raw_map[x][y] == "G":
					self.background.append(MapObject.grass(x + 1, y + 1))
				elif self.raw_map[x][y] == "W":
					self.background.append(MapObject.wall(x + 1, y + 1))
				elif self.raw_map[x][y] == "T":
					self.background.append(MapObject.tree(x + 1, y + 1))
				elif self.raw_map[x][y] == "A":
					self.background.append(MapObject.floor(x + 1, y + 1))
				else:
					print(self.raw_map[x][y])
					print("Could not create map tile from Text")

	def make_background(self):
		for x in range(len(self.raw_map)):
			#print(x)
			if x > 36:
				continue
			for y in range(len(self.raw_map[x])):
				#print(x,y)
				if y > 95:
					continue
				if self.raw_map[x][y] == "G":
					self.background2[x][y] = MapObject.grass(x + 1, y + 1)
				elif self.raw_map[x][y] == "W":
					self.background2[x][y] = MapObject.wall(x + 1, y + 1)
				elif self.raw_map[x][y] == "T":
					self.background2[x][y] = MapObject.tree(x + 1, y + 1)
				elif self.raw_map[x][y] == "A":
					self.background2[x][y] = MapObject.water(x + 1, y + 1)
				elif self.raw_map[x][y] == "F":
					self.background2[x][y] = MapObject.floor(x + 1, y + 1)
				elif self.raw_map[x][y] == "D":
					self.background2[x][y] = MapObject.door(x + 1, y + 1)
				elif self.raw_map[x][y] == "b":
					self.background2[x][y] = MapObject.bridge(x + 1, y + 1)
				elif self.raw_map[x][y] == "g":
					self.background2[x][y] = MapObject.tall_grass(x + 1, y + 1) 
				elif self.raw_map[x][y] == "h":
					self.background2[x][y] = MapObject.hole(x + 1, y + 1)
				elif self.raw_map[x][y] == "w":
					self.background2[x][y] = MapObject.false_wall(x + 1, y + 1)
				elif self.raw_map[x][y] == "c":
					self.background2[x][y] = MapObject.castle_wall(x + 1, y + 1)
				elif self.raw_map[x][y] == "C":
					self.background2[x][y] = MapObject.cobblestone(x + 1, y + 1)
				elif self.raw_map[x][y] == "(":
					self.background2[x][y] = MapObject.fence_left(x + 1, y + 1)
				elif self.raw_map[x][y] == ")":
					self.background2[x][y] = MapObject.fence_right(x + 1, y + 1)
				elif self.raw_map[x][y] == "-":
					self.background2[x][y] = MapObject.fence_middle(x + 1, y + 1)
				elif self.raw_map[x][y] == "{":
					self.background2[x][y] = MapObject.grass_fence_left(x + 1, y + 1)
				elif self.raw_map[x][y] == "}":
					self.background2[x][y] = MapObject.grass_fence_right(x + 1, y + 1)
				elif self.raw_map[x][y] == "_":
					self.background2[x][y] = MapObject.grass_fence_middle(x + 1, y + 1)
				elif self.raw_map[x][y] == "#":
					self.background2[x][y] = MapObject.tree_top(x + 1, y + 1)
				elif self.raw_map[x][y] == "<":
					self.background2[x][y] = MapObject.tree_bot_left(x + 1, y + 1)
				elif self.raw_map[x][y] == ">":
					self.background2[x][y] = MapObject.tree_bot_right(x + 1, y + 1)
				elif self.raw_map[x][y] == "*":
					self.background2[x][y] = MapObject.wooden_chair(x + 1, y + 1)
				elif self.raw_map[x][y] == "m":
					self.background2[x][y] = MapObject.beer(x + 1, y + 1)
				elif self.raw_map[x][y] == "+":
					self.background2[x][y] = MapObject.floor_fence_middle(x + 1, y + 1)
				elif self.raw_map[x][y] == "d":
					self.background2[x][y] = MapObject.visble_door(x + 1, y + 1)
				elif self.raw_map[x][y] == "U":
					self.background2[x][y] = MapObject.under_wall(x + 1, y + 1)
				elif self.raw_map[x][y] == "u":
					self.background2[x][y] = MapObject.under_wall_torch(x + 1, y + 1)
				elif self.raw_map[x][y] == "s":
					self.background2[x][y] = MapObject.sign(x + 1, y + 1)
				elif self.raw_map[x][y] == "f":
					self.background2[x][y] = MapObject.wheat(x + 1, y + 1)
				elif self.raw_map[x][y] == "e":
					self.background2[x][y] = MapObject.fire(x + 1, y + 1)
				elif self.raw_map[x][y] == "E":
					self.background2[x][y] = MapObject.window(x + 1, y + 1)
				elif self.raw_map[x][y] == "7":
					self.background2[x][y] = MapObject.carpetUL(x + 1, y + 1)
				elif self.raw_map[x][y] == "9":
					self.background2[x][y] = MapObject.carpetUR(x + 1, y + 1)
				elif self.raw_map[x][y] == "1":
					self.background2[x][y] = MapObject.carpetLL(x + 1, y + 1)
				elif self.raw_map[x][y] == "3":
					self.background2[x][y] = MapObject.carpetLR(x + 1, y + 1)
				elif self.raw_map[x][y] == "4":
					self.background2[x][y] = MapObject.carpetVLINE(x + 1, y + 1)
				elif self.raw_map[x][y] == "8":
					self.background2[x][y] = MapObject.carpetHLINE(x + 1, y + 1)
				elif self.raw_map[x][y] == "5":
					self.background2[x][y] = MapObject.carpet(x + 1, y + 1)
				elif self.raw_map[x][y] == "0":
					self.background2[x][y] = MapObject.carpetdiamond(x + 1, y + 1)
				elif self.raw_map[x][y] == "R":
					self.background2[x][y] = MapObject.castle_wall_walkable(x + 1, y + 1)
				elif self.raw_map[x][y] == "r":
					self.background2[x][y] = MapObject.under_wall_walkable(x + 1, y + 1)
				else:
					print(self.raw_map[x][y])
					print("Could not create map tile from Text")
		
	def get_raw_map(self):
		_raw = []
		for x in range(len(self.background2)):
			_raw.append([])
			for y in range(len(self.background2[0])):
				if self.background2[x][y].walkable:
					_raw[x].append(0)
				else:
					_raw[x].append(1)

		return _raw





	def update_objects(self):
		for item in self.objects:
			item.turn_action()

	def draw_map(self, state, inverted = False):
		#for item in self.background:
		#	item.draw(screen)
		for x in range(len(self.background2)):
			for y in range(len(self.background2[x])):
				if not inverted:
					self.background2[x][y].draw(state)
				else:
					self.background2[x][y].draw(state, inverted=True)
		#for item in self.objects:
		#	item.draw(screen)
		
		#self.update_objects()

	def draw_map_efficient(self, state):
		screen = state.game_box
		player = state.player
		for x in range(player.x - 10, player.x + 10):
			if x < 0 or x > 38:
				continue
			for y in range(player.y - 10, player.y + 10):
				if y < 0 or y > 90:
					continue
				try:
					self.background2[x][y].draw(screen)
				except IndexError:
					pass
	def draw_vision(self, state, screen, draw_seen=True):
		self.objects_to_draw = []
		object_coords = {}
		for item in self.objects:
			object_coords[(item.x - 1, item.y - 1)] = item
		state.game_box.erase()

		if draw_seen:
			self.draw_seen(state)

		for i in range(0,360, 2):
			x = math.cos(i * 0.01745)
			y = math.sin(i * 0.01745)
			self.do_fov(x, y, state, screen, object_coords, i)

		for item in self.objects:
			if item not in self.objects_to_draw:
				item.visible = False
		for item in self.objects_to_draw:
			item.draw(state)
		#self.update_objects()

	def do_fov(self, x, y, state, screen, objects, a):
		ox = state.player.x - 1 + 0.5
		oy = state.player.y - 1 + 0.5
		vision_range = 10
		for i in range(vision_range + abs(round(5*math.sin(a * 0.01745)))):
			if ox < 0 or oy < 0:
				return
			try:
				self.background2[int(ox)][int(oy)].draw(state)
				if self.background2[int(ox)][int(oy)].walkable == False or self.background2[int(ox)][int(oy)].visible == False:
						if self.background2[int(ox)][int(oy)] not in self.seen:
							self.seen.append(self.background2[int(ox)][int(oy)])
				if self.background2[int(ox)][int(oy)].visible == False:
					return
			except IndexError:
				pass
			try:
				obj = objects[(int(ox), int(oy))]
				obj.visible = True
				self.objects_to_draw.append(obj)
			except KeyError:
				pass
			
			ox += x
			oy += y
	def draw_seen(self, state):
		for item in self.seen:
			item.draw(state, seen=True)
if __name__ == '__main__':
	gamemap = GameMap("map1.txt", [])
	gamemap.make_background()
