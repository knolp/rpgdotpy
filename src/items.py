import abilities
import art
import random
import helper

# Materials


#items
class Item():
    """
        Base Class for items

        :bool usable                = If item i able to be used (#! Legacy)
        :string name                = Name of the class itself, used to store in JSON and !!IMPORTANTLY!! to retrieve items when loading character
        :bool consumable            = if item is consumable
        :string description         = Description of the item (visually) and/or lore about the item
        :string damage_type         = for melee weapons, which type of attack they do (slash, blunt, stab) etc
        :list art                   = list of rows (:string) with art, derived from rpgdotpy/art.py (defaults to 'not implemented')
        :string rarity              = Rarity of drops, ranging from common -> unique (#! currently no use)
        :int sell_price             = Vendor price for selling the item
        :int buy_price              = Vendor price for buying the item from a vendor (#! Legacy)
        :string effect_description  = Description of the effect of the item, what it does
        :string material            = Not implemented, probably going to be implemented for dismantling/crafting items #TODO
        :int dismember_chance       = Chance to chop of limbs, currently used in reverse in 100 - chance (so 95 == 5% chance)

        :bool dryable               = If (alchemy) item is able to be DRIED into other crafting materials
        :bool juicable              = If (alchemy) item is able to be JUICED into other crafting materials
        :list result                = list of item_class_names (:string) that is the result of above convertions
        :list stat_increase         = Stat increase on_equip in form of ["stat", <number>] 

    """
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
        self.material = False
        self.dismember_chance = 95
        self.stat_increase = False

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

    def effect(self, player, opponent, spell=False, weapon=False, on_damage_taken=False):
        return self.get_base_ret_dict()

    def get_base_ret_dict(self):
        """
            Init the base return dictionary for used in battle.py

            If not used, you will get KeyError when checking for armor-effects

            called in effect-function in items
        """
        return {
            "success" : False,
            "multiplier" : False,
            "additive" : False,
            "additive-base" : False,
            "combat_text" : False,
            "damage" : False,
            "convert" : False,
            "conditional-multiplier" : False,
            "conditional-additive" : False
        }

    def on_equip(self, player):
        if self.stat_increase:
            player.gear_stats[f"{self.stat_increase[0]}"] += self.stat_increase[1]
            return False
        else:
            return False

    def on_unequip(self, player):
        if self.stat_increase:
            player.gear_stats[f"{self.stat_increase[0]}"] -= self.stat_increase[1]
            return False
        else:
            return False

    def equip(self, state, player):
        """
            Equip items on the player and move currently equipped item to inventory
            And also update the text with what happened

            Also perform on_equip and on_unequip functions to see if things changed

            :param state: The state object containing everything about the game
            :param player: The player object containing everything about the player

            :return :tuple(:bool, :list)
                :bool = Indicates success or not (can't equip that item, etc.)
                :list = A list of strings to update information in inventory interface

        """
        translate_slots = {
            "right_hand" : "in the right hand",
            "left_hand" : "in the left hand",
            "head" : "",
            "legs" : "",
            "chest" : "",
            "ring" : "",
            "neck" : "on your neck",
            "boots" : ""
        } #For the output to inventory information console
        text = []
        if not self.equippable: #It does not have an equippable slot
            text.append("Item is not equippable")
            return False, text
        if self.equippable == "ring": #Since we have 2 rings slots we need to check which one to assign it to
            if not player.equipment["ring_1"]:
                player.equipment["ring_1"] = self
                text.append(f"[{self.readable_name}] equipped in right hand ring slot.")
                equip_text = self.on_equip(player)
                if equip_text:
                    for info in equip_text:
                        text.append(info)

                return True, text
            elif not player.equipment["ring_2"]:
                player.equipment["ring_2"] = self
                text.append(f"[{self.readable_name}] equipped in left hand ring slot.")
                equip_text = self.on_equip(player)
                if equip_text:
                    for info in equip_text:
                        text.append(info)
                return True, text
            else:
                left = helper.ring_select(state)
                if left == "no ring selected":
                    return False, [""]
                if not left:
                    current_item = player.equipment["ring_1"]
                    player.inventory.append(current_item)
                    player.equipment["ring_1"] = self
                    text.append(f"[{current_item.readable_name}] placed back into inventory.")
                    unequip_text = current_item.on_unequip(player)
                    if unequip_text:
                        for info in unequip_text:
                            text.append(info)
                    text.append(f"[{self.readable_name}] equipped equipped in right hand ring slot.")
                    equip_text = self.on_equip(player)
                    if equip_text:
                        for info in equip_text:
                            text.append(info)
                else:
                    current_item = player.equipment["ring_2"]
                    player.inventory.append(current_item)
                    player.equipment["ring_2"] = self
                    text.append(f"[{current_item.readable_name}] placed back into inventory.")
                    unequip_text = current_item.on_unequip(player)
                    if unequip_text:
                        for info in unequip_text:
                            text.append(info)
                    text.append(f"[{self.readable_name}] equipped equipped in left hand ring slot.")
                    equip_text = self.on_equip(player)
                    if equip_text:
                        for info in equip_text:
                            text.append(info)
                return True, text


            return False, text

        current_item = player.equipment[self.equippable]
        if current_item and current_item.name == self.name: #If we have the same item equipped, unnecessary to equip the same item again
            text.append("You already have one of these equipped.")
            return False, text
        if current_item: # Place the old weapon/armor back into inventory before overwriting the slot with the new one
            player.inventory.append(current_item)
            text.append(f"[{current_item.readable_name}] placed back into inventory.")
            unequip_text = current_item.on_unequip(player)
            if unequip_text:
                for info in unequip_text:
                    text.append(info)

        player.equipment[self.equippable] = self #Add item to player EQ
        text.append(f"[{self.readable_name}] equipped {translate_slots[self.equippable]}.")
        equip_text = self.on_equip(player)
        if equip_text:
            for info in equip_text:
                text.append(info)
        return True, text



