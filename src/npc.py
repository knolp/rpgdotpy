import curses
import random
import time
import monster
import battle
import actions
import items

class NPC():
	def __init__(self, name, x, y, character):
		self.name = name
		self.x = x
		self.y = y
		self.character = character
		self.type = "npc"

	def draw(self, screen):
		screen.attron(curses.color_pair(197))
		screen.addch(self.x, self.y, self.character)
		screen.attroff(curses.color_pair(197))

	def turn_action(self):
		pass

	def action(self):
		print("Not implemented")


class Usable():
	def __init__(self, name, x, y, character):
		self.name = name
		self.x = x
		self.y = y
		self.character = character
		self.type = "usable"

	def draw(self, screen):
		screen.attron(curses.color_pair(142))
		screen.addch(self.x, self.y, self.character)
		screen.attroff(curses.color_pair(142))

	def turn_action(self):
		pass

	def action(self):
		print("Not implemented")





class Human(NPC):
	def __init__(self, name, x, y):
		super().__init__(name,x,y,"@")
		self.original_x = x
		self.original_y = y
		self.old_timestamp = int(time.time())

	def turn_action(self):
		max_range = 4
		direction = random.randint(1,4)
		new_timestamp = int(time.time())
		if new_timestamp - self.old_timestamp > 1:
			self.old_timestamp = new_timestamp
		else:
			return

		if direction == 1:
			if self.y + 1 <= max_range + self.original_y:
				self.y += 1

		elif direction == 2:
			if self.y- 1 >= self.original_y - max_range:
				self.y -= 1

		elif direction == 3:
			if self.x + 1 <= max_range + self.original_x:
				self.x += 1

		elif direction == 4:
			if self.x - 1 >= self.original_x - max_range:
				self.x -= 1
		else:
			pass

# STARTER TOWN
class ErolKipman(NPC):
	def __init__(self, x, y):
		name = "Erol Kipman"
		super().__init__(name,x,y,"E")
		self.original_x = x
		self.original_y = y
		self.old_timestamp = int(time.time())

	def turn_action(self):
		pass

	def action(self, screen, state):
		actions.SpeakErolKipman(screen, state).execute()


class OskGhar(NPC):
	inventory = [
		items.Longsword(),
		items.DeverBerry(),
		items.BasementKey()
	]
	name = "Osk'Ghar the Rock"
	def __init__(self, x, y):
		name = "Osk'Ghar the Rock"
		super().__init__(name,x,y,"O")
		self.original_x = x
		self.original_y = y
		self.old_timestamp = int(time.time())

	def turn_action(self):
		pass

	def action(self, screen, state):
		actions.SpeakOskGhar(screen, state).execute()


# The 4 adventurers
class BaldirKragg(NPC):
	def __init__(self, x, y):
		name = "Baldir Kragg"
		super().__init__(name,x,y,"B")
		self.original_x = x
		self.original_y = y
		self.old_timestamp = int(time.time())

	def turn_action(self):
		pass

	def action(self, screen, state):
		actions.SpeakBaldirKragg(screen, state).execute()

class BodvarKragg(NPC):
	def __init__(self, x, y):
		name = "Bodvar Kragg"
		super().__init__(name,x,y,"B")
		self.original_x = x
		self.original_y = y
		self.old_timestamp = int(time.time())

	def turn_action(self):
		pass

	def action(self, screen, state):
		actions.SpeakBodvarKragg(screen, state).execute()

class EvanKripter(NPC):
	def __init__(self, x, y):
		name = "Evan Kripter"
		super().__init__(name,x,y,"E")
		self.original_x = x
		self.original_y = y
		self.old_timestamp = int(time.time())

	def turn_action(self):
		pass

	def action(self, screen, state):
		actions.SpeakEvanKripter(screen, state).execute()
	
