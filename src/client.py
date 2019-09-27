import sys,os,time, fileinput
import curses
import curses.textpad as textpad
import curses.ascii as asc
from pprint import pprint
import json
import math
import random
import time

import states
import player
import mapper
import npc
import helper
import actions
import inventory
import items
import battle
import monster
import pathfinding
import pathfinding2

class MenuObject():
	def __init__(self, x, y, title):
		self.x = x
		self.y = y
		self.title = title



class StateHandler():
	def __init__(self, game_box, command_box, stdscr):
		self.game_box = game_box
		self.command_box = command_box
		self.last_game_state = False
		self.last_command_state = False
		self.map_screen = False
		self.gamemap = False
		self.ingame_menu = False
		self.first_time = True
		self.stdscr = stdscr
		self.autowalk = False

		self.action = "None"

		self.player = False

		self.create_player = {}

		#self.game_state = states.Intro_temp(self.game_box, self.command_box)
		#self.command_state = states.main_menu_temp(self.game_box, self.command_box)
		self.game_state = states.Intro(self)
		self.command_state = states.main_menu(self)

		if self.command_state:
			self.command_state.commands[0].active = True


	def check_collision(self,next_tile):
		x,y = next_tile
		return self.gamemap.game_map.background2[x - 1][y - 1].walkable

	def check_npc_action(self):
		for obj in self.gamemap.game_map.objects:
			if self.player.x == obj.x and self.player.y == obj.y:
				obj.action(self.game_box, self)


	def load_player(self):
		with open("save.json", "r") as f:
			load_dict = json.load(f)

		self.player = player.Player(load_dict)
		for item in load_dict["inventory"]:
			#self.player.inventory.append(items.item_dict[item["name"]]())
			self.player.inventory.append(helper.get_item(item["name"])())

		for k,v in load_dict["equipment"].items():
			if v != False:
				#self.player.equipment[k] = items.item_dict[v["name"]]()
				self.player.equipment[k] = helper.get_item(v["name"])()

		temp_spell_list = []
		for index, item in enumerate(load_dict["spells"]):
			#print("Index: {}         Item: {}".format(index, item))
			if item != False:
				temp_spell_list.append(helper.get_spell(item["name"])())
			else:
				temp_spell_list.append(False)
		self.player.spells = temp_spell_list

		temp_spellbook_list = []
		for item in load_dict["spellbook"]:
			#print("                               " + item["name"])
			temp_spellbook_list.append(helper.get_spell(item["name"])())
		self.player.spellbook = temp_spellbook_list

	def save_player(self):
		params = {}

		for k,v in self.player.__dict__.items()	:
			params[k] = v
			if k == "location":
				params[k] = v.raw_name
			if k == "inventory":
				for i in range(len(params[k])):
					params[k][i] = params[k][i].__dict__
			
			if k == "equipment":
				for key,value in params[k].items():
					#params[k][i] = params[k][i].__dict__
					if params[k][key] != False:
						params[k][key] = value.__dict__

			if k == "spells":
				for i in range(len(params[k])):
					if params[k][i] != False:
						params[k][i] = params[k][i].__dict__
					else:
						params[k][i] = False

			if k == "spellbook":
				for i in range(len(params[k])):
					params[k][i] = params[k][i].__dict__

		with open("save.json", "w") as f:
			json.dump(params,f)

		self.load_player()

	def make_player(self):
		self.create_player["x"] = 13
		self.create_player["y"] = 13

		self.player = player.Player(self.create_player)

	def update_map(self):
		self.gamemap = self.player.location(self)

	def change_map_screen(self):
		self.map_screen = not self.map_screen

	def is_tab_enabled(self):
		if self.player != False:
			return True
		else:
			return False

	def check_tall_grass(self):
		if self.gamemap.game_map.background2[self.player.x - 1][self.player.y - 1].name == "Tall Grass":
			if random.randint(1,100) < 16:
				battle.Battle(self, random.choice(self.gamemap.random_monsters)(), "3").play()


def is_tab_enabled(state):
	if state.player != False:
		return True
	else:
		return False


def draw_commands(state, command_box):
	i = 0
	for item in state.commands:
		i += 2
		if item.text == "Back":
			command_box.attron(curses.color_pair(2))
			command_box.addstr(37,2,item.text)
			command_box.attroff(curses.color_pair(2))

		if item.active:
			command_box.attron(curses.color_pair(5))
			if item.text != "Back":
				command_box.addstr(i,2,item.text)
			else:
				command_box.addstr(37,2,item.text)
			command_box.attroff(curses.color_pair(5))
		else:
			if item.text != "Back":
				command_box.addstr(i,2,item.text)

def get_next(state, command_box):
	for item in state.commands:
		if item.active == True:
			item.active = False
			next_position = item.position + 1
			if next_position > len(state.commands):
				next_position = len(state.commands)
	for item in state.commands:
		if item.position == next_position:
			item.active = True

