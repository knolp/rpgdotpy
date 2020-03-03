import curses
import items
import abilities
import recipes
from curses.textpad import Textbox, rectangle


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
	screen.clear()
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
	screen.clear()
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
	screen.clear()
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
			screen.addstr(18, 40, options[1])
		else:
			screen.addstr(18,34, options[0])
			screen.attron(curses.color_pair(5))
			screen.addstr(18, 40, options[1])
			screen.attroff(curses.color_pair(5))

		k = screen.getch()

		if k == curses.KEY_LEFT:
			first_selected = True
		elif k == curses.KEY_RIGHT:
			first_selected = False
	
	curses.ungetch(curses.KEY_F0)
	return first_selected


def popup(screen, state, text):
	screen.clear()
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
	curses.ungetch(curses.KEY_F0)

def get_item(item):
	for var in dir(items):
		if var.startswith("__"):
			continue
		if var == "Item":
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
