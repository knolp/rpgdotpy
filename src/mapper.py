import curses
import random
import time
import npc
import os
import math

curses.initscr()
curses.start_color()
curses.use_default_colors()

# CHECK COLORS.PY FOR COLORS


class MapObject():
	def __init__(self, x, y, character, walkable=True, color=False, executable=False, colors=False, name=False, visible=True):
		self.x = x
		self.y = y
		self.character = character
		self.walkable = walkable
		self.color = color
		self.colors = colors
		self.executable = executable
		self.name = name
		self.visible = visible

	@classmethod
	def tree(cls, x, y):
		return cls(x, y, "T", walkable=False, color=24, visible=False, name="Tree")

	@classmethod
	def wall(cls, x, y):
		return cls(x, y, "#", walkable=False, color=96, visible=False, name="Wall")

	@classmethod
	def floor(cls, x, y):
		return cls(x, y, " ", walkable=True, color=54, name="Floor")

	@classmethod
	def grass(cls, x, y):
		return cls(x, y, "'", walkable=True, color=[42], name="Grass")

	@classmethod
	def water(cls, x, y):
		return cls(x, y, "~", walkable=False, color=21, name="Water")

	@classmethod
	def door(cls, x, y):
		return cls(x, y, "%", walkable=True, color=209, executable=True, visible=False, name="Door")

	@classmethod
	def bridge(cls, x, y):
		return cls(x, y, ".", walkable=True, color=96, name="Bridge")

	@classmethod
	def tall_grass(cls,x,y):
		return cls(x, y, curses.ACS_PLMINUS, walkable=True, color=132, name="Tall Grass")

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
		return cls(x, y, curses.ACS_BULLET, walkable=True, color=139, name="Cobblestone")

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
		return cls(x, y, curses.ACS_CKBOARD, walkable=False, color=143, name="Tree Top")

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


	def draw(self, screen, seen=False):
		if type(self.color) == list:
			self.color = random.choice(self.color)

		if self.colors:
			if self.color == False:
				self.color, useless = self.colors
			if self.color == self.colors[1]:
				self.color, useless = self.colors
			elif self.color == self.colors[0]:
				useless, self.color = self.colors
		if self.color and seen == False:
			screen.attron(curses.color_pair(self.color))
			screen.addch(self.x, self.y, self.character)
			screen.attroff(curses.color_pair(self.color))
		elif self.color and seen == True:
			screen.attron(curses.color_pair(self.color))
			screen.addch(self.x, self.y, self.character, curses.A_REVERSE)
			screen.attroff(curses.color_pair(self.color))
		else:
			screen.addstr(self.x, self.y, self.character)


class GameMap():
	def __init__(self, map_file, objects, events=False):
		map_file = "{}\maps\{}".format(os.getcwd(),map_file)
		with open(map_file, "r") as f:
			self.raw_map = f.readlines()
			for i in range(len(self.raw_map)):
				self.raw_map[i] = self.raw_map[i].replace("\n", "")
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
				else:
					print(self.raw_map[x][y])
					print("Could not create map tile from Text")



	def update_objects(self):
		for item in self.objects:
			item.turn_action()

	def draw_map(self, screen):
		#for item in self.background:
		#	item.draw(screen)
		for x in range(len(self.background2)):
			for y in range(len(self.background2[x])):
				self.background2[x][y].draw(screen)
		for item in self.objects:
			item.draw(screen)
		
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
	def draw_vision(self, state, screen):
		self.objects_to_draw = []
		object_coords = {}
		for item in self.objects:
			object_coords[(item.x - 1, item.y - 1)] = item
		state.game_box.clear()

		self.draw_seen(screen)

		for i in range(0,360, 2):
			x = math.cos(i * 0.01745)
			y = math.sin(i * 0.01745)
			self.do_fov(x, y, state, screen, object_coords, i)

		for item in self.objects_to_draw:
			item.draw(screen)
		#self.update_objects()

	def do_fov(self, x, y, state, screen, objects, a):
		ox = state.player.x - 1 + 0.5
		oy = state.player.y - 1 + 0.5
		vision_range = 10
		for i in range(vision_range + abs(round(5*math.sin(a * 0.01745)))):
			if ox < 0 or oy < 0:
				return
			try:
				self.background2[int(ox)][int(oy)].draw(screen)
				if self.background2[int(ox)][int(oy)].walkable == False or self.background2[int(ox)][int(oy)].visible == False:
						if self.background2[int(ox)][int(oy)] not in self.seen:
							self.seen.append(self.background2[int(ox)][int(oy)])
				if self.background2[int(ox)][int(oy)].visible == False:
					return
			except IndexError:
				pass
			try:
				self.objects_to_draw.append(objects[(int(ox), int(oy))])
			except KeyError:
				pass
			
			ox += x
			oy += y
	def draw_seen(self, screen):
		for item in self.seen:
			item.draw(screen, seen=True)
if __name__ == '__main__':
	gamemap = GameMap("map1.txt", [])
	gamemap.make_background()
