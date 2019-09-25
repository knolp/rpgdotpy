import time
import helper
import curses
from curses.textpad import Textbox, rectangle

color_dict = {
	"head" : 1,
	"neck" : 2,
	"chest" : 3,
	"legs" : 4,
	"right_hand" : 5,
	"left_hand" : 6,
	"boots" : 7,
	"ring_1" : 8,
	"ring_2" : 8,
	False : 9
}

def input_text(name, vocation, screen, text, state):
	screen.clear()
	start = 10
	screen.addstr(5, 34, name)
	screen.addstr(6, 34, vocation)
	for item in text:
		screen.addstr(start, 34, item)
		start += 1
	screen.addstr(18,34, "Enter message:")
	screen.addstr(21,34, "-----------------------------")
	screen.addstr(22,34,"[Enter] to send. 'bye' or 'exit' to quit.")
	window = curses.newwin(1,30,20,35)
	screen.refresh()

	tbox = Textbox(window)

	tbox.edit()

	text = tbox.gather()

	return text.strip(" ")


def open_chest(screen, state, name, items):
	k = -1
	start = 10
	offset = 15

	player = state.player

	loot_list = [helper.get_item(item)() for item in items]

	selected_item = 0
	height, width = screen.getmaxyx()
	taken = []

	while k != ord("q"):
		screen.clear()

		start = 10
		loot_text = "Inside the {} you find:".format(name)
		screen.addstr(8, int((width / 2) - (len(loot_text) / 2)), loot_text)

		if loot_list:
			for i in range(len(loot_list)):
				if selected_item == i:
					screen.attron(curses.color_pair(5))
				screen.addstr(start, offset, loot_list[i].readable_name)
				if selected_item == i:
					screen.attroff(curses.color_pair(5))
				start += 1
		else:
			screen.addstr(start, offset, "No loot")

		if k == curses.KEY_DOWN:
			if len(loot_list) != 0:
				selected_item += 1
				if selected_item >= len(loot_list) - 1:
					selected_item = len(loot_list) - 1

		if k == curses.KEY_UP:
			if len(loot_list) != 0:
				selected_item -= 1
				if selected_item <= 0:
					selected_item = 0

		if k == ord(" "):
			if len(loot_list) != 0:
				taken.append(loot_list[selected_item])
				player.inventory.append(loot_list.pop(selected_item))
			curses.ungetch(curses.KEY_F0)

		k = screen.getch()
	curses.ungetch(curses.KEY_F0)
	if taken:
		return taken
	else:
		return []

def view_inventory(screen, state):
	k = -1
	selected_item = 0




	if len(state.player.inventory) == 0:
		helper.popup(screen, state, ["Inventory Empty"])
		return

	while k != ord("q"):
		screen.clear()
		start = 10
		pos = 5
		counter = 0

		info_start = 5
		info_pos = 100

		info_list = ["Head", "Neck", "Chest", "Legs", "Right Hand", "Left Hand", "Boots", "Ring", "other"]

		for idx, item in enumerate(info_list):
			screen.attron(curses.color_pair(idx + 1))
			screen.addstr(info_start + idx, info_pos, item)
			screen.attroff(curses.color_pair(idx + 1))

		

		for item in state.player.inventory:
			if counter != selected_item:
				screen.attron(curses.color_pair(color_dict[item.equippable]))
				screen.addstr(start, pos, item.readable_name[0:2])
				screen.attroff(curses.color_pair(color_dict[item.equippable]))
			else:
				#screen.attron(curses.color_pair(5))
				screen.addstr(start, pos, item.readable_name[0:2], curses.A_UNDERLINE)
				#screen.attroff(curses.color_pair(5))
			pos += 3
			if pos == 35:
				pos = 5
				start += 1
			counter += 1
		counter = 0
		screen.refresh()

		screen.addstr(30,0,"---------------------------------------------------------")
		screen.attron(curses.color_pair(color_dict[state.player.inventory[selected_item].equippable]))
		screen.addstr(31,0,"Name: {}".format(state.player.inventory[selected_item].readable_name))
		screen.attroff(curses.color_pair(color_dict[state.player.inventory[selected_item].equippable]))
		screen.addstr(32,0,"Description: {}".format(state.player.inventory[selected_item].description))
		if state.player.inventory[selected_item].equippable != False:
			screen.addstr(34, 0, "Stats:")
			screen.addstr(35, 0, "Attack: {}  Defence: {}".format(state.player.inventory[selected_item].attack, state.player.inventory[selected_item].defence))

		k = screen.getch()

		if k == curses.KEY_RIGHT:
			selected_item += 1
			if selected_item >= len(state.player.inventory):
				selected_item = len(state.player.inventory) - 1
		elif k == curses.KEY_LEFT:
			selected_item -= 1
			if selected_item < 0:
				selected_item = 0
		elif k == curses.KEY_DOWN:
			selected_item += 30
			if selected_item >= len(state.player.inventory):
				selected_item = len(state.player.inventory) - 1
		elif k == curses.KEY_UP:
			selected_item -= 30
			if selected_item < 0:
				selected_item = 0

