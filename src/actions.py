import npc
import items
import helper
import inventory
import curses
from curses.textpad import Textbox, rectangle
# Actions the player can do, such as read signs and interact with NPC:s, should either do stuff or open dialog box etc


def input_text(name, vocation, screen, text, state):
	screen.clear()
	start = 10
	screen.attron(curses.color_pair(135))
	screen.addstr(5, 34, name)
	screen.addstr(6, 34, vocation)
	screen.attroff(curses.color_pair(135))
	for item in text:
		if "[" in item:
			before, keyword, after = item.split("[")[0], item.split("[")[1].split("]")[0], item.split("]")[1]
			screen.addstr(start,34,before)
			screen.attron(curses.color_pair(136))
			screen.addstr(start,34 + len(before),keyword)
			screen.attroff(curses.color_pair(136))
			screen.addstr(start, 34 + len(before) + len(keyword), after)
		else:
			screen.addstr(start, 34, item)
		start += 1
	screen.addstr(23,34, "Enter message:")
	screen.addstr(26,34, "-----------------------------")
	screen.addstr(27,34,"[Enter] to send. 'bye' or 'exit' to quit.")
	window = curses.newwin(1,30,25,35)
	screen.refresh()

	tbox = Textbox(window)

	tbox.edit()

	text = tbox.gather()

	return text.strip(" ")


def add_ungetch(f):
	def return_func(self):
		f(self)
		curses.ungetch(curses.KEY_F0)
	return return_func



class Action():
	def __init__(self, screen, state, action_name):
		self.screen = state.stdscr
		self.state = state
		self.action_name = action_name

	def execute(self):
		pass


#STARTER TOWN
class SpeakErolKipman(Action):
	def __init__(self, screen, state):
		super().__init__(screen, state, "Speak")
		self.name = "Erol Kipman"
		self.vocation = "Starter Town Sheriff"

	@add_ungetch
	def execute(self):
		text_state = 0
		text = [
				"Hi there!",
				"My name is [Erol Kipman], Sheriff of Starter Town",
				"Are you new here?"
			]
		while True:
			answer = input_text(self.name, self.vocation, self.screen, text, self.state)

			#General
			if answer.lower() in ["e", "exit", "bye", "q", "quit"]:
				return False
			elif answer.lower() in ["rumours", "hints", "gossip"]:
				text = [
					"Hmm, I haven't heard much.",
					"People are not to keen to share gossip with the",
					"strong arm of the law."
					]
				continue
			elif answer.lower() in ["quests", "quest"]:
				text = [
					"I sadly have no [quests] for you.",
					"If you are looking for one I think",
					"the blacksmith [Osk'Ghar] may have some trouble."
				]

			elif answer.lower() in ["trade", "barter"]:
				text = ["Do I look like a merchant to you?"]

			elif answer.lower() in ["burial site", "dark arts", "necromancy", "undead", "dead", "haunted"]:
				text = [
					"The house across the road from [Osk'Ghar]'s workshop is said to be haunted.",
					"",
					"When the previous tenants started to renovate the floors, they found an",
					"old burial site underneath.",
					"",
					"Rumours are that the townfolk have seen hooded men entering at night",
					"which is why I am posted here."
				]

			#Specific
			elif answer.lower() == "yes" and text_state == 0:
				text_state = 1
				text = [
					"Yes, I thought I saw a new face.",
					"Feel free to wander around as you see fit.",
					"I recommend you check out the blacksmith, [Osk'Ghar]",
					"if you are in need of a [quest]."]
				continue
			elif answer.lower() in ["oskghar", "osk'ghar", "blacksmith", "smith"]:
				text = [
					"[Osk'Ghar] is the town blacksmith.",
					"",
					"He lives in the house next to where I am posted."
				]



			#catch-all
			else:
				text = [
					"Huh?",
					"I didn't quite catch that.",
					"",
					"Did you want to [Trade]?",
					"Or did you want some [Hints]?"
				]


