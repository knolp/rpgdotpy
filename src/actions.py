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
	screen.addstr(5, 34, name)
	screen.addstr(6, 34, vocation)
	for item in text:
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
				"My name is Erol Kipman, Sheriff of Starter Town",
				"Are you new here?"
			]
		while True:
			answer = input_text(self.name, self.vocation, self.screen, text, self.state)

			#General
			if answer.lower() in ["e", "exit", "bye", "q", "quit"]:
				return False
			if answer.lower() in ["rumours", "hints", "gossip"]:
				text = [
					"Hmm, I haven't heard much.",
					"People are not to keen gossiping with the",
					"person who is in charge of the law."
					]
				continue
			if answer.lower() in ["quests", "quest"]:
				text = [
					"I sadly have no quests for you.",
					"If you are looking for one I think",
					"The blacksmith Osk'Ghar may have some trouble."
				]

			if answer.lower() in ["trade", "barter"]:
				text = ["Do I look like a merchant to you?"]


			#Specific
			if answer.lower() == "yes" and text_state == 0:
				text_state = 1
				text = [
					"Yes, I thought I saw a new face.",
					"Feel free to wander around as you see fit.",
					"I recommend you check out the blacksmith, Osk'Ghar",
					"if you are in need of a quest."]
				continue
			if answer.lower() in ["oskghar", "osk'ghar", "blacksmith", "smith"]:
				text = [
					"Osk'Ghar is the town blacksmith.",
					"",
					"He lives in the house next to where I am posted."
				]


class SpeakOskGhar(Action):
	def __init__(self, screen, state):
		super().__init__(screen, state, "Speak")
		self.name = "Osk'Ghar the Rock"
		self.vocation = "Starter Town Blacksmith"
	
	@add_ungetch
	def execute(self):
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
				"I am Osk'Ghar the Rock, the blacksmith.",
				"What can I do for you?"
			]
		while True:
			answer = input_text(self.name, self.vocation, self.screen, text, self.state)

			#General
			if answer.lower() in ["e", "exit", "bye", "q", "quit"]:
				return False
			if answer.lower() in ["rumours", "hints", "gossip"]:
				text = [
					"Rumours, eh?",
					"Well, I just sold some swords to a",
					"group of adventurers heading to a cave",
					"up north, that could get interesting."
					]
				continue
			if answer.lower() in ["quests", "quest"]:
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
			

			if answer.lower() in ["trade", "barter"]:
				text = [
					"Do I look like a merchant to you?",
					"Actually yes, so implement trading here."
				]
			
			if answer.lower() in ["door", "locked"]:
				text = [
					"The door in the backroom is locked,",
					"But I am willing to give it to you if",
					"you help me with my [Quest]."
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

if __name__ == "__main__":
	pass