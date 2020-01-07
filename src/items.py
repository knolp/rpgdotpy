import abilities
import art

import random

class Item():
    def __init__(self,name, usable):
        self.name = name
        self.usable = usable
        self.consumable = False
        self.description = "Description not implemented"
        self.damage_type = False
        self.art = art.draw_not_implemented()
        self.rarity = "common"
        self.sell_price = 10
        self.buy_price = int(self.sell_price * 1.5)
        self.effect_description = False

        #Alchemy stuff
        self.dryable = False
        self.juicable = False
        self.result = False


        self.attack_styles = {
            "Slash" : ["swings", "attacks", "slashes"],
            "Stab" : ["swings", "attacks", "stabs"],
            "Blunt" : ["swings", "attacks", "smashes"]
        }

    def __str__(self):
        return self.name

    def modifier(self, player, opponent):
        return False

    def effect(self, player, opponent):
        return False




#WEAPONS

class TrainingSword(Item):
    def __init__(self):
        super().__init__("TrainingSword", False)
        self.readable_name = "Training Sword"
        self.type = "weapon"
        self.equippable = "right_hand"
        self.attack = 0
        self.defence = 0
        self.description = "A training sword made out of wood, a bit chipped and worn out."
        self.damage_type = "Slash"

class Longsword(Item):
    def __init__(self):
        super().__init__("Longsword", False)
        self.readable_name = "Longsword"
        self.type = "weapon"
        self.equippable = "right_hand"
        self.attack = 2
        self.defence = 0
        self.description = "A longsword made from steel, a fine weapon indeed."
        self.damage_type = "Slash"
        self.art = art.draw_Longsword()

class IronMace(Item):
    def __init__(self):
        super().__init__("IronMace", False)
        self.readable_name = "Iron Mace"
        self.type = "weapon"
        self.equippable = "right_hand"
        self.attack = 2
        self.defence = 0
        self.description = "A mace made of iron, great for smashing."
        self.damage_type = "Blunt"
        self.effect_description = "Has a chance to cause stun."

    def effect(self, player, opponent):
        if opponent.player == True:
            readable_name = opponent.name
        else:
            readable_name = opponent.readable_name
        if random.randint(1,100) > 50:
            list_of_effects = [effect.type for effect in opponent.status_effects]
            if "Stun" not in list_of_effects:
                opponent.status_effects.append(abilities.Stun(2, readable_name))
                return {
                    "combat_text" : [
                        "{}'s heavy weight knocks {} to the ground".format(self.readable_name, readable_name),
                    ] 
                }
            else:
                return {
                    "combat_text" : False
                }

class Rapier(Item):
    def __init__(self):
        super().__init__("Rapier", False)
        self.readable_name = "Rapier"
        self.type = "weapon"
        self.equippable = "right_hand"
        self.attack = 2
        self.defence = 0
        self.description = "A pointy rapier."
        self.damage_type = "Stab"
        self.effect_description = "Has a chance to cause bleed."
        self.art = art.draw_Rapier()

    def effect(self, player, opponent):
        if opponent.player == True:
            opponent_readable_name = opponent.name
        else:
            opponent_readable_name = opponent.readable_name
        if "Bleed" in opponent.immune:
            return {
                "combat_text" : False
            }
        if random.randint(1,100) > 70:
            list_of_effects = [effect.type for effect in opponent.status_effects]
            if "Bleed" not in list_of_effects:
                opponent.status_effects.append(abilities.Bleed(5, 2, opponent_readable_name))
                return {
                    "combat_text" : [
                        "{}'s pointy tip makes a deep wound".format(self.readable_name),
                        "and causes {} to bleed.".format(opponent_readable_name)] 
                }
        else:
            return {
                "combat_text" : False
            }

class MoonlightSword(Item):
    def __init__(self):
        super().__init__("MoonlightSword", False)
        self.readable_name = "Moonlight Sword"
        self.type = "weapon"
        self.equippable = "right_hand"
        self.attack = 3
        self.defence = 0
        self.description = "A blade that glows ominously in the dark."
        self.damage_type = "Slash"
        self.rarity = "epic"
        self.effect_description = "Scales with intelligence"

    def modifier(self, player, opponent):
        return int(player.stats["Intelligence"] * 0.3)

class RatSmasher(Item):
    def __init__(self):
        super().__init__("RatSmasher", False)
        self.readable_name = "Rat Smasher"
        self.type = "weapon"
        self.equippable = "right_hand"
        self.attack = 1
        self.defence = 0
        self.description = "A wooden plank with a mithril nail poking out at the top."
        self.damage_type = "Stab"
        self.rarity = "unique"
        self.effect_description = "Deals double damage to rats"

    def modifier(self, player, opponent):
        if opponent.race == "Rat":
            return 2
        else:
            return False


