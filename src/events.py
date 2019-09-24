import states
import helper


def StarterTown_north(state):
	state.player.location = getattr(states, "GreenForest")
	state.player.x = 36

	state.update_map()

def StarterTown_door(state):
	state.player.location = getattr(states, "StarterTown_house")
	state.player.x = 23
	state.player.y = 47

	state.update_map()

def StarterTown_house_door(state):
	state.player.location = getattr(states, "StarterTown")
	state.player.x = 18
	state.player.y = 47

	state.update_map()

def StarterTown_house_basement_door_entrance(state):
	inv_list = [item.name for item in state.player.inventory]
	if "BasementKey" in inv_list:
		state.player.location = getattr(states, "StarterTown_house_basement")
		state.player.x = 23
		state.player.y = 47

		state.update_map()
	else:
		helper.popup(state.game_box, state, [
			"You try to open the door, but it is locked.",
			"You notice a sign on the door that reads:",
			"",
			"'Door locked.",
			"Ask me if you need access",
			"- Osk'Ghar'"
			])
		state.player.x = 14
		state.player.y = 32

def StarterTown_house_basement_door_exit(state):
	state.player.location = getattr(states, "StarterTown_house")
	state.player.x = 14
	state.player.y = 32

	state.update_map()


def StarterTown_house_basement_door_to_hallway_entrance(state):
	state.player.location = getattr(states, "StarterTown_house_basement_hallway")

	state.player.x = 2
	state.player.y = 83

	state.update_map()

def StarterTown_house_basement_hallway_door_exit(state):
	state.player.location = getattr(states, "StarterTown_house_basement")

	state.player.x = 36
	state.player.y = 83

	state.update_map()

def StarterTown_haunted_house_entrance(state):
	state.player.location = getattr(states, "StarterTown_haunted_house_1")

	state.player.x = 23
	state.player.y = 47

	state.update_map()

def StarterTown_haunted_house_exit(state):
	state.player.location = getattr(states, "StarterTown")

	state.player.x = 9
	state.player.y = 73

	state.update_map()

def StarterTown_haunted_house_hole_entrance(state):
	state.player.location = getattr(states, "StarterTown_haunted_house_2")

	state.update_map()

def StarterTown_haunted_house_2_dungeon_door_left(state):
	if "HauntedHouse_dungeon_door_left_opened" in state.player.flags:
		return
	inv_list = [item.name for item in state.player.inventory]
	if "DungeonKeyHaunted" in inv_list:
		answer = helper.yes_no(state.game_box, state, [
			"Your key seems to fit perfect.",
			"",
			"Do you open the door?"
		])
		if answer:
			state.player.flags.append("HauntedHouse_dungeon_door_left_opened")
			state.player.x = 29
			state.player.y = 66
		else:
			state.player.x = 29
			state.player.y = 67
		
	else:
		helper.popup(state.game_box, state, [
			"You try to open the door, but it is locked."
			])
		state.player.x = 29
		state.player.y = 67

def StarterTown_haunted_house_2_dungeon_door_right(state):
	if "HauntedHouse_dungeon_door_right_opened" in state.player.flags:
		return
	inv_list = [item.name for item in state.player.inventory]
	if "DungeonKeyHaunted" in inv_list:
		answer = helper.yes_no(state.game_box, state, [
			"Your key seems to fit perfect.",
			"",
			"Do you open the door?"
		])
		if answer:
			state.player.flags.append("HauntedHouse_dungeon_door_right_opened")
			state.player.x = 29
			state.player.y = 82
		else:
			state.player.x = 29
			state.player.y = 81
		
	else:
		helper.popup(state.game_box, state, [
			"You try to open the door, but it is locked."
			])
		state.player.x = 29
		state.player.y = 81





def GreenForest_south(state):
	state.player.location = getattr(states, "StarterTown")
	state.player.x = 2

	state.update_map()

def GreenForest_brown_bear_inn_entrance(state):
	state.player.location = getattr(states, "BrownBearInn")
	state.player.x = 33
	state.player.y = 49

	state.update_map()



def BrownBearInn_exit(state):
	state.player.location = getattr(states, "GreenForest")
	state.player.x = 11
	state.player.y = 21

	state.update_map()
