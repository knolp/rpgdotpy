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


def popup(screen, state, text):
	screen.clear()
	k = -1
	
	while k != ord(" ") and k != ord("q"):
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