def get_prev(state, command_box):
	for item in state.commands:
		if item.active == True:
			item.active = False
			next_position = item.position - 1
			if next_position < 1:
				next_position = 1

	for item in state.commands:
		if item.position == next_position:
			item.active = True







def check_direction(state):
	if state.player.x == state.player.last_pos[0]:
		if state.player.y > state.player.last_pos[1]:
			return "right"
		else:
			return "left"
	else:
		if state.player.x > state.player.last_pos[0]:
			return "down"
		else:
			return "up"







def draw_menu(stdscr):

	k = 0
	cursor_x = 0
	cursor_y = 0
	name = ""

	curses.curs_set(0)
	curses.cbreak()
	curses.mousemask(curses.ALL_MOUSE_EVENTS)
	stdscr.keypad(1)

	game_box = stdscr.derwin(39,99,0,1)
	command_box = stdscr.derwin(39,48,0,101)

	last_mouse_x = 0
	last_mouse_y = 0

	direction = "right"

	path = []
	closed_path = []
	open_path = []

	state_handler = StateHandler(game_box, command_box, stdscr)

	curses.start_color()

	curses.use_default_colors()
	for i in range(0, curses.COLORS - 1):
		curses.init_pair(i + 1, i, i - 1)

	curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_RED)
	curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
	curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLUE)
	curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_GREEN)
	curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
	curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_YELLOW)
	curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_CYAN)

	#Color range 131 -> 147 reserved

	curses.init_pair(131, 232, 165)
	curses.init_pair(132, curses.COLOR_YELLOW, curses.COLOR_GREEN)
	curses.init_pair(133, curses.COLOR_RED, -1)
	curses.init_pair(134, curses.COLOR_GREEN, -1)
	curses.init_pair(135, curses.COLOR_CYAN, -1)
	curses.init_pair(136, curses.COLOR_YELLOW, -1)
	curses.init_pair(137, curses.COLOR_BLUE, - 1)
	curses.init_pair(138, 130, -1)
	curses.init_pair(139, 238 , 242) #Cobblestone
	curses.init_pair(140, 237, 242) #Fence
	curses.init_pair(141, 240, 40) #Grass Fence
	curses.init_pair(142, 136, 40) #Tree Bot
	curses.init_pair(143, 22, 40) #Tree Top
	curses.init_pair(144, 220, 94) #Beer
	curses.init_pair(145, 94, 52) #Wooden Chair
	curses.init_pair(146, 237, 52) #floor fence
	curses.init_pair(147, curses.COLOR_WHITE, -1)

	counter = 0

	while (k != ord('q')):
		

		stdscr.clear()

		counter += 1

		game_box.border()
		command_box.border()

		height, width = state_handler.game_box.getmaxyx()

		if state_handler.map_screen == True:
			
			if k == 9 and is_tab_enabled(state_handler):
				k = 1
				state_handler.change_map_screen()
				continue
			if state_handler.autowalk == False:
				if k in [curses.KEY_DOWN, curses.KEY_UP, curses.KEY_LEFT, curses.KEY_RIGHT, ord("w"), ord("a"), ord("s"), ord("d")]:
					state_handler.player.last_pos = state_handler.player.x, state_handler.player.y
					#state_handler.check_tall_grass()
					name = ""

				if k == curses.KEY_DOWN or k == ord("s"):
					if direction == "down":
						curses.flushinp()
					direction = "down"
					next_direction = state_handler.player.x + 1
					next_tile = next_direction, state_handler.player.y
					if state_handler.player.x < 37 and state_handler.check_collision(next_tile):
						state_handler.player.x = next_direction
					k = 1
				elif k == curses.KEY_UP or k == ord("w"):
					if direction == "up":
						curses.flushinp()
					direction = "up"
					next_direction = state_handler.player.x - 1
					next_tile = next_direction, state_handler.player.y
					if state_handler.player.x > 1 and state_handler.check_collision(next_tile):
						state_handler.player.x = next_direction
					k = 1
				elif k == curses.KEY_LEFT or k == ord("a"):
					if direction == "left":
						curses.flushinp()
					direction = "left"
					next_direction = state_handler.player.y - 1
					next_tile = state_handler.player.x, next_direction
					if state_handler.player.y > 1 and state_handler.check_collision(next_tile):
						state_handler.player.y = next_direction
					k = 1
				elif k == curses.KEY_RIGHT or k == ord("d"):
					if direction == "right":
						curses.flushinp()
					direction = "right"
					next_direction = state_handler.player.y + 1
					next_tile = state_handler.player.x, next_direction
					if state_handler.player.y < 96 and state_handler.check_collision(next_tile):
						state_handler.player.y = next_direction
					k = 1

				elif k == ord(" "):
					state_handler.check_npc_action()

			state_handler.gamemap.check_events()


			state_handler.gamemap.draw()
			draw_commands(state_handler.ingame_menu, state_handler.command_box)
			state_handler.player.draw(game_box)

			if last_mouse_x != 0:
				state_handler.game_box.addstr(last_mouse_y, last_mouse_x - 1, name)

		else:

			if k == 9 and is_tab_enabled(state_handler):
				k = 1
				state_handler.change_map_screen()
				state_handler.command_state = state_handler.gamemap.menu_commands(state_handler)
				state_handler.command_state.commands[0].active = True
				continue
			elif k == curses.KEY_DOWN:
				get_next(state_handler.command_state, command_box)
			elif k == curses.KEY_UP:
				get_prev(state_handler.command_state, command_box)
			elif k == curses.KEY_RIGHT:
				pass
			elif k == curses.KEY_LEFT:
				cursor_x = cursor_x - 1
			elif k == ord(" "):
				state_handler.game_state.execute()
				for item in state_handler.command_state.commands:
					if item.active:
						next_command_state = item.execute_command()
						if next_command_state == False:
							pass
						else:
							state_handler.command_state = next_command_state(state_handler)
							if hasattr(state_handler.command_state, "game"):
								state_handler.command_state.commands[0].active = True
							else:
								state_handler.command_state.commands[0].active = True
						next_game_state = item.execute_game()
						if next_game_state == False:
							pass
						elif hasattr(state_handler.command_state, "game"):
							state_handler.gamemap = state_handler.player.location(state_handler)
							state_handler.game_state = state_handler.gamemap.menu(state_handler)
							state_handler.ingame_menu = state_handler.gamemap.ingame_menu(state_handler)
						else:
							if state_handler.player != False:
								state_handler.gamemap = state_handler.player.location(state_handler)
								state_handler.ingame_menu = state_handler.gamemap.ingame_menu(state_handler)
								state_handler.game_state = state_handler.gamemap.menu(state_handler)
								curses.ungetch(curses.KEY_F0)
							else:
								state_handler.game_state = next_game_state(state_handler)



			state_handler.game_state.draw()
			draw_commands(state_handler.command_state, state_handler.command_box)

		cursor_x = max(0, cursor_x)
		cursor_x = min(width-1, cursor_x)

		cursor_y = max(0, cursor_y)
		cursor_y = min(height-1, cursor_y)

		if state_handler.player:
			cursor_y = state_handler.player.y
			cursor_x = state_handler.player.x


		

		#statusbarstr = "Mouse: x: {} , y: {} | Pos: {}, {} | {}x{} | Action: {}".format(last_mouse_x, last_mouse_y,cursor_x, cursor_y, width, height, state_handler.action)

		#stdscr.attron(curses.color_pair(3))
		#stdscr.addstr(height, 0, statusbarstr)
		#stdscr.attroff(curses.color_pair(3))

		k = stdscr.getch()
		#curses.flushinp()

		if k == curses.KEY_MOUSE:
			unused_1, last_mouse_x, last_mouse_y,unused_2,unused_3 = curses.getmouse()
			if last_mouse_x <= 97 and last_mouse_y <= 37 and state_handler.map_screen == True:
				for item in state_handler.gamemap.game_map.objects:
					if item.y == (last_mouse_x - 1) and item.x == last_mouse_y:
						name = item.name
						break
					else:
						name = state_handler.gamemap.game_map.background2[last_mouse_y - 1][last_mouse_x - 2].name
			else:
				last_mouse_y = 0
				last_mouse_x = 0
			k = 1

		if k == ord("e") and state_handler.player != False:
			inventory.view_equipment(state_handler.stdscr, state_handler)

		if k == ord("i") and state_handler.player != False:
			inventory.view_inventory(state_handler.stdscr, state_handler)

		if k == ord("p") and state_handler.player != False:
			inventory.view_spellbook(state_handler.stdscr, state_handler)

		if k == ord("c") and state_handler.player != False:
			battlemode = battle.Battle(state_handler, monster.Rat(), "3")
			battlemode.play()

		if k == ord("k") and state_handler.player != False:
			item_list = [items.ChainHelmet, items.LeatherBoots, items.StuddedLegs, items.RatFangNecklace, items.ChainMail]
			for i in range(150):
				state_handler.player.inventory.append(random.choice(item_list)())

		if k == ord("1"):
			if direction == "up":
				state_handler.player.x -= 4
			elif direction == "down":
				state_handler.player.x += 4
			elif direction == "left":
				state_handler.player.y -= 4
			elif direction == "right":
				state_handler.player.y += 4




def main():
	curses.wrapper(draw_menu)

if __name__ == "__main__":
	main()