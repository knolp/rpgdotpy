import curses
import random
import time
import monster
import battle
import actions
import items
import alchemy
import farming
import helper


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
	def __init__(self, name, x, y, character, color=142):
		self.name = name
		self.x = x
		self.y = y
		self.character = character
		self.type = "usable"
		self.color = color

	def draw(self, screen):
		screen.attron(curses.color_pair(self.color))
		screen.addch(self.x, self.y, self.character)
		screen.attroff(curses.color_pair(self.color))

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
		items.ChainHelmet(),
		items.ChainMail(),
		items.IronMace(),
		items.Rapier(),
		items.LeatherBoots(),
		items.Buckler()
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

# Brown Bear Inn
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

#<!-- The 4 adventurers -->
class AbyrroQuatz(NPC):
	def __init__(self, x, y):
		name = "Abyrro Quatz"
		super().__init__(name, x, y, "A")
		self.original_x = x
		self.original_y = y
		
	def turn_action(self):
		pass

	def action(self, screen, state):
		actions.SpeakAbyrroQuatz(screen, state).execute()

# HALL OF JUSTICE

class BeccaLithe(NPC):
	def __init__(self, x, y):
		name = "Becca Lithe"
		super().__init__(name,x,y,"B")
		self.original_x = x
		self.original_y = y
		self.old_timestamp = int(time.time())

	def turn_action(self):
		pass

	def action(self, screen, state):
		actions.SpeakBeccaLithe(screen, state).execute()













#Monsters

class Monster():
	def __init__(self, name, x, y, character, state, flag=False, radar=False):
		self.name = name
		self.x = x
		self.y = y
		self.character = character
		self.state = state
		self.type = "monster"
		self.flag = flag
		self.radar = radar
		self.color = 240
		self.path_to_target = []

	def draw(self, screen):
		screen.addstr(self.x -1, self.y - 1, "N/A")
		screen.attron(curses.color_pair(self.color))
		screen.addch(self.x, self.y, self.character)
		screen.attroff(curses.color_pair(self.color))

	def turn_action(self):
		pass

	def action(self):
		print("Not implemented")



class Rat(Monster):
	def __init__(self, x, y, state, flag=False, radar=False):
		super().__init__("Rat", x, y, "R", state, flag=flag, radar=radar)

	def action(self):
		result = battle.Battle(self.state, monster.Rat(), "3").play()
		return result

	def draw(self, screen):
		text = "RAT"
		screen.addstr(self.x - 1, self.y - int((len(text) / 2)), text)
		screen.attron(curses.color_pair(self.color))
		screen.addch(self.x, self.y, self.character)
		screen.attroff(curses.color_pair(self.color))

class RatKing(Monster):
	def __init__(self, x, y, state, flag=False, radar=False):
		super().__init__("RatKing", x, y, "R", state, flag=flag, radar=radar)

	def action(self, run=True):
		result = battle.Battle(self.state, monster.RatKing(), "3", run=run).play()
		return result

	def draw(self, screen):
		text = "RATKING"
		screen.addstr(self.x - 1, self.y - int((len(text) / 2)), text)
		screen.attron(curses.color_pair(self.color))
		screen.addch(self.x, self.y, self.character)
		screen.attroff(curses.color_pair(self.color))



class SkeletonGrunt(Monster):
	def __init__(self, x, y, state, flag=False, radar=False):
		super().__init__("SkeletonGrunt", x, y, "S", state, flag=flag, radar=radar)

	def action(self, run=False):
		result = battle.Battle(self.state, monster.SkeletonGrunt(), "3", run=run).play()
		return result

	def draw(self, screen):
		text = "SKG"
		screen.addstr(self.x - 1, self.y - int((len(text) / 2)), text)
		screen.attron(curses.color_pair(self.color))
		screen.addch(self.x, self.y, self.character)
		screen.attroff(curses.color_pair(self.color))

































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
		super().__init__(name,x,y,"%",color=147)
		self.original_x = x
		self.original_y = y
		self.screen = state.stdscr
		self.state = state

	def turn_action(self):
		pass

	def action(self, screen, state):
		actions.DeverBerryPick(self.screen, self.state).execute()




# Player Housing Upgrades

class AlchemyTable(Usable):
	def __init__(self, x, y, state):
		name = "AlchemyTable"
		self.readable_name = "Alchemy Table"
		super().__init__(name, x, y, curses.ACS_PI, color=147)
		self.original_x = x
		self.original_y = y
		self.screen = state.stdscr
		self.state = state

	def turn_action(self):
		pass

	def action(self, screen, state):
		print(alchemy.make_potion(state))

class Juicer(Usable):
	def __init__(self, x, y, state):
		name = "Juicer"
		self.readable_name = "Juicer"
		super().__init__(name, x, y, "J", color=147)
		self.original_x = x
		self.original_y = y
		self.screen = state.stdscr
		self.state = state

	def turn_action(self):
		pass

	def action(self, screen, state):
		print(alchemy.make_juice(state))


#Farming patch ids
#StarterTown_house_1 = första från vänster i starter town house
#StarterTown_house_2 = ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#StarterTown_house_3 = ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#StarterTown_house_4 = ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

class FarmingPatch(Usable):
	def __init__(self, x, y, state, identity,color=153):
		name = "FarmingPatch"
		self.identity = identity
		self.readable_name = "Farming Patch"
		super().__init__(name, x, y, "F", color=color)
		self.original_x = x
		self.original_y = y
		self.screen = state.stdscr
		self.state = state

	def turn_action(self):
		pass

	def action(self, screen, state):
		farming.farming(self.state, self.identity)



# FLORA
class AriamBush(Usable):
	def __init__(self, x, y, state, flag, color=156):
		name="AriamBush"
		self.readable_name = "Ariam Bush"
		super().__init__(name,x,y,"%",color=color)
		self.original_x = x
		self.original_y = y
		self.screen = state.stdscr
		self.state = state
		self.flag = flag
	
	def action(self, screen, state):
		if self.flag not in [x[0] for x in state.player.flora]:
			text = [
				"Ariam Bush",
				"",
				"Do you pick some leaves of this bush?"
			]
			answer = helper.yes_no(state.stdscr, state, text)
			if answer:
				state.player.flora.append([self.flag, state.timer.tid, 10000])
				state.player.inventory.append(items.AriamLeaf())
				return
			else:
				return
		else:
			text = [
				"Ariam Bush",
				"",
				"This bush has been picked clean recently."
			]
			helper.popup(state.stdscr, state, text)
			return
		







if __name__ == '__main__':
	human = Human("Niklas", 13, 37)
	print(human.name, human.x, human.y, human.character)