def view_inventory2(screen, state):
	invent = state.player.inventory
	k = -1

	selected_tab = 0
	tabs = ["Weapons", "Armors", "Key items", "Consumables"]
	inv_type = ["weapon", "armor", "key", "consumable"]


	selected_item = [0,0]

	## TEMP SETTINGS FOR FIRST TIME
	max_matrix_rows = 11
	inv_matrix = [[False for i in range(10)] for i in range(10)]

	while k != ord("q"):
		screen.clear()
		#print tabs
		for i in range(len(tabs)):
			start_offset = i * 10
			if i == selected_tab:
				screen.attron(curses.color_pair(145))
				screen.addstr(0, start_offset, tabs[i])
				screen.attroff(curses.color_pair(145))
			else:
				screen.addstr(0, start_offset, tabs[i])

		show_inv = [x for x in invent if x.type == inv_type[selected_tab]]
		if len(show_inv) != 0:

			max_matrix_rows = len(show_inv) // 10 + 1
			inv_matrix = [[False for i in range(10)] for i in range(max_matrix_rows)]
			for i in range(len(inv_matrix)):
				for j in range(len(inv_matrix[0])):
					try:
						inv_matrix[i][j] = show_inv.pop()
					except IndexError:
						break
			col_counter = 4
			for i in range(len(inv_matrix)):
				for j in range(len(inv_matrix[0])):
					if inv_matrix[i][j] != False:
						if j == selected_item[1] and i == selected_item[0]:
							screen.attron(curses.color_pair(145))
						for idx, item in enumerate([curses.ACS_ULCORNER, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_URCORNER]):
							screen.addch(col_counter, j * 6 + idx, item)
						screen.addch(col_counter + 1, j * 6, curses.ACS_VLINE)
						screen.addstr(col_counter + 1, j * 6 + 1, inv_matrix[i][j].readable_name[:3])
						screen.addch(col_counter + 1, j * 6 + 4, curses.ACS_VLINE)

						for idx, item in enumerate([curses.ACS_LLCORNER, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_LRCORNER]):
							screen.addch(col_counter + 2, j * 6 + idx, item)
						if j == selected_item[1] and i == selected_item[0]:
							screen.attroff(curses.color_pair(145))
				col_counter += 4


			row_info_start = 70
			col_info_start = 20
			current = inv_matrix[selected_item[0]][selected_item[1]]

			#Draw Art
			art_start = (20 - len(current.art)) // 2
			for item in current.art:
				screen.addstr(art_start, row_info_start, item)
				art_start += 1

			#print item info

			screen.addstr(col_info_start,row_info_start,f"Name: {current.readable_name}")
			screen.addstr(col_info_start + 1, row_info_start, f"Description: {current.description}")
			if current.equippable:
				screen.addstr(col_info_start + 2, row_info_start, f"Attack: {current.attack}")
				screen.addstr(col_info_start + 3, row_info_start, f"Defence: {current.defence}")
		else:
			screen.addstr(4,0,"No items here")

		k = screen.getch()
		#handle keys
			#tab = changes tab + 1 (repeat)
			#arrow-keys = look items

		if k == 9:
			selected_item = [0,0]
			selected_tab += 1
			if selected_tab >= len(tabs):
				selected_tab = 0
		
		elif k == curses.KEY_DOWN:
			selected_item[0] += 1
			if selected_item[0] >= max_matrix_rows - 1:
				selected_item[0] = max_matrix_rows - 1
				if inv_matrix[selected_item[0]][selected_item[1]] == False:
					selected_item[1] = 9
				while inv_matrix[selected_item[0]][selected_item[1]] == False:
					selected_item[1] -= 1


		elif k == curses.KEY_UP:
			selected_item[0] -= 1
			if selected_item[0] < 0:
				selected_item[0] = 0

		elif k == curses.KEY_RIGHT:
			selected_item[1] += 1
			if selected_item[1] >= 10:
				selected_item[1] = 9
			if inv_matrix[selected_item[0]][selected_item[1]] == False:
				selected_item[1] -= 1

		elif k == curses.KEY_LEFT:
			selected_item[1] -= 1
			if selected_item[1] < 0:
				selected_item[1] = 0

	
