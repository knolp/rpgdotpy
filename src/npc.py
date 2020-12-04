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
import battlefields


class NPC():
	def __init__(self, name, x, y, character):
		self.name = name
		self.x = x
		self.y = y
		self.character = character
		self.type = "npc"
		self.visible = False
		self.quest = False

	def draw(self, state):
		screen = state.game_box
		if self.quest:
			screen.addch(self.x - 1, self.y, "!", curses.color_pair(138))
		screen.attron(curses.color_pair(197))
		screen.addch(self.x, self.y, self.character)
		screen.attroff(curses.color_pair(197))

	def turn_action(self):
		pass

	def action(self):
		print("Not implemented")

	def check_inbound(self):
		if self.x < 1 or self.x > 37:
			return False
		if self.y < 1 or self.y > 96:
			return False
		return True


class Usable():
	def __init__(self, name, x, y, character, color=142):
		self.name = name
		self.x = x
		self.y = y
		self.character = character
		self.type = "usable"
		self.color = color
		self.visible = False

	def draw(self, state):
		screen = state.game_box
		screen.attron(curses.color_pair(self.color))
		screen.addch(self.x, self.y, self.character)
		screen.attroff(curses.color_pair(self.color))

	def turn_action(self):
		pass

	def action(self):
		print("Not implemented")
	
	def check_inbound(self):
		if self.x < 1 or self.x > 37:
			return False
		if self.y < 1 or self.y > 96:
			return False
		return True





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

#Trade District Alchemist

class EmpaLinka(NPC):
	inventory = [
			items.ArcaneDust(),
			items.TrollHair(),
			items.DeverBerrySkinDried()
		]
	def __init__(self,x,y):
		name = "Empa Linka"
		super().__init__(name, x, y, "E")
		self.original_x = x
		self.original_y = y
	
	def turn_action(self):
		pass

	def action(self, screen, state):
		actions.SpeakEmpaLinka(screen, state).execute()

# Starter Town Dock
class EdwardGryll(NPC):
	def __init__(self, x, y):
		name = "Edward Gryll"
		super().__init__(name, x, y, "E")
		self.original_x = x
		self.original_y = y

	def turn_action(self):
		pass

	def action(self, screen, state):
		actions.SpeakEdwardGryll(screen, state).execute()

#Starter Town Tannery
class DidricBurton(NPC):
	inventory = [
		items.DeerHide()
	]
	name = "Didric Burton"
	def __init__(self, x, y):
		name = "Didric Burton"
		super().__init__(name,x,y,"D")
		self.original_x = x
		self.original_y = y
		self.old_timestamp = int(time.time())

	def turn_action(self):
		pass

	def action(self, screen, state):
		actions.SpeakDidricBurton(screen, state).execute()










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
		self.path = []
		self.speed = 1
		self.visible = False
		self.text = "N/A"

	def draw(self, state):
		screen = state.game_box
		try:
			screen.addstr(self.x - 1, self.y - int((len(self.text) / 2)), self.text)
			screen.attron(curses.color_pair(self.color))
			screen.addch(self.x, self.y, self.character)
			screen.attroff(curses.color_pair(self.color))
			return True
		except:
			print("WTF")
			return False

	def turn_action(self):
		pass

	def action(self):
		print("Not implemented")



class Rat(Monster):
	def __init__(self, x, y, state, flag=False, radar=False):
		super().__init__("Rat", x, y, "R", state, flag=flag, radar=radar)
		self.speed = 2
		self.text = "RAT"

	def action(self):
		result = battle.Battle(self.state, monster.Rat(self.state), "3").play()
		return result

		

class RatKing(Monster):
	def __init__(self, x, y, state, flag=False, radar=False):
		super().__init__("RatKing", x, y, "R", state, flag=flag, radar=radar)
		self.speed = 2
		self.text = "RATKING"

	def action(self, run=True):
		result = battle.Battle(self.state, monster.RatKing(self.state), "3", run=run).play()
		return result


class SkeletonGrunt(Monster):
	def __init__(self, x, y, state, flag=False, radar=False):
		super().__init__("SkeletonGrunt", x, y, "S", state, flag=flag, radar=radar)
		self.speed = 3
		self.text = "SKG"

	def action(self, run=False):
		result = battle.Battle(self.state, monster.SkeletonGrunt(self.state), battlefields.Battlefield("Dungeon"), run=run).play()
		return result





























class Smoke(Usable):
	def __init__(self, x, y):
		name = "Smoke"
		self.readable_name = "Smoke"
		super().__init__(name,x,y," ", color=random.choice([139, 248]))
		self.original_x = x
		self.original_y = y

	def turn_action(self):
		self.x -= 1
		self.y -= random.randint(-3,-1)

	def action(self, screen, state):
		pass


# Objects (Usable)

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

class WoodenChest(Usable):
	def __init__(self, x, y, flag, item_list, requirement = False):
		name = "WoodenChest"
		self.readable_name = "Wooden Chest"
		super().__init__(name,x,y,"X")
		self.original_x = x
		self.original_y = y
		self.flag = flag
		self.item_list = item_list
		self.requirement = requirement


	def turn_action(self):
		pass

	def action(self, screen, state):
		if (self.requirement and self.requirement in state.player.flags) or self.requirement == False:
			actions.WoodenChestOpen(screen, state, self).execute()
		else:
			helper.popup(screen,state,[
				"The chest is locked."
			])

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


class SingleBookCase(Usable):
	def __init__(self, x, y, state, book):
		name = "SingleBookCase"
		self.readable_name = "Bookcase (single)"
		self.book = book
		super().__init__(name,x,y,curses.ACS_CKBOARD,color=148)
		

	def turn_action(self):
		pass

	def action(self, screen, state):
		text = [
			"In this bookcase you see a book with the name",
			"",
			f"[{self.book.readable_name}]",
			f"by [{self.book.author}]",
			"",
			"Do you read it?"
		]
		answer = helper.yes_no(state.stdscr, state, text)

		if answer:
			self.book.read(state.stdscr)
			return
		else:
			return

class EmptyBookCase(Usable):
	def __init__(self, x, y, state, text):
		name = "EmptyBookCase"
		self.readable_name = "Bookcase (Empty)"
		self.text = text
		super().__init__(name,x,y,curses.ACS_CKBOARD,color=161)
		

	def turn_action(self):
		pass

	def action(self, screen, state):
		helper.popup(state.stdscr, state, self.text)




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
	def __init__(self, x, y, state, identity, color=153):
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