import curses
import items
import abilities
import recipes
import states
from curses.textpad import Textbox, rectangle
import time


def time_print(f):
	def return_func(self, *args, **kwargs):
		start_time = time.time()
		res = f(self, *args, **kwargs)
		print(f"{f.__name__} took {time.time() - start_time} to complete")
		return res
	return return_func

def add_ungetch(f):
	def return_func(self, *args, **kwargs):
		res = f(self, *args, **kwargs)
		curses.ungetch(curses.KEY_F0)
		return res
	return return_func

def add_ungetch_and_cbreak(f):
	def return_func(self, *args, **kwargs):
		res = f(self, *args, **kwargs)
		curses.ungetch(curses.KEY_F0)
		curses.nocbreak()
		return res
	return return_func

def input_text(screen, text, state):
	screen.erase()
	start = 10
	for item in text:
		screen.addstr(start, 34, item)
		start += 1
	screen.addstr(18,34, "Enter message:")
	screen.addstr(21,34, "-----------------------------")
	screen.addstr(22,34,"[Enter] to send.")
	window = curses.newwin(1,30,20,35)
	screen.refresh()

	tbox = Textbox(window)

	tbox.edit()

	text = tbox.gather()

	return text[:-1]

def yes_no(screen, state, text):
	screen.erase()
	k = -1
	yes_selected = True
	
	while k != ord(" "):
		start = 10
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

			screen.attron(curses.color_pair(5))
			screen.addstr(18,34, "Ok")
			screen.attroff(curses.color_pair(5))
			
			start += 1
		if yes_selected:
			screen.attron(curses.color_pair(5))
			screen.addstr(18,34, "Yes")
			screen.attroff(curses.color_pair(5))
			screen.addstr(18, 40, "No")
		else:
			screen.addstr(18,34, "Yes")
			screen.attron(curses.color_pair(5))
			screen.addstr(18, 40, "No")
			screen.attroff(curses.color_pair(5))

		k = screen.getch()

		if k == curses.KEY_LEFT:
			yes_selected = True
		elif k == curses.KEY_RIGHT:
			yes_selected = False
	
	curses.ungetch(curses.KEY_F0)
	return yes_selected


def two_options(screen, state, text, options):
	screen.erase()
	k = -1
	first_selected = True
	
	while k != ord(" "):
		start = 10
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
		if first_selected:
			screen.attron(curses.color_pair(5))
			screen.addstr(18,34, options[0])
			screen.attroff(curses.color_pair(5))
			screen.addstr(18, 45, options[1])
		else:
			screen.addstr(18,34, options[0])
			screen.attron(curses.color_pair(5))
			screen.addstr(18, 45, options[1])
			screen.attroff(curses.color_pair(5))

		k = screen.getch()

		if k == curses.KEY_LEFT:
			first_selected = True
		elif k == curses.KEY_RIGHT:
			first_selected = False
	
	curses.ungetch(curses.KEY_F0)
	return first_selected