def select_new_item(slot, inventory, screen, old_item):

	screen.clear()
	k = -1
	selected_item = 0

	slot_list = []
	eq_inventory = [x for x in inventory if x.equippable == slot]

	if len(eq_inventory) == 0:
		return False

	start = 10

	while k != ord("q"):
		screen.clear()
		start = 10
		pos = 5
		counter = 0

		for item in eq_inventory:
			if counter != selected_item:
				screen.addch(start, pos, item.readable_name[0])
			else:
				screen.attron(curses.color_pair(5))
				screen.addch(start, pos, item.readable_name[0])
				screen.attroff(curses.color_pair(5))
			pos += 1
			if pos == 35:
				pos = 5
				start += 1
			counter += 1
		counter = 0
		screen.refresh()

		screen.addstr(30,0,"---------------------------------------------------------")
		screen.addstr(31,0,"Name: {}".format(eq_inventory[selected_item].readable_name))
		screen.addstr(32,0,"Description: {}".format(eq_inventory[selected_item].description))
		if eq_inventory[selected_item].equippable != False:
			screen.addstr(34, 0, "Stats:")
			screen.addstr(35, 0, "Attack: {}  Defence: {}".format(eq_inventory[selected_item].attack, eq_inventory[selected_item].defence))

		if old_item != False:
			screen.addstr(30, 65, "Currently Equipped:")
			screen.addstr(31, 65, "Name: {}".format(old_item.readable_name))
			screen.addstr(32, 65, "Description: {}".format(old_item.description))
			screen.addstr(34, 65, "Stats:")
			screen.addstr(35, 65, "Attack: {}  Defence: {}".format(old_item.attack, old_item.defence))


		k = screen.getch()

		if k == ord(" "):
			inventory.remove(eq_inventory[selected_item])
			return eq_inventory[selected_item]

		if k == curses.KEY_RIGHT:
			selected_item += 1
			if selected_item >= len(eq_inventory):
				selected_item = len(eq_inventory) - 1
		elif k == curses.KEY_LEFT:
			selected_item -= 1
			if selected_item < 0:
				selected_item = 0
		elif k == curses.KEY_DOWN:
			selected_item += 30
			if selected_item >= len(eq_inventory):
				selected_item = len(eq_inventory) - 1
		elif k == curses.KEY_UP:
			selected_item -= 30
			if selected_item < 0:
				selected_item = 0
	return "pressed_q"


# EQUIPMENT VIEW