class SpeakOskGhar(Action):
	def __init__(self, screen, state):
		super().__init__(screen, state, "Speak")
		self.name = "Osk'Ghar the Rock"
		self.vocation = "Starter Town Blacksmith"
	
	@add_ungetch
	def execute(self):
		print(self.state.player.flags)
		if "RatMenace_started" in self.state.player.flags:
			text_state = 2
			if "RatMenace_rat1_killed" in self.state.player.flags:
				if "RatMenace_rat2_killed" in self.state.player.flags:
					if "RatMenace_rat3_killed" in self.state.player.flags:
						if "RatMenace_rat_king_killed" in self.state.player.flags:
							self.state.player.flags.append("RatMenace_completed")
			if "RatMenace_completed" in self.state.player.flags:
				text_state = 3
		else:
			text_state = 0
		text = [
				"Oh, a customer!",
				"I am [Osk'Ghar the Rock], the blacksmith.",
				"What can I do for you?"
			]
		while True:
			answer = input_text(self.name, self.vocation, self.screen, text, self.state)

			#General
			if answer.lower() in ["e", "exit", "bye", "q", "quit"]:
				return False
			elif answer.lower() in ["rumours", "hints", "gossip"]:
				text = [
					"Rumours, eh?",
					"Well, I just sold some swords to a",
					"group of [adventurers] heading to a cave",
					"up north, that could get interesting."
					]
				continue
			elif answer.lower() in ["adventurers"]:
				text = [
					"Last I saw of them, they headed into town up north.",
					"",
					"Odd group I must say, an Elf, a Human and two Dwarf brothers.",
					"One was even a fabled [Berserker]!"
				]
			elif answer.lower() in ["berserker"]:
				text = [
					"Dwarves have lost their god, and without a god to follow",
					"some have seeked out to the old primal ones, sacrificing their",
					"lifespan for enormous power.",
					"",
					"Most other races abolish this behaviour, Orcs included.",
					"His companions must be desperate to take one of them into their following."
				]
			elif answer.lower() in ["quests", "quest"]:
				if text_state == 0:
					text = [
						"I have a great quest for you if you wish.",
						"You see, I have a...",
						"",
						"*cough* Rodent problem. *cough*",
						"",
						"It's a bit embarassing being an Orc and",
						"still afraid of a few measly rats.",
						"Will you help me out with this?"
					]
					text_state = 1
				
				elif text_state == 2:
					text = [
						"You are already on a quest for me,",
						"You need to slay those pesky rats, remember?"
					]
				
				elif text_state == 3:
					text = [
						"So you slayed them all!",
						"Feel free to take an item from the",
						"chest behind me as a token of ",
						"appreciation."
					]
					self.state.player.flags.append("RatMenace_reward")
			

			elif answer.lower() in ["trade", "barter"]:
				text = [
					"Do I look like a merchant to you?",
					"Actually yes, so implement trading here."
				]
				inventory.trade(npc.OskGhar, self.screen, self.state)

			
			elif answer.lower() in ["door", "locked"]:
				text = [
					"The door in the backroom is locked,",
					"But I am willing to give it to you if",
					"you help me with my [Quest]."
				]

			#catch-all
			else:
				text = [
					"Huh?",
					"I didn't quite catch that.",
					"",
					"Did you want to [Trade]?",
					"Or did you want some [Hints]?"
				]


			#Specific
			if answer.lower() == "yes" and text_state == 1:
				text_state = 2
				self.state.player.flags.append("RatMenace_started")
				text = [
					"Great!",
					"Take this key and go down the basement in",
					"the room to the west.",
					"",
					"	[Basement Key added to inventory]",
					"",
					"And remember, be careful!"
					]
				self.state.player.inventory.append(items.BasementKey())
				continue


class SpeakBaldirKragg(Action):
	def __init__(self, screen, state):
		super().__init__(screen, state, "Speak")
		self.name = "Baldir Kragg"
		self.vocation = "Dwarf Berserker"
	
	@add_ungetch
	def execute(self):
		text_state = 0
		text = [
			"The dwarf seems have drunk himself to sleep."
		]

		while True:
			answer = input_text(self.name, self.vocation, self.screen, text, self.state)

			if answer.lower() in ["e", "exit", "bye", "q", "quit"]:
				return False

			else:
					text = [
						"You get no response from the dwarf."
					]

class SpeakBodvarKragg(Action):
	def __init__(self, screen, state):
		super().__init__(screen, state, "Speak")
		self.name = "Bodvar Kragg"
		self.vocation = "Dwarf Warrior"
	
	@add_ungetch
	def execute(self):
		text_state = 0
		text = [
			"The dwarf seems have drunk himself to sleep."
		]

		while True:
			answer = input_text(self.name, self.vocation, self.screen, text, self.state)

			if answer.lower() in ["e", "exit", "bye", "q", "quit"]:
				return False

			else:
					text = [
						"You get no response from the dwarf."
					]


class SpeakEvanKripter(Action):
	def __init__(self, screen, state):
		super().__init__(screen, state, "Speak")
		self.name = "Evan Kripter"
		self.vocation = "Elf Ranger"
	
	@add_ungetch
	def execute(self):
		text_state = 0
		if "EvanKripter_met" not in self.state.player.flags:
			text = [
				"Hello there!",
				"My name is Evan Kripter, one of the famous 'Four Adventurers'",
				"",
				"Don't let my appearance scare you, I am not like the other elves."
			]
			self.state.player.flags.append("EvanKripter_met")
		else:
			text = [
				"What can I do for you, friend?"
			]

		while True:
			answer = input_text(self.name, self.vocation, self.screen, text, self.state)

			if answer.lower() in ["e", "exit", "bye", "q", "quit"]:
				return False
			elif answer.lower() in ["brew", "potion", "wake up", "wakeup", "wake", "elven brew"]:
				text = [
					"Ah yes, I spoke of the Adr'al brew.",
					"",
					"If you can get me some [deverberries] I am happy to make it for you.",
					"Can be difficult and dangerous to find around here though."
				]
			elif answer.lower() in ["berries", "berry", "deverberries", "deverberry"]:
				text = [
					"[Deverberries] can usually be found near the burial sites of the dead",
					"They grow exceptionally often where necromancy or dark arts have been performed."
				]

			else:
					text = [
						"Huh?"
					]