#WEAPONS

class TrainingSword(Item):
    def __init__(self):
        super().__init__("TrainingSword", False)
        self.readable_name = "Training Sword"
        self.type = "weapon"
        self.subtype = "sword"
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
        self.subtype = "sword"
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
        self.subtype = "mace"
        self.equippable = "right_hand"
        self.attack = 2
        self.defence = 0
        self.description = "A mace made of iron, great for smashing."
        self.damage_type = "Blunt"
        self.effect_description = "Has a chance to cause stun."

    def effect(self, player, opponent):
        """
            Stuns the opponent for <stuns> turns
            Stun meaning it cannot perform actions
        """
        if opponent.player == True:
            readable_name = "you"
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
        self.subtype = "sword"
        self.equippable = "right_hand"
        self.attack = 2
        self.defence = 0
        self.description = "A pointy rapier."
        self.damage_type = "Stab"
        self.effect_description = "Has a chance to cause bleed."
        self.art = art.draw_Rapier()

    def effect(self, player, opponent):
        """
            Inflicts bleed to the opponent

            Bleed is derived from abilities.py
        """
        if opponent.player == True:
            opponent_readable_name = "you"
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
        self.subtype = "sword"
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
        self.subtype = "mace"
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
        self.subtype = "sword"
        self.equippable = "right_hand"
        self.attack = 1
        self.defence = 0
        self.description = "A blade flashing with color."
        self.damage_type = "Stab"
        self.rarity = "unique"
        self.effect_description = "Can inflict multiple status effects."

    def effect(self, player, opponent):
        if opponent.player == True:
            opponent_readable_name = "you"
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

    def on_unequip(self, player):
        return ["The world grows [darker]."]

#OFF_HANDS
class Buckler(Item):
    def __init__(self):
        super().__init__("Buckler", False)
        self.readable_name = "Buckler"
        self.type = "weapon"
        self.subtype = "shield"
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
        self.subtype = "catalyst"
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
        self.equippable = self.subtype = "head"
        self.attack = 0
        self.defence = 2
        self.description = "A hood made out of chainmail, quite heavy to wear."
        self.art = art.draw_ChainHelmet()
        self.rarity = "common"
        self.material = ""
        self.stat_increase = ["Strength", 5]
        self.magic_damage = 3
        self.effect_description = f"+{self.stat_increase[1]} {self.stat_increase[0]}"

class WizardHat(Item):
    def __init__(self):
        super().__init__("WizardHat", False)
        self.readable_name = "Wizard Hat"
        self.type = "armor"
        self.equippable = self.subtype = "head"
        self.attack = 0
        self.defence = 0
        self.description = "A pointy blue wizard hat, a perfect headwear for a magic apprentice!"
        #self.art = art.draw_ChainHelmet()
        self.rarity = "common"
        self.material = ""
        self.stat_increase = ["Intelligence", 5]
        self.magic_damage = 3
        self.effect_description = f"+{self.stat_increase[1]} {self.stat_increase[0]}, +{self.magic_damage} base damage to all spells."

    def effect(self, player, opponent, spell=False, Melee=False, on_damage_taken=False):
        _ret_dict = self.get_base_ret_dict()
        if not spell:
            _ret_dict["success"] = False
        
        else:
            _ret_dict["success"] = True
            _ret_dict["additive"] = self.magic_damage

        return _ret_dict