def ring_select(state):
	"""
		For selecting which slot to equip ring

		:param state: State

		:return bool (True for right, False for left)
	"""
	screen = state.stdscr
	screen.erase()
	k = -1
	first_selected = True
	right_ring = state.player.equipment["ring_1"]
	left_ring = state.player.equipment["ring_2"]
	options = ["Left", "Right"]
	orange = curses.color_pair(136)

	start_x = 15
	
	while k != ord(" "):
		# Left
		screen.addstr(12, 37, "LEFT", curses.color_pair(135))
		screen.addstr(start_x - 1, 5, "Name: ")
		screen.addstr(start_x - 1, 5 + len("Name: "), left_ring.readable_name, orange)
		screen.addstr(start_x + 1, 5, "Attack: ")
		screen.addstr(start_x + 1, 5 + len("Attack: "), str(left_ring.attack), orange)
		screen.addstr(start_x + 2, 5, "Defence: ")
		screen.addstr(start_x + 2, 5 + len("Defence: "), str(left_ring.defence), orange)
		screen.addstr(start_x + 3, 5, "Description: ")
		screen.addstr(start_x + 3, 5 + len("Description: "), str(left_ring.description), orange)
		screen.addstr(start_x + 4, 5, "Effect: ")
		screen.addstr(start_x + 4, 5 + len("Effect: "), str(left_ring.effect_description), orange)

		# Right
		screen.addstr(12, 112, "RIGHT", curses.color_pair(135))
		screen.addstr(start_x - 1, 80, "Name: ")
		screen.addstr(start_x - 1, 80 + len("Name: "), right_ring.readable_name, orange)
		screen.addstr(start_x + 1, 80, "Attack: ")
		screen.addstr(start_x + 1, 80 + len("Attack: "), str(right_ring.attack), orange)
		screen.addstr(start_x + 2, 80, "Defence: ")
		screen.addstr(start_x + 2, 80 + len("Defence: "), str(right_ring.defence), orange)
		screen.addstr(start_x + 3, 80, "Description: ")
		screen.addstr(start_x + 3, 80 + len("Description: "), str(right_ring.description), orange)
		screen.addstr(start_x + 4, 80, "Effect: ")
		screen.addstr(start_x + 4, 80 + len("Effect: "), str(right_ring.effect_description), orange)

		#Info text
		screen.addstr(44, 65, "[Space]: Select", orange)
		screen.addstr(45, 65, "[Q]: Back", orange)

		




		if first_selected:
			screen.attron(curses.color_pair(5))
			screen.addstr(35, 65, options[0])
			screen.attroff(curses.color_pair(5))
			screen.addstr(35, 75, options[1])
		else:
			screen.addstr(35, 65, options[0])
			screen.attron(curses.color_pair(5))
			screen.addstr(35, 75, options[1])
			screen.attroff(curses.color_pair(5))

		k = screen.getch()

		if k == curses.KEY_LEFT:
			first_selected = True
		elif k == curses.KEY_RIGHT:
			first_selected = False
		elif k == ord("q"):
			return "no ring selected"
	
	curses.ungetch(curses.KEY_F0)
	return first_selected


def color_first(screen, x, y, first, second, color):
	screen.addstr(x, y, first, color)
	screen.addstr(x, y + len(first), second)

def color_second(screen, x, y, first, second, color):
	screen.addstr(x, y, first)
	screen.addstr(x, y + len(first), second, color)

def color_both(screen, x, y, first, second, color_first, color_second):
	screen.addstr(x, y, first, color_first)
	screen.addstr(x, y + len(first), second, color_second)

#! Todo rework popup #!
def popup(screen, state, text):
	screen.erase()
	height, width = screen.getmaxyx()
	k = -1
	
	while k != ord(" ") and k != ord("q"):
		start = 10
		for item in text:
			y_offset = int((width - len(item)) / 2)
			if "[" in item:
				before, keyword, after = item.split("[")[0], item.split("[")[1].split("]")[0], item.split("]")[1]
				screen.addstr(start, y_offset, before)
				screen.attron(curses.color_pair(136))
				screen.addstr(start, y_offset + len(before), keyword)
				screen.attroff(curses.color_pair(136))
				screen.addstr(start, y_offset + len(before) + len(keyword), after)
			else:
				screen.addstr(start, y_offset, item)

			screen.attron(curses.color_pair(5))
			screen.addstr(30,int(width/ 2) - 2, "Ok")
			screen.attroff(curses.color_pair(5))
			
			start += 1

		k = screen.getch()
		if k == 163:
			state.log_info("I HAPPENED")
			return
		state.log_info(k)
	curses.ungetch(curses.KEY_F0)

def info_screen(state):
	screen = state.stdscr
	screen.erase()
	height, width = screen.getmaxyx()
	k = -1
	y_offset = 10
	
	while k != ord(" ") and k != ord("q"):
		start = 10

		screen.addstr(5,y_offset + 15,"E",curses.color_pair(197))
		screen.addstr(5,y_offset + 17, "- This is an NPC, press SPACE to interact and talk with them.")
		screen.addstr(7,y_offset + 15, "%", curses.color_pair(142))
		screen.addstr(7,y_offset + 17, "- This is a usable object, press SPACE to interact with it")
		screen.addstr(8,y_offset + 23, "* For example Chests, levers, Bushes etc.")
		screen.addstr(10,y_offset + 15, "%", curses.color_pair(209))
		screen.addstr(10,y_offset + 17, "- This is a door, walk into them to get inside (our otside)")

		screen.addstr(14,y_offset + 15, "I - Open the Inventory")
		screen.addstr(15,y_offset + 15, "E - Open your Equipment menu")
		screen.addstr(16,y_offset + 15, "P - Open your spellbook")
		screen.addstr(17,y_offset + 11, "SPACE - Interact with objects and NPCs")
		screen.addstr(18,y_offset + 11, "[1-6] - Assignable hotkeys")

		screen.attron(curses.color_pair(5))
		screen.addstr(30,int(width/ 2) - 2, "Ok")
		screen.attroff(curses.color_pair(5))

		k = screen.getch()
	curses.ungetch(curses.KEY_F0)

