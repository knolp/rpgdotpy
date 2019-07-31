'''import sys,os,time
import curses
import curses.textpad as textpad
import curses.ascii as asc
from pprint import pprint


class GameLoop():
	def __init__(self, state_handler):
		self.state_handler = state_handler
		self.player = state_handler.player'''

import sys,os,time
import curses
import curses.textpad as textpad
import curses.ascii as asc
from pprint import pprint

import states
import player

class MenuObject():
	def __init__(self, x, y, title):
		self.x = x
		self.y = y
		self.title = title


class StateHandler():
	def __init__(self, game_box, command_box):
		self.game_box = game_box
		self.command_box = command_box
		self.game_state = states.Intro_temp(self.game_box, self.command_box)
		self.command_state = states.main_menu_temp(self.game_box, self.command_box)
		self.command_state.commands[0].active = True
		self.last_game_state = False
		self.last_command_state = False

		self.player = False

		self.create_player = {}


	def load_player(self):
		self.player = player.Player("Kerberos")

	def create_player(self, name):
		self.player = player.Player(name)


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

def draw_menu(stdscr):

	k = 0
	cursor_x = 0
	cursor_y = 0

	# Clear and refresh the screen for a blank canvas
	stdscr.clear()
	stdscr.refresh()
	stdscr.nodelay(1)
	curses.curs_set(0)

	game_box = stdscr.derwin(39,99,0,1)
	command_box = stdscr.derwin(39,48,0,101)

	#command_state = states.main_menu(game_box,command_box)
	#game_state = states.Intro(game_box, command_state)
	#command_state.commands[0].active = True

	state_handler = StateHandler(game_box, command_box)

	# Start colors in curses
	curses.start_color()
	curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_RED)
	curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
	curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLUE)
	curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_GREEN)

	# Loop where k is the last character pressed
	while (k != ord('q')):

		stdscr.clear()

		game_box.border()
		command_box.border()

		height, width = state_handler.game_box.getmaxyx()


		if k == curses.KEY_DOWN:
			get_next(state_handler.command_state, command_box)
		elif k == curses.KEY_UP:
			get_prev(state_handler.command_state, command_box)
		elif k == curses.KEY_RIGHT:
			cursor_x = cursor_x + 1
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
						state_handler.command_state.commands[0].active = True

					next_game_state = item.execute_game()
					if next_game_state == False:
						pass
					else:
						state_handler.game_state = next_game_state(state_handler)


		state_handler.game_state.draw()
		draw_commands(state_handler.command_state, state_handler.command_box)

		cursor_x = max(0, cursor_x)
		cursor_x = min(width-1, cursor_x)

		cursor_y = max(0, cursor_y)
		cursor_y = min(height-1, cursor_y)


		statusbarstr = "Press 'q' to exit | Map Editor | Pos: {}, {} | {}x{}".format(cursor_x, cursor_y, width, height)


		# Render status bar
		stdscr.attron(curses.color_pair(3))
		stdscr.addstr(height, 0, statusbarstr)
		stdscr.attroff(curses.color_pair(3))


		state_handler.game_box.move(cursor_y, cursor_x)
		# Refresh the screen
		#stdscr.refresh()

		# Wait for next input
		k = stdscr.getch()

def main():
	curses.wrapper(draw_menu)

if __name__ == "__main__":
	main()