def view_equipment(screen, state):
	screen.clear()

	k = -1
	select_loop = [
		"head",
		"neck",
		"left_hand",
		"chest",
		"right_hand",
		"legs",
		"ring_1",
		"boots",
		"ring_2"
	]
	selected_item = 3

	translate = {
		"head" : "Head",
		"chest" : "Chest",
		"legs" : "Legs",
		"boots" : "Boots",
		"ring_1" : "Ring 1",
		"ring_2" : "Ring 2",
		"neck" : "Neck",
		"right_hand" : "Right Hand",
		"left_hand" : "Left Hand",
	}

	offset = {
		"head" : (2,45),
		"chest" : (12,45),
		"legs" : (17, 45),
		"boots" : (22,45),
		"left_hand" : (12, 25),
		"right_hand" : (12, 65),
		"ring_1" : (22, 25),
		"ring_2" : (22, 65),
		"neck" : (7,45)
	}

	border_color = 1


	while k != ord("q"):
		screen.clear()
		#border_color += 1

		#INFO STRINGS
		info_start = 5
		info_pos = 100

		#lets make some boxes

		screen.attron(curses.color_pair(border_color))

		#head
		screen.addstr(0, 43, "#" * 20)
		for i in range(5):
			screen.addstr(i, 43, "#")
			screen.addstr(i, 62, "#")

		#neck
		screen.addstr(5, 43, "#" * 20)
		for i in range(5,10):
			screen.addstr(i, 43, "#")
			screen.addstr(i, 62, "#")

		#chest
		screen.addstr(10, 43, "#" * 20)
		for i in range(10, 15):
			screen.addstr(i, 43, "#")
			screen.addstr(i, 62, "#")

		#left_hand
		screen.addstr(10,23, "#" * 20)
		for i in range(10,15):
			screen.addstr(i, 23, "#")
		screen.addstr(15,23, "#" * 20)

		#right_hand
		screen.addstr(10,63, "#" * 20)
		for i in range(10,16):
			screen.addstr(i, 83, "#")
		screen.addstr(15,63, "#" * 20)

		

		#legs
		screen.addstr(15, 43, "#" * 20)
		for i in range(15,20):
			screen.addstr(i, 43, "#")
			screen.addstr(i, 62, "#")

		#boots
		screen.addstr(20, 43, "#" * 20)
		for i in range(20,25):
			screen.addstr(i, 43, "#")
			screen.addstr(i, 62, "#")

		#ring_1
		screen.addstr(20,23, "#" * 20)
		for i in range(20,25):
			screen.addstr(i, 23, "#")
		screen.addstr(25,23, "#" * 20)

		#ring_2
		screen.addstr(20,63, "#" * 20)
		for i in range(20,26):
			screen.addstr(i, 83, "#")
		screen.addstr(25,63, "#" * 20)

		#Bottom
		screen.addstr(25, 43, "#" * 20)

		screen.attroff(curses.color_pair(border_color))



		screen.addstr(info_start, info_pos, "Space: Swap")
		screen.addstr(info_start + 2, info_pos, "X: Remove")
		screen.addstr(info_start + 4, info_pos, "Q: Quit")

		start = 10
		pos = 5
		counter = 0

		for k,v in state.player.equipment.items():
			start, pos = offset[k]
			if k == select_loop[selected_item]:
				screen.attron(curses.color_pair(5))
			if v != False:
				screen.addstr(start, pos, "{}:".format(translate[k]))
				screen.addstr(start + 1, pos, v.readable_name)
			else:
				screen.addstr(start, pos, "{}:".format(translate[k]))
				screen.addstr(start + 1, pos, "Nothing")
			if k == select_loop[selected_item]:
				screen.attroff(curses.color_pair(5))
				
		screen.refresh()

		k = screen.getch()

		if k == ord("x"):
			slot = select_loop[selected_item]
			if state.player.equipment[slot] == False:
				k = -1
				continue
			state.player.inventory.append(state.player.equipment[slot])
			state.player.equipment[slot] = False

		if k == ord(" "):
			slot = select_loop[selected_item]
			old_item = state.player.equipment[slot]
			new_item = select_new_item(slot, state.player.inventory, screen, old_item)
			if new_item == False:
				k = -1
				helper.popup(screen, state, ["No equippable item for this slot."])
				continue

			if new_item == "pressed_q":
				k = -1
				continue

			if state.player.equipment[slot] != False:
				state.player.inventory.append(state.player.equipment[slot])
			state.player.equipment[slot] = new_item


		if k == curses.KEY_RIGHT:
			if selected_item == 2:
				selected_item = 3
			elif selected_item == 3:
				selected_item = 4
			elif selected_item == 6:
				selected_item = 7
			elif selected_item == 7:
				selected_item = 8

		elif k == curses.KEY_LEFT:
			if selected_item == 3:
				selected_item = 2
			elif selected_item == 4:
				selected_item = 3
			elif selected_item == 7:
				selected_item = 6
			elif selected_item == 8:
				selected_item = 7

		elif k == curses.KEY_DOWN:
			if selected_item == 0:
				selected_item = 1
			elif selected_item == 1:
				selected_item = 3
			elif selected_item == 2:
				selected_item = 6
			elif selected_item == 3:
				selected_item = 5
			elif selected_item == 4:
				selected_item = 8
			elif selected_item == 5:
				selected_item = 7

		elif k == curses.KEY_UP:
			if selected_item == 8:
				selected_item = 4
			elif selected_item == 7:
				selected_item = 5
			elif selected_item == 6:
				selected_item = 2
			elif selected_item == 5:
				selected_item = 3
			elif selected_item == 3:
				selected_item = 1
			elif selected_item == 1:
				selected_item = 0