class ChromaticBlade(Item):
    def __init__(self):
        super().__init__("ChromaticBlade", False)
        self.readable_name = "Chromatic Blade"
        self.type = "weapon"
        self.equippable = "right_hand"
        self.attack = 1
        self.defence = 0
        self.description = "A blade flashing with color."
        self.damage_type = "Stab"
        self.rarity = "unique"
        self.effect_description = "Can inflict multiple status effects."

    def effect(self, player, opponent):
        if opponent.player == True:
            opponent_readable_name = opponent.name
        else:
            opponent_readable_name = opponent.readable_name
        if random.randint(1,100) > 70:
            list_of_effects = [effect.type for effect in opponent.status_effects]
            if "Bleed" not in list_of_effects and "Bleed" not in opponent.immune:
                opponent.status_effects.append(abilities.Bleed(int(random.randint(1,7)), 2, opponent_readable_name))
            if "Chill" not in list_of_effects and "Chill" not in opponent.immune:
                opponent.status_effects.append(abilities.Chill(int(random.randint(1,7)), 2, opponent_readable_name))
            if "Burn" not in list_of_effects and "Burn" not in opponent.immune:
                opponent.status_effects.append(abilities.Burn(int(random.randint(1,7)), 2, opponent_readable_name))
            
            return {
                "combat_text" : [
                    "{} flashes as it hits it target".format(self.readable_name),
                    "and causes {} to experience a multiple of effects.".format(opponent_readable_name)] 
            }
        else:
            return {
                "combat_text" : False
            }

#OFF_HANDS
class Buckler(Item):
    def __init__(self):
        super().__init__("Buckler", False)
        self.readable_name = "Buckler"
        self.type = "weapon"
        self.equippable = "left_hand"
        self.attack = 0
        self.defence = 4
        self.description = "A small buckler with an insignia of a lion on the inside." 
        self.block_chance = 60

class CeramicDoll(Item):
    def __init__(self):
        super().__init__("CeramicDoll", False)
        self.readable_name = "Ceramic Doll"
        self.type = "weapon"
        self.equippable = "left_hand"
        self.attack = 0
        self.defence = 0
        self.description = "A ceramic doll with fiery red eyes."
        self.block_chance = 0



#HEAD

class ChainHelmet(Item):
    def __init__(self):
        super().__init__("ChainHelmet", False)
        self.readable_name = "Chain Helmet"
        self.type = "armor"
        self.equippable = "head"
        self.attack = 0
        self.defence = 2
        self.description = "A hood made out of chainmail, quite heavy to wear."
        self.art = art.draw_ChainHelmet()
        self.rarity = "common"


#CHEST

class ChainMail(Item):
    def __init__(self):
        super().__init__("ChainMail", False)
        self.readable_name = "Chain Mail"
        self.type = "armor"
        self.equippable = "chest"
        self.attack = 0
        self.defence = 2
        self.description = "A simple chainmail. Starting to get a bit rusty."
        self.art = art.draw_ChainMail()
        self.rarity = "rare"

#LEGS

class StuddedLegs(Item):
    def __init__(self):
        super().__init__("StuddedLegs", False)
        self.readable_name = "Studded Legs"
        self.type = "armor"
        self.equippable = "legs"
        self.attack = 0
        self.defence = 2
        self.description = "Leather legs reinforced with iron studs."
        self.rarity = "epic"

#BOOTS

class LeatherBoots(Item):
    def __init__(self):
        super().__init__("LeatherBoots", False)
        self.readable_name = "Leather Boots"
        self.type = "armor"
        self.equippable = "boots"
        self.attack = 0
        self.defence = 1
        self.description = "Boots made out of cheap leather."
        self.art = art.draw_LeatherBoots()
        self.rarity = "legendary"

#NECKLACES / JEWELERRY

class RatFangNecklace(Item):
    def __init__(self):
        super().__init__("RatFangNecklace", False)
        self.readable_name = "Ratfang Necklace"
        self.type = "armor"
        self.equippable = "neck"
        self.attack = 0
        self.defence = 0
        self.description = "A \"necklace\" made out of a large rat fang."
        self.art = art.draw_RatFangNecklace()
        self.rarity = "unique"





# Key Items
class BasementKey(Item):
    def __init__(self):
        super().__init__("BasementKey", False)
        self.readable_name = "Basement Key (Osk'Ghar)"
        self.type = "key"
        self.equippable = False
        self.description = "Unlocks the basement door at Osk'Ghar."

class DungeonKeyHaunted(Item):
    def __init__(self):
        super().__init__("DungeonKeyHaunted", False)
        self.readable_name = "Dungeon key (Haunted House)"
        self.type = "key"
        self.equippable = False
        self.description = "Unlocks a dungeon door somewhere."

class Shovel(Item):
    def __init__(self):
        super().__init__("Shovel", False)
        self.readable_name = "Shovel"
        self.type = "key"
        self.equippable = False
        self.description = "Good for digging."

class StarterTownHouseKey(Item):
    def __init__(self):
        super().__init__("StarterTownHouseKey", False)
        self.readable_name = "House Key (Starter Town)"
        self.type = "key"
        self.equippable = False
        self.description = "Unlocks the front door at the house in Starter Town"
        self.art = art.draw_key()
        self.rarity = "unique"







#Crafting Material
class DeverBerry(Item):
    def __init__(self):
        super().__init__("DeverBerry", False)
        self.readable_name = "Deverberry"
        self.type = "crafting"
        self.equippable = False
        self.description = "A cloudy, white berry. Smells atrocious."
        self.juicable = True
        self.result = ["DeverBerryJuice", "DeverBerrySkin"]

