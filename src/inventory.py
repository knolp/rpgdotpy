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

		k = screen.getch()
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
	curses.ungetch(curses.KEY_F0)
	if taken:
		return taken
	else:
		return []

def view_inventory(screen, state):
	invent = state.player.inventory
	k = -1

	selected_tab = 0
	tabs = ["Weapons |", "Armors |", "Key items |", "Consumables |", "Crafting"]
	inv_type = ["weapon", "armor", "key", "consumable", "crafting"]
	rarity_colors = {
		"common" : 147,
		"rare" : 134,
		"epic" : 133,
		"unique" : 135,
		"legendary" : 136
	}


	selected_item = [0,0]

	## TEMP SETTINGS FOR FIRST TIME
	max_matrix_rows = 11
	inv_matrix = [[False for i in range(10)] for i in range(10)]
	inv_scroll = 0

	while k != ord("q"):
		screen.clear()
		#print tabs
		for i in range(len(tabs)):
			start_offset = i * 12
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
			counter = 0
			for i in range(inv_scroll, len(inv_matrix)):
				for j in range(len(inv_matrix[0])):
					if inv_matrix[i][j] != False:
						if j == selected_item[1] and i == selected_item[0]:
							screen.attron(curses.color_pair(145))
						else:
							screen.attron(curses.color_pair(rarity_colors[inv_matrix[i][j].rarity]))
						for idx, item in enumerate([curses.ACS_ULCORNER, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_URCORNER]):
							screen.addch(col_counter, j * 6 + idx, item)
						screen.addch(col_counter + 1, j * 6, curses.ACS_VLINE)
						screen.addstr(col_counter + 1, j * 6 + 1, inv_matrix[i][j].readable_name[:3])
						screen.addch(col_counter + 1, j * 6 + 4, curses.ACS_VLINE)

						for idx, item in enumerate([curses.ACS_LLCORNER, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_LRCORNER]):
							screen.addch(col_counter + 2, j * 6 + idx, item)
						if j == selected_item[1] and i == selected_item[0]:
							screen.attroff(curses.color_pair(145))
						else:
							screen.attroff(curses.color_pair(rarity_colors[inv_matrix[i][j].rarity]))
				col_counter += 4
				counter += 1
				if counter == 9:
					break

			if inv_scroll < max_matrix_rows - 9:
				screen.addch(39, 29, curses.ACS_DARROW)
			if inv_scroll > 0:
				screen.addch(3, 29, curses.ACS_UARROW)

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
			if current.effect_description:
				screen.addstr(col_info_start + 4, row_info_start, f"Effect: {current.effect_description}")
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
					selected_item[0] -= 1
			if selected_item[0] > inv_scroll + 8:
				inv_scroll += 1
				if inv_scroll > max_matrix_rows - 8:
					inv_scroll -= 1
					selected_item[0] -= 1


		elif k == curses.KEY_UP:
			selected_item[0] -= 1
			if selected_item[0] < 0:
				selected_item[0] = 0
			if selected_item[0] < inv_scroll:
				inv_scroll -= 1
				#selected_item[0] += 1

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