def swap_spells(screen, state, old_spell_index):
	screen.clear()

	k = -1
	selected_item = 0

	height, width = screen.getmaxyx()

	start = int(height / 2)
	offset = int(width / 2)

	while k != ord("q"):
		screen.clear()

		if state.player.spells[old_spell_index] == False:
			explain_text = "Choose a spell to replace {}".format("[Empty Slot]")
		else:
			explain_text = "Choose a spell to replace {}".format(state.player.spells[old_spell_index].readable_name)

		screen.addstr(10, offset - int((len("Inactive Spells") / 2) + 30), "Inactive Spells")
		screen.addstr(11, offset - int((len(explain_text) / 2) + 30), explain_text)

		for i in range(len(state.player.spellbook)):
			if i == selected_item:
				screen.attron(curses.color_pair(5))
			
			screen.addstr(start + i, offset - int((len(state.player.spellbook[i].readable_name) / 2) + 30), state.player.spellbook[i].readable_name)

			if i == selected_item:
				screen.attroff(curses.color_pair(5))

		#DESCRIPTION

		if selected_item >= len(state.player.spellbook):
			screen.addstr(32,10,"Name: ")
			screen.addstr(33,10,"Description: ")
		else:
			screen.addstr(32,10, "Name: {}".format(state.player.spellbook[selected_item].readable_name))
			screen.addstr(33,10, "Description: {}".format(state.player.spellbook[selected_item].description))
		
		k = screen.getch()

		if k == ord(" "):
			state.player.spells[old_spell_index] = state.player.spellbook[selected_item]
			return True

		elif k == curses.KEY_DOWN:
			selected_item += 1
			if selected_item >= len(state.player.spellbook):
				selected_item = len(state.player.spellbook) - 1
		elif k == curses.KEY_UP:
			selected_item -= 1
			if selected_item < 0:
				selected_item = 0

def view_spellbook(screen, state):
	screen.clear()

	k = -1
	selected_item = 0

	height, width = screen.getmaxyx()

	start = int(height / 2)
	offset = int(width / 2)

	

	while k != ord("q"):
		screen.clear()

		explain_text = "You can have a maximum of 5 active spells equipped."

		screen.addstr(10, offset - int((len("Active Spells") / 2) + 30), "Active Spells")
		screen.addstr(11, offset - int((len(explain_text) / 2) + 30), explain_text)

		for i in range(0,5):
			if i == selected_item:
				screen.attron(curses.color_pair(5))
			
			if state.player.spells[i] == False:
				screen.addstr(start + i, offset - int((len("[Empty Slot]") / 2) + 30), "[Empty Slot]")
			else:
				screen.addstr(start + i, offset - int((len(state.player.spells[i].readable_name) / 2) + 30), state.player.spells[i].readable_name)

			if i == selected_item:
				screen.attroff(curses.color_pair(5))

		#DESCRIPTION

		if state.player.spells[selected_item] == False:
			screen.addstr(32,10,"Name: ")
			screen.addstr(33,10,"Description: ")
		else:
			screen.addstr(32,10, "Name: {}".format(state.player.spells[selected_item].readable_name))
			screen.addstr(33,10, "Description: {}".format(state.player.spells[selected_item].description))
		
		k = screen.getch()

		if k == ord(" "):
			swap_spells(screen, state, selected_item)

		elif k == curses.KEY_DOWN:
			selected_item += 1
			if selected_item >= 4:
				selected_item = 4
		elif k == curses.KEY_UP:
			selected_item -= 1
			if selected_item < 0:
				selected_item = 0
			



#ITEM STUFF


if __name__ == "__main__":
	print(select_new_item("boots", [helper.get_item("LeatherBoots")()]))