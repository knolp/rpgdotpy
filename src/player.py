import json
import states
import items
import helper
import random
import abilities
import recipes

def create_player(create_player):
	return Player(create_player)


def load_player():
	pass

class Dummy():
	def __init__(self, items):
		for k,v in items.items():
			print(k,v)
			self.k = v
		self.flags = []
		self.inventory = []

class Player():
	def __init__(self, create_dict):
		"""self.name = create_dict["name"]
								self.x = create_dict["x"]
								self.y = create_dict["y"]
								self.location = create_dict["location"]
						
								self.turn = create_dict["turn"]
						
								self.gold = create_dict["gold"]
								self.inventory = create_dict["inventory"]
						
								self.equipped = create_dict["equipped"]"""

		for key in create_dict:
			setattr(self, key, create_dict[key])
		
		self.time = 0
		self.seed = 34444
		self.flora = [] #t.ex ["StarterTown_ariam_bush", 100 (#timestamp), 1000 (#time dead)]
		self.location = getattr(states, create_dict["location"])
		self.inventory = [
			items.AriamSeed(),
			items.TrainingSword()
		]

		self.temp_alchemy_inventory = []
		self.recipes = []
		self.active_farms = [] #0=id,1=Plant,2=time_planted,3=result,4=harvest_time
		self.hotkeys = {
			"1" : False,
			"2" : abilities.PhaseShift(),
			"3" : False,
			"4" : False,
			"5" : False,
			"6" : False,
		}

		self.stats = {
			"Intelligence" : 13,
			"Strength" : 2,
			"Charisma" : 13,
			"Agility" : 13,
			"Attunement" : 13,
			"Alchemy" : 13,
			"Farming" : 13
		}

		self.last_pos = (3,3)
		self.last_target = ["TradeDistrict", 0, 0]

		self.ascii = False

		#Combat stuff

		self.status_effects = []
		self.immune = []
		self.health = 1000
		self.max_health = 1000
		self.gold = 10000
		self.player = True

		self.equipment = {
			"head" : items.ChainHelmet(),
			"chest" : items.ChainMail(),
			"legs" : items.StuddedLegs(),
			"left_hand" : False,
			"right_hand": items.IronMace(),
			"boots" : items.LeatherBoots(),
			"ring_1" : False,
			"ring_2" : False,
			"neck" : False
		}



		#Spellstuff
		self.mindvision = 0
		self.phaseshift = 0

	def draw(self, screen):
		if self.phaseshift:
			screen.addstr(self.x, self.y, str(self.phaseshift))
		else:
			screen.addstr(self.x, self.y, "@")


if __name__ == '__main__':
	items = {
		"name" : "hej",
		"boop" : 3
		}

	dummy = Dummy(items)

	print(dummy.k)