def trade(npc, screen, state):
	screen.clear()
	k = -1
	selected_item = [0,0]
	selected_item_npc = [0,0]
	return_to_speak = False

	invent = state.player.inventory
	npc_invent = npc.inventory

	player_view = True

	max_matrix_rows = 11
	inv_matrix = [[False for i in range(10)] for i in range(10)]
	inv_scroll = 0
	max_matrix_rows_npc = 11
	inv_matrix_npc = [[False for i in range(10)] for i in range(10)]
	inv_scroll_npc = 0

	selected_tab = 0
	selected_tab_npc = 0
	tabs = ["Weapons", "Armors", "Key items", "Consumables", "Crafting"]
	npc_tabs = ["Weapons", "Armors", "Key items", "Consumables", "Crafting"]
	inv_type = ["weapon", "armor", "key", "consumable", "crafting"]
	rarity_colors = {
		"common" : 147,
		"rare" : 134,
		"epic" : 133,
		"unique" : 135,
		"legendary" : 136
	}

	while k != ord("q"):
		screen.clear()
		# Make borders
		#screen.attron(curses.color_pair(133))
		if player_view:
			screen.addch(0,7, curses.ACS_ULCORNER)
			screen.addch(0,67, curses.ACS_URCORNER)
			screen.addch(27,7, curses.ACS_LLCORNER)
			screen.addch(27,67, curses.ACS_LRCORNER)
			screen.addch(0,8,curses.ACS_HLINE)
			screen.addch(0,66,curses.ACS_HLINE)
			screen.addch(27,66,curses.ACS_HLINE)
			screen.addch(27,8,curses.ACS_HLINE)
			screen.addch(1,7,curses.ACS_VLINE)
			screen.addch(1,67,curses.ACS_VLINE)
			screen.addch(26,67,curses.ACS_VLINE)
			screen.addch(26,7,curses.ACS_VLINE)
		else:
			screen.addch(0,79, curses.ACS_ULCORNER)
			screen.addch(0,142, curses.ACS_URCORNER)
			screen.addch(27,79, curses.ACS_LLCORNER)
			screen.addch(27,142, curses.ACS_LRCORNER)
			screen.addch(0,80,curses.ACS_HLINE)
			screen.addch(0,141,curses.ACS_HLINE)
			screen.addch(27,80,curses.ACS_HLINE)
			screen.addch(27,141,curses.ACS_HLINE)
			screen.addch(1,79,curses.ACS_VLINE)
			screen.addch(1,142,curses.ACS_VLINE)
			screen.addch(26,79,curses.ACS_VLINE)
			screen.addch(26,142,curses.ACS_VLINE)
		#screen.attroff(curses.color_pair(133))

		screen.addstr(32, 1, "Current gold:")
		screen.addstr(33, 1, str(state.player.gold))

		screen.addstr(32, 118, "Q: Quit")
		screen.addstr(33, 118, "B: Back to chat")
		screen.addstr(34, 118, "Tab: Change tab")
		screen.addstr(35, 118, "C: Change view")
		screen.addstr(36, 118, "Space: Buy / Sell")


		# show player inventory
		start_offset_tabs = 8
		for i in range(len(tabs)):
			if i == selected_tab:
				screen.attron(curses.color_pair(145))
				screen.addstr(1, start_offset_tabs, tabs[i])
				screen.attroff(curses.color_pair(145))
			else:
				screen.addstr(1, start_offset_tabs, tabs[i])
			start_offset_tabs += len(tabs[i]) + 1

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
			counter = 0
			offset_items_player = 8
			for i in range(inv_scroll, len(inv_matrix)):
				for j in range(len(inv_matrix[0])):
					if inv_matrix[i][j] != False:
						if j == selected_item[1] and i == selected_item[0]:
							screen.attron(curses.color_pair(145))
						else:
							screen.attron(curses.color_pair(rarity_colors[inv_matrix[i][j].rarity]))
						for idx, item in enumerate([curses.ACS_ULCORNER, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_URCORNER]):
							screen.addch(col_counter, (j * 6 + idx) + offset_items_player, item)
						screen.addch(col_counter + 1, (j * 6) + offset_items_player, curses.ACS_VLINE)
						screen.addstr(col_counter + 1, (j * 6 + 1) + offset_items_player, inv_matrix[i][j].readable_name[:3])
						screen.addch(col_counter + 1, (j * 6 + 4) + offset_items_player, curses.ACS_VLINE)

						for idx, item in enumerate([curses.ACS_LLCORNER, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_LRCORNER]):
							screen.addch(col_counter + 2, (j * 6 + idx) + offset_items_player, item)
						if j == selected_item[1] and i == selected_item[0]:
							screen.attroff(curses.color_pair(145))
						else:
							screen.attroff(curses.color_pair(rarity_colors[inv_matrix[i][j].rarity]))
				col_counter += 4
				counter += 1
				if counter == 6:
					break
		else:
			inv_matrix = [[False for i in range(10)] for i in range(max_matrix_rows)]

		#	show selected item and items to sell
		# 		show selected_item_frame
		frame_start = 35
		frame_end = 115
		screen.addch(28, frame_start, curses.ACS_ULCORNER)
		screen.addch(38, frame_start, curses.ACS_LLCORNER)
		for i in range(frame_start + 1, frame_end):
			screen.addch(28, i, curses.ACS_HLINE)
			screen.addch(38, i, curses.ACS_HLINE)
		for i in range(28 +1, 38):
			screen.addch(i, frame_start, curses.ACS_VLINE)
			screen.addch(i, frame_end, curses.ACS_VLINE)
		screen.addch(28, frame_end, curses.ACS_URCORNER)
		screen.addch(38, frame_end, curses.ACS_LRCORNER)

		# show NPC inventory
		#	show selected item and items to buy
		start_offset_tabs_npc = 80
		for i in range(len(npc_tabs)):
			if i == selected_tab_npc:
				screen.attron(curses.color_pair(145))
				screen.addstr(1, start_offset_tabs_npc, npc_tabs[i])
				screen.attroff(curses.color_pair(145))
			else:
				screen.addstr(1, start_offset_tabs_npc, npc_tabs[i])
			start_offset_tabs_npc += len(npc_tabs[i]) + 1

		offset_items_npc = 80
		show_inv_npc = [x for x in npc_invent if x.type == inv_type[selected_tab_npc]]
		if len(show_inv_npc) != 0:
			max_matrix_rows_npc = len(show_inv_npc) // 10 + 1
			inv_matrix_npc = [[False for i in range(10)] for i in range(max_matrix_rows_npc)]
			for i in range(len(inv_matrix_npc)):
				for j in range(len(inv_matrix_npc[0])):
					try:
						inv_matrix_npc[i][j] = show_inv_npc.pop()
					except IndexError:
						break
			col_counter = 4
			counter = 0
			for i in range(inv_scroll_npc, len(inv_matrix_npc)):
				for j in range(len(inv_matrix_npc[0])):
					if inv_matrix_npc[i][j] != False:
						if j == selected_item_npc[1] and i == selected_item_npc[0] and player_view == False:
							screen.attron(curses.color_pair(145))
						else:
							screen.attron(curses.color_pair(rarity_colors[inv_matrix_npc[i][j].rarity]))
						for idx, item in enumerate([curses.ACS_ULCORNER, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_URCORNER]):
							screen.addch(col_counter, (j * 6 + idx) + offset_items_npc, item)
						screen.addch(col_counter + 1, (j * 6) + offset_items_npc, curses.ACS_VLINE)
						screen.addstr(col_counter + 1, (j * 6 + 1) + offset_items_npc, inv_matrix_npc[i][j].readable_name[:3])
						screen.addch(col_counter + 1, (j * 6 + 4) + offset_items_npc, curses.ACS_VLINE)

						for idx, item in enumerate([curses.ACS_LLCORNER, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_LRCORNER]):
							screen.addch(col_counter + 2, (j * 6 + idx) + offset_items_npc, item)
						if j == selected_item_npc[1] and i == selected_item_npc[0] and player_view == False:
							screen.attroff(curses.color_pair(145))
						else:
							screen.attroff(curses.color_pair(rarity_colors[inv_matrix_npc[i][j].rarity]))
				col_counter += 4
				counter += 1
				if counter == 6:
					break
		else:
			inv_matrix_npc = [[False for i in range(10)] for i in range(max_matrix_rows_npc)]
		# show information about selected item
		if player_view:
			current = inv_matrix[selected_item[0]][selected_item[1]]
		else:
			current = inv_matrix_npc[selected_item_npc[0]][selected_item_npc[1]]

		screen.attron(curses.color_pair(136))
		if current:
			screen.addstr(29,frame_start + 1, f"Name: {current.readable_name}")
			screen.addstr(30, frame_start + 1, f"Description: {current.description}")
			if current.equippable:
				screen.addstr(31, frame_start + 1, f"Attack: {current.attack}")
				screen.addstr(32, frame_start + 1, f"Defence: {current.defence}")
				if current.effect_description:
					screen.addstr(33, frame_start + 1, f"Effect: {current.effect_description}")
			if player_view:
				screen.addstr(37, frame_start + 1, f"Sell price: {current.sell_price} gold")
			else:
				if state.player.gold >= current.buy_price:
					screen.attron(curses.color_pair(134))
					screen.addstr(37, frame_start + 1, f"Buy price: {current.buy_price} gold")
					screen.attroff(curses.color_pair(134))
				else:
					screen.attron(curses.color_pair(133))
					screen.addstr(37, frame_start + 1, f"Buy price: {current.buy_price} gold")
					screen.attroff(curses.color_pair(133))
		else:
			screen.addstr(33,frame_start + 40 - int(len("No item selected") / 2), "No item selected")

		screen.attroff(curses.color_pair(136))

		# show information on sellprice, buy price and gold handed over (<- or ->)
		k = screen.getch()

		if k == 9:
			if player_view:
				selected_item = [0,0]
				inv_scroll = 0
				selected_tab += 1
				if selected_tab >= len(tabs):
					selected_tab = 0
			else:
				selected_item_npc = [0,0]
				selected_tab_npc += 1
				inv_scroll_npc = 0
				if selected_tab_npc >= len(npc_tabs):
					selected_tab_npc = 0
		
		elif k == curses.KEY_DOWN:
			if player_view:
				selected_item[0] += 1
				if selected_item[0] >= max_matrix_rows - 1:
					selected_item[0] = max_matrix_rows - 1
					if inv_matrix[selected_item[0]][selected_item[1]] == False:
						selected_item[0] -= 1
				if selected_item[0] > inv_scroll + 5:
					inv_scroll += 1
					if inv_scroll > max_matrix_rows - 5:
						inv_scroll -= 1
						selected_item[0] -= 1
			else:
				selected_item_npc[0] += 1
				if selected_item_npc[0] >= max_matrix_rows_npc - 1:
					selected_item_npc[0] = max_matrix_rows_npc - 1
					if inv_matrix_npc[selected_item_npc[0]][selected_item_npc[1]] == False:
						selected_item_npc[0] -= 1
				if selected_item_npc[0] > inv_scroll_npc + 5:
					inv_scroll_npc += 1
					if inv_scroll_npc > max_matrix_rows_npc - 5:
						inv_scroll_npc -= 1
						selected_item_npc[0] -= 1


		elif k == curses.KEY_UP:
			if player_view:
				selected_item[0] -= 1
				if selected_item[0] < 0:
					selected_item[0] = 0
				if selected_item[0] < inv_scroll:
					inv_scroll -= 1
			else:
				selected_item_npc[0] -= 1
				if selected_item_npc[0] < 0:
					selected_item_npc[0] = 0
				if selected_item_npc[0] < inv_scroll_npc:
					inv_scroll_npc -= 1

		elif k == curses.KEY_RIGHT:
			if player_view:
				selected_item[1] += 1
				if selected_item[1] >= 10:
					selected_item[1] = 9
				if inv_matrix[selected_item[0]][selected_item[1]] == False:
					selected_item[1] -= 1
			else:
				selected_item_npc[1] += 1
				if selected_item_npc[1] >= 10:
					selected_item_npc[1] = 9
				if inv_matrix_npc[selected_item_npc[0]][selected_item_npc[1]] == False:
					selected_item_npc[1] -= 1

		elif k == curses.KEY_LEFT:
			if player_view:
				selected_item[1] -= 1
				if selected_item[1] < 0:
					selected_item[1] = 0
			else:
				selected_item_npc[1] -= 1
				if selected_item_npc[1] < 0:
					selected_item_npc[1] = 0

		elif k == ord(" "):
			if player_view:
				if not current:
					continue
				sell = helper.yes_no(screen, state, [f"Sell {current.readable_name} for {current.sell_price} gold?"])
				if sell:
					state.player.gold += current.sell_price
					state.player.inventory.pop(state.player.inventory.index(current))

			else:
				if not current:
					continue
				if state.player.gold < current.buy_price:
					helper.popup(screen, state, ["You cannot afford that."])
					continue
				buy = helper.yes_no(screen, state, [f"Buy {current.readable_name} for {current.buy_price} gold?"])
				if buy:
					state.player.gold -= current.buy_price
					state.player.inventory.append(current)
				else:
					continue

		elif k == ord("c"):
			player_view = not player_view

		elif k == ord("b"):
			return False 

	return True