class DeverBerryJuice(Item):
    def __init__(self):
        super().__init__("DeverBerryJuice", False)
        self.readable_name = "Deverberry Juice"
        self.type = "crafting"
        self.equippable = False
        self.description = "A hideous smelling juice made from Deverberries"

class DeverBerrySkin(Item):
    def __init__(self):
        super().__init__("DeverBerrySkin", False)
        self.readable_name = "Deverberry Skin"
        self.type = "crafting"
        self.equippable = False
        self.description = "Probably has a better smell when dried."
        self.dryable = True
        self.result = ["DeverBerrySkinDried"]

class DeverBerrySkinDried(Item):
    def __init__(self):
        super().__init__("DeverBerrySkinDried", False)
        self.readable_name = "Deverberry Skin (Dried)"
        self.type = "crafting"
        self.equippable = False
        self.description = "Leathery skin of a dried deverberry."

class BarburaLeaf(Item):
    def __init__(self):
        super().__init__("BarburaLeaf", False)
        self.readable_name = "Barbura Leaf"
        self.type = "crafting"
        self.equippable = False
        self.description = "Yellow leaf picked from a Barbura bush."
        self.dryable = True
        self.result = ["BarburaLeafDried"]

class BarburaLeafDried(Item):
    def __init__(self):
        super().__init__("BarburaLeafDried", False)
        self.readable_name = "Barbura Leaf (Dried)"
        self.type = "crafting"
        self.equippable = False
        self.description = "A crunchy, sweet smelling leaf."

class AriamLeaf(Item):
    def __init__(self):
        super().__init__("AriamLeaf", False)
        self.readable_name = "Ariam Leaf"
        self.type = "crafting"
        self.equippable = False
        self.description = "An orange leaf from an Ariam plant."
        self.dryable = True
        self.result = ["AriamLeafDried"]

class AriamLeafDried(Item):
    def __init__(self):
        super().__init__("AriamLeafDried", False)
        self.readable_name = "Ariam Leaf (Dried)"
        self.type = "crafting"
        self.equippable = False
        self.description = "A crunchy, faded orange leaf."

class ButterflyWing(Item):
    def __init__(self):
        super().__init__("ButterflyWing", False)
        self.readable_name = "Butterfly Wing"
        self.type = "crafting"
        self.equippable = False
        self.description = "A shimmering wing."

class ArcaneDust(Item):
    def __init__(self):
        super().__init__("ArcaneDust", False)
        self.readable_name = "Arcane Dust"
        self.type = "crafting"
        self.equippable = False
        self.description = "A bottle containing a flowing sand-like material."

class TrollHair(Item):
    def __init__(self):
        super().__init__("TrollHair", False)
        self.readable_name = "Troll Hair"
        self.type = "crafting"
        self.equippable = False
        self.description = "A bunch of troll hairs tied together."

class DesertSalt(Item):
    def __init__(self):
        super().__init__("DesertSalt", False)
        self.readable_name = "Desert Salt"
        self.type = "crafting"
        self.equippable = False
        self.description = "A bottle of salt with the brand 'HMC', mined in the eastern desert."

class ObsidianShard(Item):
    def __init__(self):
        super().__init__("ObsidianShard", False)
        self.readable_name = "Obsidian Shard"
        self.type = "crafting"
        self.equippable = False
        self.description = "A shard of pure black obsidian from the eastern desert."


#Seeds
class BarburaSeed(Item):
    def __init__(self):
        super().__init__("BarburaSeed", False)
        self.readable_name = "Barbura Seed"
        self.type = "farming"
        self.equippable = False
        self.description = "A small green seed."
        self.result = ["BarburaLeaf"]
        self.level = 1
        self.harvest_time = 1209600 #2 weeks

class AriamSeed(Item):
    def __init__(self):
        super().__init__("AriamSeed", False)
        self.readable_name = "Ariam Seed"
        self.type = "farming"
        self.equippable = False
        self.description = "A brown seed from an Ariam Flower"
        self.result = ["AriamLeaf"]
        self.level = 2
        self.harvest_time = 2629746 #1 month

#Consumable
class MinorHealthPotion(Item):
    def __init__(self):
        super().__init__("MinorHealthPotion", False)
        self.readable_name = "Minor health potion"
        self.type = "consumable"
        self.equippable = False
        self.description = "A small vial of red fluid."

class AdralBrew(Item):
    def __init__(self):
        super().__init__("AdralBrew", False)
        self.readable_name = "Ad'ral Brew"
        self.type = "consumable"
        self.equippable = False
        self.description = "A vial of brown fluid, created by the elves."
        self.effect_description = "+1 perception, +1 strength"






# item_dict = {
#     "Longsword" : Longsword,
#     "BasementKey" : BasementKey,
#     "ChainHelmet" : ChainHelmet,
#     "ChainMail" : ChainMail,
#     "StuddedLegs" : StuddedLegs,
#     "LeatherBoots" : LeatherBoots
# }