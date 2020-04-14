import states
import helper
import random
import animation

def go_west(state,location):
	state.player.location = getattr(states, location)
	state.player.y = 95

	state.update_map()

def go_east(state,location):
	state.player.location = getattr(states, location)
	state.player.y = 2

	state.update_map()

def go_north(state,location):
	state.player.location = getattr(states, location)
	state.player.x = 36

	state.update_map()

def go_south(state,location):
	state.player.location = getattr(states, location)
	state.player.x = 2

	state.update_map()
	
def StarterTown_north(state):
	state.player.location = getattr(states, "GreenForest")
	state.player.x = 36

	state.update_map()

def StarterTown_west(state):
	state.player.location = getattr(states, "HuntersCamp")
	state.player.y = 95

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
			"Door locked.",
			"Ask me if you need access",
			"[- Osk'Ghar]"
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


def StarterTown_haunted_house_3_entrance(state):
	state.player.location = getattr(states, "StarterTown_haunted_house_3")

	state.player.x = 36
	state.player.y = 72

	state.update_map()

def StarterTown_haunted_house_3_back_exit(state):
	state.player.location = getattr(states, "StarterTown_haunted_house_2")

	state.player.x = 2
	state.player.y = 72

	state.update_map()

def StarterTown_haunted_house_3_sewer_exit(state):
	state.player.location = getattr(states, "GreenForest")

	state.player.x = 22
	state.player.y = 86

	state.update_map()
	state.save_player(quicksave=True)



def GreenForest_south(state):
	state.player.location = getattr(states, "StarterTown")
	state.player.x = 2

	state.update_map()

def GreenForest_west(state):
	state.player.location = getattr(states, "TradeDistrict")
	state.player.y = 95

	state.update_map()

def GreenForest_brown_bear_inn_entrance(state):
	state.player.location = getattr(states, "BrownBearInn")
	state.player.x = 33
	state.player.y = 49

	state.update_map()

def GreenForest_sewer_entrance(state):
	state.player.location = getattr(states, "StarterTown_haunted_house_3")
	state.player.x = 20
	state.player.y = 14

	state.update_map()



def BrownBearInn_exit(state):
	state.player.location = getattr(states, "GreenForest")
	state.player.x = 11
	state.player.y = 21

	state.update_map()


def GreenForest_hall_of_justice_entrance(state):
	state.player.location = getattr(states, "HallOfJustice")
	state.player.x = 33
	state.player.y = 48

	state.update_map()

def GreenForest_tanner_entrance(state):
	state.player.location = getattr(states, "TannerHouse")
	state.player.x = 25
	state.player.y = 47

	state.update_map()

def GreenForest_tanner_exit(state):
	state.player.location = getattr(states, "GreenForest")
	state.player.x = 25
	state.player.y = 11

	state.update_map()


def HallOfJustice_exit(state):
	state.player.location = getattr(states, "GreenForest")
	state.player.x = 15
	state.player.y = 72

	state.update_map()

def GreenForest_player_house_entrance(state):
	state.player.location = getattr(states, "StarterTownPlayerHouse")
	state.player.x = 33
	state.player.y = 48

	state.update_map()

def StarterTown_player_house_exit(state):
	state.player.location = getattr(states, "GreenForest")
	state.player.x = 25
	state.player.y = 31

	state.update_map()


def TradeDistrict_east(state):
	state.player.location = getattr(states, "GreenForest")
	state.player.y = 2

	state.update_map()

def TradeDistrict_south(state):
	state.player.location = getattr(states, "HuntersCamp")
	state.player.x = 2

	state.update_map()

def TradeDistrict_alchemist_entrance(state):
	state.player.location = getattr(states, "TradeDistrictAlchemist")
	state.player.x, state.player.y = 23,47

	state.update_map()

def TradeDistrict_alchemist_exit(state):
	state.player.location = getattr(states, "TradeDistrict")
	state.player.x, state.player.y = 20,20

	state.update_map()

def HuntersCamp_north(state):
	state.player.location = getattr(states, "TradeDistrict")
	state.player.x = 36

	state.update_map()

def HuntersCamp_east(state):
	state.player.location = getattr(states, "StarterTown")
	state.player.y = 2

	state.update_map()

def GrandPalace_interior_entrance_enter(state):
	state.player.location = getattr(states, "GrandPalace_interior_entrance")
	state.player.x = 34
	state.player.y = 48

	state.update_map()

def GrandPalace_interior_entrance_exit(state):
	state.player.location = getattr(states, "StarterTownLeftWall")
	state.player.x = 4
	state.player.y = 33

	state.update_map()

def LeftWall_library_enter(state):
	state.player.location = getattr(states, "LeftWallLibrary")
	state.player.x, state.player.y = 23,47

	state.update_map()

def LeftWall_library_exit(state):
	state.player.location = getattr(states, "StarterTownLeftWall")
	state.player.x, state.player.y = 24,48

	state.update_map()


def RandomCave(state, target):
	state.player.seed = random.randint(3554,19929292)
	state.player.location = getattr(states, "RandomCave")
	state.player.last_target = target
	#state.player.y = random.randint(3,95)
	#state.player.x = random.randint(3,34)

	state.update_map(target=target)