#CHEST

class ChainMail(Item):
    def __init__(self):
        super().__init__("ChainMail", False)
        self.readable_name = "Chain Mail"
        self.type = "armor"
        self.equippable = self.subtype = "chest"
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
        self.equippable = self.subtype = "legs"
        self.attack = 0
        self.defence = 2
        self.description = "Leather legs reinforced with iron studs."
        self.rarity = "epic"
        self.material = "leather"

#BOOTS

class LeatherBoots(Item):
    def __init__(self):
        super().__init__("LeatherBoots", False)
        self.readable_name = "Leather Boots"
        self.type = "armor"
        self.equippable = self.subtype = "boots"
        self.attack = 0
        self.defence = 1
        self.description = "Boots made out of cheap leather."
        self.art = art.draw_LeatherBoots()
        self.rarity = "legendary"

# NECKLACES

class RatFangNecklace(Item):
    def __init__(self):
        super().__init__("RatFangNecklace", False)
        self.readable_name = "Ratfang Necklace"
        self.type = "armor"
        self.equippable = self.subtype = "neck"
        self.attack = 0
        self.defence = 0
        self.description = "A \"necklace\" made out of a large rat fang."
        self.art = art.draw_RatFangNecklace()
        self.rarity = "unique"

# Rings

class TopazRing(Item):
    def __init__(self):
        super().__init__("TopazRing", False)
        self.readable_name = "Topaz Ring"
        self.type = "armor"
        self.equippable = self.subtype = "ring"
        self.attack = 0
        self.defence = 0
        self.description = "A small iron ring with a topaz attached to it."
        self.rarity = "rare"
        self.effect_description = "30% increased fire damage and converts all spell damage to Fire."

    def effect(self, player, opponent, spell=False, Melee=False, on_damage_taken=False):
        _ret_dict = self.get_base_ret_dict()
        if not spell:
            _ret_dict["success"] = False
        
        else:
                _ret_dict["success"] = True
                _ret_dict["conditional-multiplier"] = ["fire", 1.3]
                _ret_dict["convert"] = "fire"

        return _ret_dict


class SilverRing(Item):
    def __init__(self):
        super().__init__("SilverRing", False)
        self.readable_name = "Silver Ring"
        self.type = "armor"
        self.equippable = self.subtype = "ring"
        self.attack = 2
        self.defence = 0
        self.description = "A silver ring with a worn out engravement on it."
        self.rarity = "rare"
        self.effect_description = "Boosts attack."

    def effect(self, player, opponent, spell=False, Melee=False, on_damage_taken=False):
        return {
            "success" : False
        }

class RingOfThorns(Item):
    def __init__(self):
        super().__init__("RingOfThorns", False)
        self.readable_name = "Ring of Thorns"
        self.type = "armor"
        self.equippable = self.subtype = "ring"
        self.attack = 0
        self.defence = 0
        self.description = "An elven ring of wood sprouting sharp thorns."
        self.rarity = "rare"
        self.effect_description = "Reflects damage back to attackers (based on Strength)."

    def effect(self, player, opponent, spell=False, Melee=False, on_damage_taken=False):
        _ret_dict = self.get_base_ret_dict()
        if not on_damage_taken:
            _ret_dict["success"] = False
        else:
            _ret_dict["success"] = True
            reflect_damage = max(int(player.stats["Strength"] / 4), 2)
            _ret_dict["damage"] = reflect_damage
            _ret_dict["combat_text"] = [f"{self.readable_name} reflects {reflect_damage} damage back to {opponent.readable_name}"]

        return _ret_dict

    def on_equip(self, player):
        player.health -= 2
        return ["The ring cuts you as you equip it, dealing [2] damage."]

class BandOfDarkness(Item):
    def __init__(self):
        super().__init__("BandOfDarkness", False)
        self.readable_name = "Band of Darkness"
        self.type = "armor"
        self.equippable = self.subtype = "ring"
        self.attack = 0
        self.defence = 0
        self.description = "A dark, polished metal ring."
        self.rarity = "rare"
        self.effect_description = "Converts spell damage to [Occult] damage."

    def effect(self, player, opponent, spell=False, Melee=False, on_damage_taken=False):
        _ret_dict = self.get_base_ret_dict()
        if not spell:
            _ret_dict["success"] = False
        else:
            _ret_dict["success"] = True
            _ret_dict["convert"] = "occult"

        return _ret_dict





