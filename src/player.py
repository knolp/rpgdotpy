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

		self.gear_stats = {
			"Intelligence" : 0,
			"Strength" : 0,
			"Charisma" : 0,
			"Agility" : 0,
			"Attunement" : 0,
			"Alchemy" : 0,
			"Farming" : 0
		}

		self.last_pos = (3,3)
		self.last_target = ["TradeDistrict", 0, 0]

		#Minions
		self.max_minions = 3
		self.minion_pos = [self.last_pos] * self.max_minions
		self.minions = []

		self.ascii = False

		#Combat stuff

		self.status_effects = []
		self.immune = []
		self.health = 1999
		self.max_health = 2000
		self.gold = 10000
		self.player = True

		self.equipment = {
			"head" : False,
			"chest" : False,
			"legs" : False,
			"left_hand" : False,
			"right_hand": False,
			"boots" : False,
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

	def get_combined_stats(self):
		return {
			"Intelligence" : self.stats["Intelligence"] + self.gear_stats["Intelligence"],
			"Strength" : self.stats["Strength"] + self.gear_stats["Strength"],
			"Charisma" : self.stats["Charisma"] + self.gear_stats["Charisma"],
			"Agility" : self.stats["Agility"] + self.gear_stats["Agility"],
			"Attunement" : self.stats["Attunement"] + self.gear_stats["Attunement"],
			"Alchemy" : self.stats["Alchemy"] + self.gear_stats["Alchemy"],
		}

	def _populate_gear_stats(self):
		for slot, item in self.equipment.items():
			if item and item.stat_increase:
				self.gear_stats[item.stat_increase[0]] += item.stat_increase[1]


if __name__ == '__main__':
	items = {
		"name" : "hej",
		"boop" : 3
		}

	dummy = Dummy(items)