class SpeakLarsMagnus(Action):
	def __init__(self, screen, state):
		super().__init__(screen, state, "Speak")
		self.name = "Lars Magnus"
		self.vocation = "Human Warrior"
	
	@add_ungetch
	def execute(self):
		text_state = 0
		if "LarsMagnus_met" not in self.state.player.flags:
			text = [
				"Hi there!",
				"",
				"I apologize for the behavior of my two dwarf friends.",
				"",
				"I hope they didn't disturb you, but they seemed to have passed out."
			]
			self.state.player.flags.append("LarsMagnus_met")
		else:
			text = [
				"Hello again!",
				"How may I help you?"
			]

		while True:
			answer = input_text(self.name, self.vocation, self.screen, text, self.state)
			print(answer)

			if answer.lower() in ["e", "exit", "bye", "q", "quit"]:
				return False

			elif answer.lower() in ["yes", "y"] and "WakeUpCall_started" not in self.state.player.flags:
				if text_state == 1:
					self.state.player.flags.append("WakeUpCall_started")
					text = [
						"Splendid!",
						"",
						"You should talk to [Evan Kripter].",
						"He spoke of some elven brew that might help before you came in"
					]
			elif answer.lower() == "dwarf brothers":
				text = [
					"Ah yes, the lovely gentlement at the other end of the table.",
					"",
					"One's a barbarian and the other a warrior.",
					"Great to have in combat, not so much anywhere else."
				]

			elif answer.lower() in ["evan kripter", "evan", "kripter"]:
				text = [
					"[Evan Kripter] is the Elf Ranger in front of me.",
					"You can't miss him."
				]

			elif answer.lower() in ["quests", "quest"]:
				text = [
					"Unfortunately we have no quest for you.",
					"",
					"We are actually heading on our own quest, to a cave of necromancers up north.",
					"As soon as we can get these two [Dwarf brothers] to wake up that is.",
					"",
					"Do you think you could help us out with that?"
				]
				if "WakeUpCall_started" in self.state.player.flags:
					text = [
						"We still need to wake up these dwarves before we head out.",
						"Let me know if you got any potions or brews"
					]
				text_state = 1

			else:
					text = [
						"Huh?"
					]





# Objects

# BASEMENT OSKGHAR

class BasementLeverTouch(Action):
	def __init__(self, screen, state):
		super().__init__(screen, state, "Speak")
		self.name = "BasementLever"
	
	@add_ungetch
	def execute(self):
		pulled = helper.yes_no(self.screen, self.state, [
			"You see and old, rusty lever.",
			"",
			"Do you pull it?"
		])

		if pulled:
			for item in self.state.gamemap.game_map.objects:
				if item.name == "Rock":
					self.state.gamemap.game_map.objects.remove(item)
		#curses.ungetch(curses.KEY_F0)

class Rock(Action):
	def __init__(self, screen, state):
		super().__init__(screen, state, "Speak")
		self.name = "Rock"
	
	def execute(self):
		helper.popup(self.screen, self.state, [
			"There is a rock in the way.",
			"",
			"it looks unusal though, as if it's",
			"connected to some kind of contraption."
		])

class BasementChestOpen(Action):
	def __init__(self, screen, state):
		super().__init__(screen, state, "Open")
		self.name = "BasementChestOpen"
		self.readable_name = "Wooden Chest"

	def execute(self):
		answer = helper.yes_no(self.screen, self.state, [
			"A wooden chest",
			"",
			"It seems to not be locked",
			"Do you open it?"

		])
		loot = []
		if "BasementChest_item_taken_MoonlightSword" not in self.state.player.flags:
			loot.append("MoonlightSword")
		if answer == True:
			taken = inventory.open_chest(self.screen, self.state, self.readable_name, loot)
			for item in taken:
				if "BasementChest_item_taken_{}".format(item.name) not in self.state.player.flags:
					self.state.player.flags.append("BasementChest_item_taken_{}".format(item.name))
			
		else:
			return

class DeverBerryPick(Action):
	def __init__(self, screen, state):
		super().__init__(screen, state, "pick")
		self.name = "DeverBerryPick"
		self.readable_name = "A patch of deverberries"

	def execute(self):
		if "WakeUpCall_deverberries_picked" in self.state.player.flags:
			helper.popup(self.screen, self.state, [
				"You do not want to pick more of these foul berries",
				"than you actually have to."
			])
			return
		answer = helper.yes_no(self.screen, self.state, [
			"A patch of deverberries seems to be growing on the damp floor.",
			"",
			"Do you pick one?"

			])

		if answer == True:
			self.state.player.inventory.append(items.DeverBerry())
			self.state.player.flags.append("WakeUpCall_deverberries_picked")

if __name__ == "__main__":
	pass