# Key Items
class BasementKey(Item):
    def __init__(self):
        super().__init__("BasementKey", False)
        self.readable_name = "Basement Key (Osk'Ghar)"
        self.type = "key"
        self.subtype = "key"
        self.equippable = False
        self.description = "Unlocks the basement door at Osk'Ghar."
        self.art = art.draw_key()
        for i in range(len(self.art)):
            self.art[i] = self.art[i][::-1]

class DungeonKeyHaunted(Item):
    def __init__(self):
        super().__init__("DungeonKeyHaunted", False)
        self.readable_name = "Dungeon key (Haunted House)"
        self.type = "key"
        self.subtype = "key"
        self.equippable = False
        self.description = "Unlocks a dungeon door somewhere."
        self.art = art.draw_key()[::-1]

class Shovel(Item):
    def __init__(self):
        super().__init__("Shovel", False)
        self.readable_name = "Shovel"
        self.type = "key"
        self.subtype = "tool"
        self.equippable = False
        self.description = "Good for digging."

class StarterTownHouseKey(Item):
    def __init__(self):
        super().__init__("StarterTownHouseKey", False)
        self.readable_name = "House Key (Starter Town)"
        self.type = "key"
        self.subtype = "key"
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
        self.subtype = "flora"
        self.equippable = False
        self.description = "A cloudy, white berry. Smells atrocious."
        self.juicable = True
        self.result = ["DeverBerryJuice", "DeverBerrySkin"]

class DeverBerryJuice(Item):
    def __init__(self):
        super().__init__("DeverBerryJuice", False)
        self.readable_name = "Deverberry Juice"
        self.type = "crafting"
        self.subtype = "flora"
        self.equippable = False
        self.description = "A hideous smelling juice made from Deverberries"

class DeverBerrySkin(Item):
    def __init__(self):
        super().__init__("DeverBerrySkin", False)
        self.readable_name = "Deverberry Skin"
        self.type = "crafting"
        self.subtype = "flora"
        self.equippable = False
        self.description = "Probably has a better smell when dried."
        self.dryable = True
        self.result = ["DeverBerrySkinDried"]

class DeverBerrySkinDried(Item):
    def __init__(self):
        super().__init__("DeverBerrySkinDried", False)
        self.readable_name = "Deverberry Skin (Dried)"
        self.type = "crafting"
        self.subtype = "flora"
        self.equippable = False
        self.description = "Leathery skin of a dried deverberry."

class BarburaLeaf(Item):
    def __init__(self):
        super().__init__("BarburaLeaf", False)
        self.readable_name = "Barbura Leaf"
        self.type = "crafting"
        self.subtype = "flora"
        self.equippable = False
        self.description = "Yellow leaf picked from a Barbura bush."
        self.dryable = True
        self.result = ["BarburaLeafDried"]

class BarburaLeafDried(Item):
    def __init__(self):
        super().__init__("BarburaLeafDried", False)
        self.readable_name = "Barbura Leaf (Dried)"
        self.type = "crafting"
        self.subtype = "flora"
        self.equippable = False
        self.description = "A crunchy, sweet smelling leaf."

class AriamLeaf(Item):
    def __init__(self):
        super().__init__("AriamLeaf", False)
        self.readable_name = "Ariam Leaf"
        self.type = "crafting"
        self.subtype = "flora"
        self.equippable = False
        self.description = "An orange leaf from an Ariam plant."
        self.dryable = True
        self.result = ["AriamLeafDried"]

class AriamLeafDried(Item):
    def __init__(self):
        super().__init__("AriamLeafDried", False)
        self.readable_name = "Ariam Leaf (Dried)"
        self.type = "crafting"
        self.subtype = "flora"
        self.equippable = False
        self.description = "A crunchy, faded orange leaf."

class ButterflyWing(Item):
    def __init__(self):
        super().__init__("ButterflyWing", False)
        self.readable_name = "Butterfly Wing"
        self.type = "crafting"
        self.subtype = "misc"
        self.equippable = False
        self.description = "A shimmering wing."

class ArcaneDust(Item):
    def __init__(self):
        super().__init__("ArcaneDust", False)
        self.readable_name = "Arcane Dust"
        self.type = "crafting"
        self.subtype = "magical"
        self.equippable = False
        self.description = "A bottle containing a flowing sand-like material."