def view_inventory_2(state):
	#Initial thoughs
	#Go for a skyrim-esque inventory management composed of "tabs" going deeper and a marker for equipped items (automatically at the top)
	#Try to go for alphabetical order
	#Inital thoughts of width: (1) + 10,(1) + 10,(1) + 35, (1) + 90 (for item art etc) + (1)
	
	###############################################################################
	#Armor -> # Head     # Leather Gloves *     # Assassin Vambrace               #
	#Weapons  #	Chest -> # Assassin Vambrace -> # Attack: 0                       #
	#Crafting # Hands    # Plate Gloves         # Defence: 2                      #
	#         # Feet     #                      # Effect: Critical chance +3%     #
	#         #          #                      #                                 #
	###############################################################################
	#Space: Use                                                                   #
	#E    : Equip                                                                 #
	###############################################################################

	#Init some variables regarding player inventory and equipment
	inventory = state.player.inventory
	list_of_equipped_items = list(state.player.equipment.values())

	#Static values
	list_of_types = ["Armor", "Weapons", "Crafting", "Key Items", "Consumables"]
	dict_of_subtypes = {
		"Armor": ["Head", "Chest", "Legs", "Feet", "Neck", "Finger"],
		"Weapons" : ["Swords", "Maces", "Shields", "Wands", "Staves", "Catalysts"],
		"Crafting" : ["Flora","Seeds", "Metals", "Creature products", "Magical", "Misc"],
		"Key Items": ["Quest", "Keys", "Books", "Tools"],
		"Consumables" : ["Potions", "Elixirs", "Brews", "Scrolls", "Food"]
	}
	dict_of_subtypes_translations = {
		"Armor" : ["head", "chest", "legs", "boots", "neck", "ring"],
		"Weapons" : ["sword", "mace", "shield", "wand", "staff", "catalyst"],
		"Crafting" : ["flora", "seed", "metal", "creature", "magical", "misc"],
		"Key Items" : ["quest", "key", "book", "tool"],
		"Consumables" : ["potion", "elixir", "brew", "scroll", "food"]
	}
	
	#Distance for each column
	type_end = 14
	subtype_end = 34
	item_end = 70
	
	#Selection variables
	#0 = Type
	#1 = subtype
	#2 = item
	selected_tab = [0,0,0]
	currently_selected_tab = 0

	#init screen variable to make easier use
	screen = state.stdscr #Use whole screen with stdscr
	k = -1 #Reset key

	while k != ord("q"): #Press Q to exit inventory menu
		screen.clear() # Clear old screen

		#Init the border-grid
		#Top row, all the way
		screen.addch(0, 0, curses.ACS_ULCORNER) #Upper left corner of the columns
		screen.addch(0, 148, curses.ACS_URCORNER) #Upper right corner of the columns
		for i in range(1, 148):
			screen.addch(49, i, curses.ACS_HLINE) # Add horizontal line on bottom row
			if i == type_end:
				screen.addch(0, i, curses.ACS_TTEE) #Add our first pillar
				screen.addch(43, i, curses.ACS_BTEE) #Add our first pillar
				continue
			if i == subtype_end:
				screen.addch(0, i, curses.ACS_TTEE) #Add our second pillar
				screen.addch(43, i, curses.ACS_BTEE) #Add our second pillar
				continue
			if i == item_end:
				screen.addch(0, i, curses.ACS_TTEE) #Add our Third pillar
				screen.addch(43, i, curses.ACS_BTEE) #Add our Third pillar
				continue
			if i == item_end + 20: #1/4 of information window
				screen.addch(0, i, curses.ACS_TTEE) #Add art-border
				screen.addch(23, i, curses.ACS_LLCORNER)
				screen.addch(43, i, curses.ACS_HLINE) # Add horizontal Line on "middle" row
				continue
			if i == item_end + 20 + 39: # 1/4 + 2/4 of information window
				screen.addch(0, i, curses.ACS_TTEE)
				screen.addch(23, i, curses.ACS_LRCORNER)
				screen.addch(43, i, curses.ACS_HLINE) # Add horizontal Line on "middle" row
				continue
			if item_end + 20 < i < item_end + 20 + 39:
				screen.addch(23, i, curses.ACS_HLINE)


			screen.addch(0, i, curses.ACS_HLINE) # Add horizontal lines on top row
			screen.addch(43, i, curses.ACS_HLINE) # Add horizontal Line on "middle" row
			

		#Bottom Row, all the way
		screen.addch(49, 0, curses.ACS_LLCORNER) # Lower left corner
		screen.addch(49, 148, curses.ACS_LRCORNER) #Lower Right Corner
		# For the line between them we can bake in to the for-loop from before

		# "Middle Row" just above commands
		#Let's give that about 5 rows of information (49 - 5 = 44) (44 - 1 = 43)
		screen.addch(43, 0, curses.ACS_LTEE) #Connecting left T
		screen.addch(43, 148, curses.ACS_RTEE) #Reversed on other side
		for i in range(1,49):
			if i == 43:
				continue # Skip our tee-subtypes
			if i < 43: #Between "middle" and top row, where our information go
				screen.addch(i, type_end, curses.ACS_VLINE) #First pillar
				screen.addch(i, subtype_end, curses.ACS_VLINE) #Second pillar
				screen.addch(i, item_end, curses.ACS_VLINE) #Third pillar
				if i < 23:
					screen.addch(i, item_end + 20, curses.ACS_VLINE)
					screen.addch(i, item_end + 20 + 39, curses.ACS_VLINE)
			screen.addch(i, 0, curses.ACS_VLINE) #Add Vertical line
			screen.addch(i,148, curses.ACS_VLINE)

		#Add Labels
		screen.addstr(0, 1 , "Type")
		screen.addstr(0, type_end + 1, "Subtype")
		screen.addstr(0, subtype_end + 1, "Item")
		screen.addstr(0, item_end + 1, "Information")

		#Static Stuff (ex. Labels (types and subtypes (will always be the same)))
		#Print out the types (First column)
		for idx, item in enumerate(list_of_types): #List over the item types and their indexx
			if item == list_of_types[selected_tab[0]]: #If the item is equal to selected (x-axis) item in the types list
				if currently_selected_tab == 0: #if the type-tab is also currently selected (means we can move in it)
					screen.attron(curses.color_pair(5)) #Add a green color
				else: #Else if we are on another tab, but the selected type is the last one we chose
					screen.attron(curses.color_pair(138)) #Add a nice orange color (Our favourite)
				screen.addstr(idx + 2, 1, item)
				if currently_selected_tab == 0: #Deactivate it all
					screen.attroff(curses.color_pair(5))
				else:
					screen.attroff(curses.color_pair(138))
			else:
				screen.addstr(idx + 2, 1, item)

		temp_subtypes = dict_of_subtypes[list_of_types[selected_tab[0]]] #To make it easier to type
		for idx, item in enumerate(temp_subtypes): #For each in temp subtype we made earlier
			if item == temp_subtypes[selected_tab[1]]: #If the current iteration is the one we have selected, make it coloured green
				if currently_selected_tab == 1:
					screen.attron(curses.color_pair(5))
				else:
					screen.attron(curses.color_pair(138)) #Else if we are on another tab, make it a nice orange color (our favorite)
				screen.addstr(idx + 2, type_end + 1, item)
				if currently_selected_tab == 1:
					screen.attroff(curses.color_pair(5))
				else:
					screen.attroff(curses.color_pair(138))
			else:
				screen.addstr(idx + 2, type_end + 1, item)


		#Dynamic content (ex. items and item information)

		#Possible rebase: just print the right subtypes and their list.count(item), can be hard to sort a-z though


		#Get the currently selected type and subtype items from the player inventory
		dynamic_inventory = []
		for item in inventory:
			typ = list_of_types[selected_tab[0]] #wow, long line, we need to shorten it to just "subtype" variable
			if item.subtype == dict_of_subtypes_translations[typ][selected_tab[1]]: #If it is the right subtype
				dynamic_inventory.append(item) # we add it to the dynamic inventory

		already_printed = {} #This dict holds just the name and number of that item we have, so we can print it easily
		real_name_translation = {}
		for item in dynamic_inventory:
			if item.readable_name not in already_printed.keys():
				already_printed[item.readable_name] = 1
			else:
				already_printed[item.readable_name] += 1

			if item.name not in real_name_translation.items():
				real_name_translation[item.readable_name] = item.name

		dynamic_print_inventory = [(item_name, count) for item_name, count in already_printed.items()]
		
		#Here we do the outputting to the terminal for the item panel
		for idx, item in enumerate(dynamic_print_inventory):
			if item[0] == dynamic_print_inventory[selected_tab[2]][0]:
				if currently_selected_tab == 2:
					screen.attron(curses.color_pair(5))
				else:
					screen.attron(curses.color_pair(138))
			screen.addstr(idx + 1, subtype_end + 2, f"{item[0]}: {item[1]}")
			if item[0] == dynamic_print_inventory[selected_tab[2]][0]:
				if currently_selected_tab == 2:
					screen.attroff(curses.color_pair(5))
				else:
					screen.attroff(curses.color_pair(138))

		#Information screen
		if len(dynamic_print_inventory) != 0:
			copy_of_item = helper.get_item(real_name_translation[dynamic_print_inventory[selected_tab[2]][0]])() #init an item based on the readable name from print_inventory, translated
			
			#Art furthest up, info lower, preferably enclose art in a border
			# Update: border added to earlier functions defining x/y-axis ACS_stuff
			#Let's give art about ~20 spaces offset by 5
			if copy_of_item.art:
				art_height = len(copy_of_item.art)
				art_length = max([len(item) for item in copy_of_item.art])
				art_x_start = int((21 - art_height) / 2) #Get the offset to make sure the height of the art is in the middle of the "artbox"
				art_y_start = int((39 - art_length) / 2) #Get the offset to make sure the length of the art is in the middle of the "artbox"
				for idx, row in enumerate(copy_of_item.art):
					screen.addstr(idx + art_x_start, item_end + 20 + art_y_start, row) #Print the art

			# Now for the actual information
			#Let's make use of the left side column next to the art for some general stats (or maybe no...)
			#For weapons:
			if copy_of_item.type == "weapon":
				screen.addstr(24, item_end + 2, f"Attack: {copy_of_item.attack}")
				screen.addstr(25, item_end + 2, f"Attack: {copy_of_item.defence}")
				screen.addstr(26, item_end + 2, f"Damage type: {copy_of_item.damage_type}")
				if copy_of_item.effect_description:
					screen.addstr(27, item_end + 2, f"Effect: {copy_of_item.effect_description}")
				else:
					screen.addstr(27, item_end + 2, "Effect: None")
			screen.addstr(29, item_end + 2, f"Description:")
			screen.addstr(30, item_end + 2, copy_of_item.description)

		#Debug
		screen.addstr(44, 0, f"Currently_selected_tab = {currently_selected_tab}")
		screen.addstr(45, 0, f"selected_tab[currently_selected_tab] = {selected_tab[currently_selected_tab]}")


		k = screen.getch() #Get the player input

		if k == curses.KEY_DOWN:
			if currently_selected_tab < 2: #Hardcoded number of tabs (0 = types, 1 = subtypes 2 = items)
				selected_tab[currently_selected_tab + 1] = 0
			selected_tab[currently_selected_tab] += 1
			if currently_selected_tab == 0: #Here we neede to make a 
				if selected_tab[currently_selected_tab] > len(list_of_types) - 1: #check if we go over
					selected_tab[currently_selected_tab] = len(list_of_types) - 1 #If so, reset to max index 
			elif currently_selected_tab == 1:
				if selected_tab[currently_selected_tab] > len(temp_subtypes) - 1: #check if we go over
					selected_tab[currently_selected_tab] = len(temp_subtypes) - 1 #If so, reset to max index
			elif currently_selected_tab == 2:
				if selected_tab[currently_selected_tab] > len(dynamic_print_inventory) - 1: #check if we go over
					selected_tab[currently_selected_tab] = len(dynamic_print_inventory) - 1 #If so, reset to max index

		if k == curses.KEY_UP:
			if currently_selected_tab < 2:
				selected_tab[currently_selected_tab + 1] = 0
			selected_tab[currently_selected_tab] -= 1
			if selected_tab[currently_selected_tab] < 0: #Check if we go under 0
				selected_tab[currently_selected_tab] = 0 #If so, reset it to 0

		if k == curses.KEY_RIGHT: #Right is to "go forward" a tab
			if currently_selected_tab == 1:
				if len(dynamic_print_inventory) !=0:
					currently_selected_tab += 1
				else:
					currently_selected_tab += 0
			else:
				currently_selected_tab += 1
			if currently_selected_tab > len(selected_tab) - 1: #Check if we go under length of all columns
				currently_selected_tab = len(selected_tab) - 1 #If so, reset it to max

		if k == curses.KEY_LEFT: #Left is to "go back" a tab
			currently_selected_tab -= 1
			if currently_selected_tab < 0: #Check if we go under 0
				currently_selected_tab = 0 #If so, reset it to 0



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
	screen = state.stdscr

	height, width = screen.getmaxyx()

	start = int(height / 2)
	offset = int(width / 2)

	while k != ord("q"):
		screen.clear()

		if state.player.spells[old_spell_index] == False:
			explain_text = "Choose a spell to replace {}".format("[Empty Slot]")
		else:
			explain_text = "Choose a spell to replace {}".format(state.player.spells[old_spell_index].readable_name)

		screen.addstr(10, offset - int((len("Inactive Spells") / 2)), "Inactive Spells")
		screen.addstr(11, offset - int((len(explain_text) / 2)), explain_text)

		for i in range(len(state.player.spellbook)):
			if i == selected_item:
				screen.attron(curses.color_pair(5))
			
			screen.addstr(start + i, offset - int((len(state.player.spellbook[i].readable_name) / 2)), state.player.spellbook[i].readable_name)

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
	screen = state.stdscr
	screen.clear()

	k = -1
	selected_item = 0

	height, width = screen.getmaxyx()

	start = int(height / 2)
	offset = int(width / 2)

	

	while k != ord("q"):
		screen.clear()

		explain_text = "You can have a maximum of 5 active spells equipped."

		screen.addstr(10, offset - int((len("Active Spells") / 2)), "Active Spells")
		screen.addstr(11, offset - int((len(explain_text) / 2)), explain_text)

		for i in range(0,5):
			if i == selected_item:
				screen.attron(curses.color_pair(5))
			
			if state.player.spells[i] == False:
				screen.addstr(start + i, offset - int((len("[Empty Slot]") / 2)), "[Empty Slot]")
			else:
				screen.addstr(start + i, offset - int((len(state.player.spells[i].readable_name) / 2)), state.player.spells[i].readable_name)

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