def pick_seed(state):
	screen = state.stdscr
	seeds = [x for x in state.player.inventory if x.subtype == "seed"]
	selected_item = 0
	k = -1
	splice_start = 0
	splice_end = 10

	effect = {
		"Ariam Seed": "Heals you for the damage done (Nature damage)",
		"Dever Seed": "Instead of exploding, it rots the target from the inside over time (Occult damage)",
		"Barbura Seed": "Ruptures immediately for less damage (Nature Damage)",
		"Firebloom Seed": "Causes burn after rupture (Fire damage)"
	}

	real_seeds = {}

	for item in seeds:
		if item.readable_name not in real_seeds.keys():
			real_seeds[item.readable_name] = 1
		else:
			real_seeds[item.readable_name] += 1

	while k != ord("q"):
		screen.erase()
		x_pos = 5
		pos_counter = 0
		for seed, counter in real_seeds.items():
			if pos_counter == selected_item:
				screen.addstr(x_pos, 5, f"{seed}: {counter}		-		{effect[seed]}", curses.color_pair(136))
				currently_selected = seed
			else:
				screen.addstr(x_pos, 5, f"{seed}: {counter}		-		{effect[seed]}")
			x_pos += 1
			pos_counter += 1
		screen.addstr(25,25, f"pos = {selected_item}")

		k = screen.getch()
		if k == ord(" "):
			#TODO Also remove seed from invent here
			return currently_selected
		elif k == curses.KEY_UP:
			selected_item -= 1
			if selected_item < 0:
				selected_item = 0
		elif k == curses.KEY_DOWN:
			selected_item += 1
			if selected_item > len(real_seeds.keys()) - 1:
				selected_item = len(real_seeds.keys()) - 1

def select_charm(state):
	screen = state.stdscr
	selected_item = 0
	k = -1
	splice_start = 0
	splice_end = 10

	effect = {
		"Desert Salt": "Saltspikes grow on your skin, reflecting damage",
		"Deverberry Skin": "Increases your strength GREATLY, but not without side-effects."
	}
	charms = [x for x in state.player.inventory if x.readable_name in effect.keys()]
	if not len(charms):
		return False

	real_charms = {}

	for item in charms:
		if item.readable_name not in real_charms.keys():
			real_charms[item.readable_name] = 1
		else:
			real_charms[item.readable_name] += 1

	while k != ord("q"):
		screen.erase()
		x_pos = 5
		pos_counter = 0
		for seed, counter in real_charms.items():
			if pos_counter == selected_item:
				screen.addstr(x_pos, 5, f"{seed}: {counter}		-		{effect[seed]}", curses.color_pair(136))
				currently_selected = seed
			else:
				screen.addstr(x_pos, 5, f"{seed}: {counter}		-		{effect[seed]}")
			x_pos += 1
			pos_counter += 1
		screen.addstr(25,25, f"pos = {selected_item}")

		k = screen.getch()
		if k == ord(" "):
			#TODO Also remove seed from invent here
			return currently_selected
		elif k == curses.KEY_UP:
			selected_item -= 1
			if selected_item < 0:
				selected_item = 0
		elif k == curses.KEY_DOWN:
			selected_item += 1
			if selected_item > len(real_charms.keys()) - 1:
				selected_item = len(real_charms.keys()) - 1

def get_item(item):
	for var in dir(items):
		if var.startswith("__"):
			continue
		if var == "Item":
			continue
		if var == "Sets":
			continue
		if var == item:
			return getattr(items, var)

def get_recipe(recipe):
	for var in dir(recipes):
		if var.startswith("__"):
			continue
		if var == "Recipe":
			continue
		if var == recipe:
			return getattr(recipes, var)

def get_spell(spell):
	for var in dir(abilities):
		if var.startswith("__"):
			continue
		if var == "Ability":
			continue
		if var == spell:
			return getattr(abilities, var)

def get_status_effects(effect):
	for var in dir(abilities):
		if var.startswith("__"):
			continue
		if var == "Ability":
			continue
		if var == effect:
			return getattr(abilities, var)

def get_state(state):
	for var in dir(states):
		if var == state:
			return getattr(states, var)


if __name__ == "__main__":
	pass