class TrollHair(Item):
    def __init__(self):
        super().__init__("TrollHair", False)
        self.readable_name = "Troll Hair"
        self.type = "crafting"
        self.subtype = "creature"
        self.equippable = False
        self.description = "A bunch of troll hairs tied together."

class DesertSalt(Item):
    def __init__(self):
        super().__init__("DesertSalt", False)
        self.readable_name = "Desert Salt"
        self.type = "crafting"
        self.subtype = "misc"
        self.equippable = False
        self.description = "A bottle of salt with the brand 'HMC', mined in the eastern desert."

class ObsidianShard(Item):
    def __init__(self):
        super().__init__("ObsidianShard", False)
        self.readable_name = "Obsidian Shard"
        self.type = "crafting"
        self.subtype = "metal"
        self.equippable = False
        self.description = "A shard of pure black obsidian from the eastern desert."


#Seeds
class BarburaSeed(Item):
    def __init__(self):
        super().__init__("BarburaSeed", False)
        self.readable_name = "Barbura Seed"
        self.type = "farming"
        self.subtype = "seed"
        self.equippable = False
        self.description = "A small green seed."
        self.result = ["BarburaLeaf"]
        self.level = 1
        self.harvest_time = 1209600 # 2 weeks

class AriamSeed(Item):
    def __init__(self):
        super().__init__("AriamSeed", False)
        self.readable_name = "Ariam Seed"
        self.type = "farming"
        self.subtype = "seed"
        self.equippable = False
        self.description = "A brown seed from an Ariam Flower"
        self.result = ["AriamLeaf"]
        self.level = 2
        self.harvest_time = 2629746 # 1 month

class DeverSeed(Item):
    def __init__(self):
        super().__init__("DeverSeed", False)
        self.readable_name = "Dever Seed"
        self.type = "farming"
        self.subtype = "seed"
        self.equippable = False
        self.description = "A dark black seed from a deverberry bush"
        self.result = ["DeverBerry"]
        self.level = 2
        self.harvest_time = 2629746 * 3 # 3 months

class FirebloomSeed(Item):
    def __init__(self):
        super().__init__("FirebloomSeed", False)
        self.readable_name = "Firebloom Seed"
        self.type = "farming"
        self.subtype = "seed"
        self.equippable = False
        self.description = "A glowing, bright orange seed."
        self.result = ["DeverBerry"]
        self.level = 2
        self.harvest_time = 2629746 / 2 # 2 weeks

#Consumable
# Can only affect players themselves, consume-function will be passed the state.player parameter
class MinorHealthPotion(Item):
    def __init__(self):
        super().__init__("MinorHealthPotion", False)
        self.readable_name = "Minor health potion"
        self.type = "consumable"
        self.subtype = "potion"
        self.equippable = False
        self.description = "A small vial of red fluid."
        self.healing = 10
        self.effect_description = f"+{self.healing} HP"

    def consume(self, player):
        healed = self.healing
        if player.health == player.max_health:
            return False, "You are already at full health"
        if player.health + healed > player.max_health:
            healed = player.max_health - player.health
        player.health += healed
        
        return True, f"You consumed a [{self.readable_name}], it healed for {healed}"

class AdralBrew(Item):
    def __init__(self):
        super().__init__("AdralBrew", False)
        self.readable_name = "Ad'ral Brew"
        self.type = "consumable"
        self.subtype = "brew"
        self.equippable = False
        self.increase = 4
        self.stat = "Strength"
        self.turns = 600
        self.description = "A vial of brown fluid, created by the elves."
        self.effect_description = f"+{self.increase} {self.stat}"

    def consume(self, player):
        for item in player.status_effects:
            if item.name == "StatBuff":
                if item.origin == "AdralBrew":
                    if item.turns_left > 100:
                        return False, "You are already affected by this brew."
                    else:
                        player.status_effects.append(abilities.StatBuff(self.turns, self.stat, self.increase, player, origin="AdralBrew"))
                        return True, f"You refreshed your [{self.readable_name}], reseting it to {self.turns} turns."
        player.status_effects.append(abilities.StatBuff(self.turns, self.stat, self.increase, player, origin="AdralBrew"))
        return True, f"You consumed an [{self.readable_name}], it increases your {self.stat} by {self.increase} for {self.turns} turns."






# item_dict = {
#     "Longsword" : Longsword,
#     "BasementKey" : BasementKey,
#     "ChainHelmet" : ChainHelmet,
#     "ChainMail" : ChainMail,
#     "StuddedLegs" : StuddedLegs,
#     "LeatherBoots" : LeatherBoots
# }