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

    def effect(self, player, opponent):
        if random.randint(1,100) > 50:
            list_of_effects = [effect.type for effect in opponent.status_effects]
            if "Stun" not in list_of_effects:
                opponent.status_effects.append(abilities.Stun(2, opponent.readable_name))
                return {
                    "combat_text" : [
                        "{}'s heavy weight knocks {} to the ground".format(self.readable_name, opponent.readable_name),
                        "causing {} to be stunned".format(opponent.readable_name)] 
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
        self.art = art.draw_Rapier()

    def effect(self, player, opponent):
        if "Bleed" in opponent.immune:
            return {
                "combat_text" : False
            }
        if random.randint(1,100) > 70:
            list_of_effects = [effect.type for effect in opponent.status_effects]
            if "Bleed" not in list_of_effects:
                opponent.status_effects.append(abilities.Bleed(5, 2, opponent.readable_name))
                return {
                    "combat_text" : [
                        "{}'s pointy tip makes a deep wound".format(self.readable_name),
                        "and causes {} to bleed.".format(opponent.readable_name)] 
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

    def modifier(self, player, opponent):
        if opponent.race == "Rat":
            return 2
        else:
            return False

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







#Crafting Material
class DeverBerry(Item):
    def __init__(self):
        super().__init__("DeverBerry", False)
        self.readable_name = "Deverberry"
        self.type = "crafting"
        self.equippable = False
        self.description = "A cloudy, white berry. Smells atrocious."

#Consumable
class MinorHealthPotion(Item):
    def __init__(self):
        super()._init__("MinorHealthPotion", False)
        self.readable_name = "Minor health potion"
        self.type = "consumable"
        self.equippable = False
        self.description = "A small vial of red fluid."






# item_dict = {
#     "Longsword" : Longsword,
#     "BasementKey" : BasementKey,
#     "ChainHelmet" : ChainHelmet,
#     "ChainMail" : ChainMail,
#     "StuddedLegs" : StuddedLegs,
#     "LeatherBoots" : LeatherBoots
# }