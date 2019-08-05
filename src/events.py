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







def GreenForest_south(state):
	state.player.location = getattr(states, "StarterTown")
	state.player.x = 2

	state.update_map()