class LarsMagnus(NPC):
	def __init__(self, x, y):
		name = "Lars Magnus"
		super().__init__(name,x,y,"L")
		self.original_x = x
		self.original_y = y
		self.old_timestamp = int(time.time())

	def turn_action(self):
		pass

	def action(self, screen, state):
		actions.SpeakLarsMagnus(screen, state).execute()













#Monsters

class Monster():
	def __init__(self, name, x, y, character, state):
		self.name = name
		self.x = x
		self.y = y
		self.character = character
		self.state = state
		self.type = "monster"

	def draw(self, screen):
		screen.addstr(self.x -1, self.y - 1, "N/A")
		screen.attron(curses.color_pair(240))
		screen.addch(self.x, self.y, self.character)
		screen.attroff(curses.color_pair(240))

	def turn_action(self):
		pass

	def action(self):
		print("Not implemented")



class Rat(Monster):
	def __init__(self, x, y, state):
		super().__init__("Rat", x, y, "R", state)

	def action(self):
		result = battle.Battle(self.state, monster.Rat(), "3").play()
		return result

	def draw(self, screen):
		text = "RAT"
		screen.addstr(self.x - 1, self.y - int((len(text) / 2)), text)
		screen.attron(curses.color_pair(240))
		screen.addch(self.x, self.y, self.character)
		screen.attroff(curses.color_pair(240))

class RatKing(Monster):
	def __init__(self, x, y, state):
		super().__init__("RatKing", x, y, "R", state)

	def action(self, run=True):
		result = battle.Battle(self.state, monster.RatKing(), "3", run=run).play()
		return result

	def draw(self, screen):
		text = "RATKING"
		screen.addstr(self.x - 1, self.y - int((len(text) / 2)), text)
		screen.attron(curses.color_pair(240))
		screen.addch(self.x, self.y, self.character)
		screen.attroff(curses.color_pair(240))



class SkeletonGrunt(Monster):
	def __init__(self, x, y, state):
		super().__init__("SkeletonGrunt", x, y, "S", state)

	def action(self, run=False):
		result = battle.Battle(self.state, monster.SkeletonGrunt(), "3", run=run).play()
		return result

	def draw(self, screen):
		text = "SKG"
		screen.addstr(self.x - 1, self.y - int((len(text) / 2)), text)
		screen.attron(curses.color_pair(240))
		screen.addch(self.x, self.y, self.character)
		screen.attroff(curses.color_pair(240))

































# Objects

class BasementLever(Usable):
	def __init__(self, x, y):
		name = "BasementLever"
		self.readable_name = "Basement Lever"
		super().__init__(name,x,y,"X")
		self.original_x = x
		self.original_y = y

	def turn_action(self):
		pass

	def action(self, screen, state):
		actions.BasementLeverTouch(screen, state).execute()

class Rock(Usable):
	def __init__(self, x, y):
		name = "Rock"
		self.readable_name = "Rock"
		super().__init__(name,x,y,"X")
		self.original_x = x
		self.original_y = y

	def turn_action(self):
		pass

	def action(self, screen, state):
		actions.Rock(screen, state).execute()

class BasementChest(Usable):
	def __init__(self, x, y):
		name = "BasementChest"
		self.readable_name = "Wooden Chest"
		super().__init__(name,x,y,"X")
		self.original_x = x
		self.original_y = y

	def turn_action(self):
		pass

	def action(self, screen, state):
		actions.BasementChestOpen(screen, state).execute()

class DeverBerries(Usable):
	def __init__(self, x, y, state):
		name = "DeverBerries"
		self.readable_name = "A patch of deverberries"
		super().__init__(name,x,y,"%")
		self.original_x = x
		self.original_y = y
		self.screen = state.stdscr
		self.state = state

	def turn_action(self):
		pass

	def action(self, screen, state):
		actions.DeverBerryPick(self.screen, self.state).execute()







if __name__ == '__main__':
	human = Human("Niklas", 13, 37)
	print(human.name, human.x, human.y, human.character)