import curses
import random
import time
import npc
import os

curses.initscr()
curses.start_color()
curses.use_default_colors()

# CHECK COLORS.PY FOR COLORS


class MapObject():
	def __init__(self, x, y, character, walkable=True, color=False, executable=False, colors=False, name=False):
		self.x = x
		self.y = y
		self.character = character
		self.walkable = walkable
		self.color = color
		self.colors = colors
		self.executable = executable
		self.name = name

	@classmethod
	def tree(cls, x, y):
		return cls(x, y, "T", walkable=False, color=24, name="Tree")

	@classmethod
	def wall(cls, x, y):
		return cls(x, y, "#", walkable=False, color=96, name="Wall")

	@classmethod
	def floor(cls, x, y):
		return cls(x, y, " ", walkable=True, color=54, name="Floor")

	@classmethod
	def grass(cls, x, y):
		return cls(x, y, "'", walkable=True, color=42, name="Grass")

	@classmethod
	def water(cls, x, y):
		return cls(x, y, "'", walkable=False, color=21, name="Water")

	@classmethod
	def door(cls, x, y):
		return cls(x, y, "'", walkable=True, color=209, executable=True, name="Door")

	@classmethod
	def bridge(cls, x, y):
		return cls(x, y, "'", walkable=True, color=96, name="Bridge")

	@classmethod
	def tall_grass(cls,x,y):
		return cls(x, y, curses.ACS_PLMINUS, walkable=True, color=132, name="Tall Grass")



	def draw(self, screen):

		if self.colors:
			if self.color == False:
				self.color, useless = self.colors
			if self.color == self.colors[1]:
				self.color, useless = self.colors
			elif self.color == self.colors[0]:
				useless, self.color = self.colors
		if self.color:
			screen.attron(curses.color_pair(self.color))
			screen.addch(self.x, self.y, self.character)
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
				#print("for x = {}, for y = {} obj_x = {} obj_y = {}".format(x,y,self.background2[x][y].x, self.background2[x][y].y))
				self.background2[x][y].draw(screen)
		for item in self.objects:
			item.draw(screen)
		self.update_objects()


if __name__ == '__main__':
	gamemap = GameMap("map1.txt", [])
	gamemap.make_background()
