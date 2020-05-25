import random
import helper

class Ability():
    def __init__(self, name):
        self.name = name
        self.aoe = False
        self.no_direct_damage = False
    
    def execute(self, player, opponent, state):
        pass





#Spells

#  ______ _____ _____  ______ 
# |  ____|_   _|  __ \|  ____|
# | |__    | | | |__) | |__   
# |  __|   | | |  _  /|  __|  
# | |     _| |_| | \ \| |____ 
# |_|    |_____|_|  \_\______|
                             
class Fireball(Ability):
    def __init__(self):
        super().__init__("Fireball")
        self.readable_name = "Fireball"
        self.description = "Conjures a ball of fire, ready to throw at any foe."
        self.damage_type = "fire"
        self.damage = 5

    def execute(self, player, opponent, state):
        if not opponent.player:
            combat_text = []
            combat_variables = [
                "hurls a big fireball towards",
                "conjures a great ball of fire and throws it towards",
                "casts a fireball at"
            ]
            damage_done = random.randint(int(0.75 * self.damage), self.damage)
            combat_text.append("{} {} {}".format(player.name, random.choice(combat_variables), opponent.readable_name))
    
            return {
                "damage" : damage_done,
                "combat_text" : combat_text
            }

class GreatFireball(Ability):
    def __init__(self):
        super().__init__("GreatFireball")
        self.readable_name = "Great Fireball"
        self.description = "Conjures a great ball of fire, damaging a great area."
        self.damage_type = "fire"
        self.damage = 3
        self.aoe = 3

    def execute(self, player, opponent, state):
        if not opponent.player:
            combat_text = []
            combat_variables = [
                "hurls a big fireball towards",
                "conjures a great ball of fire and throws it towards",
                "casts a fireball at"
            ]
            damage_done = random.randint(int(0.75 * self.damage), self.damage)
            combat_text.append("{} {} {}".format(player.name, random.choice(combat_variables), opponent.readable_name))
    
            return {
                "damage" : damage_done,
                "combat_text" : combat_text
            }


class Scorch(Ability):
    def __init__(self):
        super().__init__("Scorch")
        self.readable_name = "Scorch"
        self.description = "Ignites the target and causes it to burn for 5 turns"
        self.damage_type = "fire"
        self.no_direct_damage = True

    def execute(self, player, opponent, state):
        combat_text = []
        combat_variables_success = [
            "{} ignites {}, causing {} to burn".format(player.name,opponent.readable_name, opponent.readable_name),
            "{} sets {} ablaze, causing {} to be on fire".format(player.name, opponent.readable_name, opponent.readable_name)
        ]
        combat_variables_failure = [
            "tries to ignite {}, but {} is already burning".format(opponent.readable_name, opponent.readable_name),
            "tries to set {} ablaze, but {} is already on fire".format(opponent.readable_name, opponent.readable_name)
        ]

        list_of_effects = [effect.type for effect in opponent.status_effects]

        if "Burn" in list_of_effects:
            combat_text.append(random.choice(combat_variables_failure))

            return {
                "damage" : 0,
                "combat_text" : combat_text
            }
        
        else:
            combat_text.append(random.choice(combat_variables_success))
            opponent.status_effects.append(Burn(5,1,opponent.name))

            return {
                "damage" : 0,
                "combat_text" : combat_text
            }




#   ____   _____ _____ _    _ _   _______ 
#  / __ \ / ____/ ____| |  | | | |__   __|
# | |  | | |   | |    | |  | | |    | |   
# | |  | | |   | |    | |  | | |    | |   
# | |__| | |___| |____| |__| | |____| |   
#  \____/ \_____\_____|\____/|______|_|   
                                         



class LifeBolt(Ability):
    def __init__(self):
        super().__init__("LifeBolt")
        self.readable_name = "Lifedraining Bolt"
        self.description = "Shoots out a bolt that can drain life from your opponent."
        self.damage_type = "occult"
        self.damage = 15

    
    def execute(self, player, opponent, state):
        combat_text = []
        combat_variables = [
            "summons a bolt from the hands and shoots it towards",
            "sends a bolt of dark energy towards",
            "shoots a dark bolt towards"
        ]
        damage_done = random.randint(int(0.75 * self.damage), self.damage)
        heal_done = int(damage_done / 10)
        combat_text.append("{} {} {}".format(player.name, random.choice(combat_variables), opponent.readable_name))
        if player.health + heal_done < player.max_health:
            player.health += heal_done
            combat_text.append("You drain {} health from the attack.".format(heal_done))
        else:
            player.health = player.max_health
            combat_text.append("You drain {} health from the attack.".format(player.max_health - player.health))

        return {
            "damage" : damage_done,
            "combat_text" : combat_text
        }


#           _____   _____          _   _ ______ 
#     /\   |  __ \ / ____|   /\   | \ | |  ____|
#    /  \  | |__) | |       /  \  |  \| | |__   
#   / /\ \ |  _  /| |      / /\ \ | . ` |  __|  
#  / ____ \| | \ \| |____ / ____ \| |\  | |____ 
# /_/    \_\_|  \_\\_____/_/    \_\_| \_|______|



 # ______ _____   ____   _____ _______ 
 #|  ____|  __ \ / __ \ / ____|__   __|
 #| |__  | |__) | |  | | (___    | |   
 #|  __| |  _  /| |  | |\___ \   | |   
 #| |    | | \ \| |__| |____) |  | |   
 #|_|    |_|  \_\\____/|_____/   |_| 
 

 
 #  _   _       _______ _    _ _____  ______ 
 #| \ | |   /\|__   __| |  | |  __ \|  ____|
 #|  \| |  /  \  | |  | |  | | |__) | |__   
 #| . ` | / /\ \ | |  | |  | |  _  /|  __|  
 #| |\  |/ ____ \| |  | |__| | | \ \| |____ 
 #|_| \_/_/    \_\_|   \____/|_|  \_\______|
 

class Infest(Ability):
    def __init__(self):
        super().__init__("Infest")
        self.readable_name = "Infest"
        self.description = "Plants a seed in the target, which burst out after a few turns dealing damage."
        self.damage_type = "nature"
        self.damage = 15

    
    def execute(self, player, opponent, state):
        if len([x for x in player.inventory if x.subtype == "seed"]):
            seed = helper.pick_seed(state)
        else:
            helper.popup(state.stdscr, state, ["No seeds available"])
            return {
                "damage" : "back"
            }
        combat_text = []
        combat_variables = [
            f"{player.name} plants a seed in {opponent.readable_name}",
            f"{player.name} infests {opponent.name} with a {seed}",
        ]
        combat_text.append(random.choice(combat_variables))
        if seed == "Barbura Seed":
            combat_variables_failure = [f"{opponent.readable_name} is already infested."]
            list_of_effects = [effect.type for effect in opponent.status_effects]
            if "Infested" in list_of_effects:
                combat_text.append(random.choice(combat_variables_failure))

                return {
                    "damage" : 0,
                    "combat_text" : combat_text
                }
            else:
                damage_done = random.randint(int(0.75 * self.damage), self.damage)
                combat_text.append("It ruptures immediately")
                for item in player.inventory:
                    if item.readable_name == seed:
                        player.inventory.pop(player.inventory.index(item))
                        break
        
        if seed == "Ariam Seed":
            damage = player.stats["Intelligence"] * 2
            combat_variables_failure = [f"{opponent.readable_name} is already infested."]
            list_of_effects = [effect.type for effect in opponent.status_effects]

            if "Infested" in list_of_effects:
                combat_text.append(random.choice(combat_variables_failure))

                return {
                    "damage" : 0,
                    "combat_text" : combat_text
                }
            
            else:
                opponent.status_effects.append(InfestAriamSeed(5,damage,opponent))
                for item in player.inventory:
                    if item.readable_name == seed:
                        player.inventory.pop(player.inventory.index(item))
                        break

                return {
                    "damage" : 0,
                    "combat_text" : combat_text
                }
        
        if seed == "Dever Seed":
            damage = int(player.stats["Intelligence"] / 2)
            combat_variables_failure = [f"{opponent.readable_name} is already infested."]
            list_of_effects = [effect.type for effect in opponent.status_effects]
            self.no_direct_damage = True

            if "Infested" in list_of_effects:
                combat_text.append(random.choice(combat_variables_failure))

                return {
                    "damage" : 0,
                    "combat_text" : combat_text
                }
            
            else:
                opponent.status_effects.append(InfestDeverSeed(5,damage,opponent))
                for item in player.inventory:
                    if item.readable_name == seed:
                        player.inventory.pop(player.inventory.index(item))
                        break


                return {
                    "damage" : 0,
                    "combat_text" : combat_text
                }

        if seed == "Firebloom Seed":
            damage = int(player.stats["Intelligence"] / 2)
            combat_variables_failure = [f"{opponent.readable_name} is already infested."]
            list_of_effects = [effect.type for effect in opponent.status_effects]
            self.no_direct_damage = True

            if "Infested" in list_of_effects:
                combat_text.append(random.choice(combat_variables_failure))

                return {
                    "damage" : 0,
                    "combat_text" : combat_text
                }
            
            else:
                opponent.status_effects.append(InfestFirebloomSeed(5,damage,opponent))
                for item in player.inventory:
                    if item.readable_name == seed:
                        player.inventory.pop(player.inventory.index(item))
                        break


                return {
                    "damage" : 0,
                    "combat_text" : combat_text
                }
        
        return {
            "damage" : 0,
            "combat_text" : combat_text
        }

class WoodlandCharm(Ability):
    def __init__(self):
        super().__init__("WoodlandCharm")
        self.readable_name = "Woodland Charm"
        self.description = "Offer a sacrificial item to the woodland gods and gain power."
        self.damage_type = "Nature"
        self.damage = 0
        self.no_direct_damage = True

    
    def execute(self, player, opponent, state):
        charm = helper.select_charm(state)
        if not charm:
            helper.popup(state.stdscr, state, ["No charms available"])
            return {
                "damage" : "back"
            }
        combat_text = []
        combat_variables = [
            f"sacrifices a {charm} to make a woodland charm"
        ]
        combat_text.append("{} {}".format(player.name, random.choice(combat_variables)))

        if charm == "Deverberry Skin":
            for item in player.status_effects:
                if item.name == "StatBuff":
                    if item.origin == "WoodlandDeverberrySkin":
                        return {
                            "damage" : self.damage,
                            "combat_text" : ["This buff is already applied"]
                        }
            player.status_effects.append(WoodlandDeverberrySkin(5, player))
            player.status_effects.append(StatBuff(5, "Strength", player.stats["Strength"], player, origin="WoodlandDeverberrySkin"))

        if charm == "Desert Salt":
            for item in player.status_effects:
                if item.name == "WoodlandDesertSalt":
                    return {
                        "damage" : self.damage,
                        "combat_text" : ["This buff is already applied"]
                    }
            player.status_effects.append(WoodlandDesertSalt(5, player))

        return {
            "damage" : self.damage,
            "combat_text" : combat_text
        }

#   ______ _______ _    _ ______ _____  ______          _      
# |  ____|__   __| |  | |  ____|  __ \|  ____|   /\   | |     
# | |__     | |  | |__| | |__  | |__) | |__     /  \  | |     
# |  __|    | |  |  __  |  __| |  _  /|  __|   / /\ \ | |     
# | |____   | |  | |  | | |____| | \ \| |____ / ____ \| |____ 
# |______|  |_|  |_|  |_|______|_|  \_\______/_/    \_\______


class StatusEffect():
    def __init__(self):
        self.damage_type = "normal"

#DEBUFFS
class Bleed(StatusEffect):
    def __init__(self, turns, damage, opponent_name):
        super().__init__()
        self.type = self.name = "Bleed"
        self.color = 133
        self.max_turn = turns + 1
        self.turns_left = turns + 1
        self.damage = damage
        self.opponent_name = opponent_name
        self.combat_text = "{} is bleeding and suffers {} from bloodloss.".format(self.opponent_name, self.damage)
        self.combat_text_over = "{} is no longer bleeding.".format(self.opponent_name)

    def execute(self):
        self.turns_left -= 1
        if self.turns_left == 0:
            return {
                "combat_text" : self.combat_text_over,
                "done" : True,
                "damage" : False
            }
        else:
            return {
                "combat_text" : self.combat_text,
                "done" : False,
                "damage" : self.damage
            }

class Stun(StatusEffect):
    def __init__(self, turns, opponent_name):
        super().__init__()
        self.type = self.name = "Stun"
        self.color = 133
        self.max_turn = turns + 1
        self.turns_left = turns + 1
        self.opponent_name = opponent_name
        if opponent_name == "you":
            self.combat_text = "{} are stunned and unable to respond.".format(self.opponent_name).capitalize()
            self.combat_text_over = "{} are no longer stunned.".format(self.opponent_name).capitalize()
        else:
            self.combat_text = "{} is stunned and unable to respond.".format(self.opponent_name).capitalize()
            self.combat_text_over = "{} is no longer stunned.".format(self.opponent_name).capitalize()

    def execute(self):
        self.turns_left -= 1
        if self.turns_left == 0:
            return {
                "combat_text" : self.combat_text_over,
                "done" : True,
                "damage" : False
            }
        else:
            return {
                "combat_text" : self.combat_text,
                "done" : False,
                "damage" : 0
            }


class Burn(StatusEffect):
    def __init__(self, turns, damage, opponent_name):
        super().__init__()
        self.type = self.name = "Burn"
        self.color = 133
        self.max_turn = turns + 1
        self.turns_left = turns + 1
        self.damage = damage
        self.opponent_name = opponent_name
        self.combat_text = "{} is burning and takes {} damage.".format(self.opponent_name, self.damage)
        self.combat_text_over = "{} is no longer burning.".format(self.opponent_name)

    def execute(self):
        self.turns_left -= 1
        if self.turns_left == 0:
            return {
                "combat_text" : self.combat_text_over,
                "done" : True,
                "damage" : False
            }
        else:
            return {
                "combat_text" : self.combat_text,
                "done" : False,
                "damage" : self.damage
            }


class Chill(StatusEffect):
    def __init__(self, turns, damage, opponent_name):
        super().__init__()
        self.type = self.name = "Chill"
        self.color = 133
        self.max_turn = turns + 1
        self.turns_left = turns + 1
        self.damage = damage
        self.opponent_name = opponent_name
        self.combat_text = "{} is chilled and takes {} more damage from frost abilities.".format(self.opponent_name, self.damage)
        self.combat_text_over = "{} is no longer chilled".format(self.opponent_name)

    def execute(self):
        self.turns_left -= 1
        if self.turns_left == 0:
            return {
                "combat_text" : self.combat_text_over,
                "done" : True,
                "damage" : False
            }
        else:
            return {
                "combat_text" : self.combat_text,
                "done" : False,
                "damage" : 0
            }

# Infest Debuffs
class InfestAriamSeed(StatusEffect):
    def __init__(self, turns, damage, opponent):
        super().__init__()
        self.type = "Infested"
        self.name = "InfestAriamSeed"
        self.color = 133
        self.max_turn = turns + 1
        self.turns_left = turns + 1
        self.damage = damage
        self.healing = int(damage / 2)
        self.opponent = opponent
        self.opponent_name = opponent.name
        self.combat_text = "{} is still infested with a seed.".format(self.opponent_name)
        self.combat_text_over = "{}'s infestation bursts, dealing {} (Nature) damage and healing for {}.".format(self.opponent_name, self.damage, self.healing)

    def execute(self):
        self.turns_left -= 1
        if self.turns_left == 0:
            return {
                "combat_text" : self.combat_text_over,
                "done" : True,
                "damage" : self.damage,
                "heal-player" : 3
            }
        else:
            return {
                "combat_text" : False,
                "done" : False,
                "damage" : 0
            }

class InfestDeverSeed(StatusEffect):
    def __init__(self, turns, damage, opponent):
        super().__init__()
        self.type = "Infested"
        self.name = "InfestDeverSeed"
        self.color = 133
        self.max_turn = turns + 1
        self.turns_left = turns + 1
        self.damage = damage
        self.opponent = opponent
        self.opponent_name = opponent.name
        self.combat_text = "The infestation rots {} from the inside, dealing {} (Occult) damage.".format(self.opponent_name, self.damage)
        self.combat_text_over = "{}'s infestation has withered away.".format(self.opponent_name, self.damage)

    def execute(self):
        self.turns_left -= 1
        if self.turns_left == 0:
            return {
                "combat_text" : self.combat_text_over,
                "done" : True,
                "damage" : False
            }
        else:
            return {
                "combat_text" : self.combat_text,
                "done" : False,
                "damage": self.damage
            }

class InfestFirebloomSeed(StatusEffect):
    def __init__(self, turns, damage, opponent):
        super().__init__()
        self.type = "Infested"
        self.name = "InfestFirebloomSeed"
        self.color = 133
        self.max_turn = turns + 1
        self.turns_left = turns + 1
        self.damage = damage
        self.opponent = opponent
        self.opponent_name = opponent.name
        self.combat_text = "{} is still infested with a seed.".format(self.opponent_name)
        self.combat_text_over = "{}'s infestation bursts, dealing {} (Fire) damage and causing Burn".format(self.opponent_name, self.damage)

    def execute(self):
        self.turns_left -= 1
        if self.turns_left == 0:
            self.opponent.status_effects.append(Burn(5,1,self.opponent_name))
            return {
                "combat_text" : self.combat_text_over,
                "done" : True,
                "damage" : self.damage,
            }
        else:
            return {
                "combat_text" : False,
                "done" : False,
                "damage" : 0
            }
                
#WoodlandCharm Buffs
class WoodlandDeverberrySkin(StatusEffect):
    def __init__(self, turns, opponent):
        super().__init__()
        self.type = "Woodland"
        self.name = "WoodlandDeverberrySkin"
        self.color = 133
        self.max_turn = turns + 1
        self.turns_left = turns + 1
        self.opponent = opponent
        self.opponent_name = opponent.name
        self.combat_text = "{} succumbs to inner rage, losing all control.".format(self.opponent_name)
        self.combat_text_over = "{} has finally come back to reality.".format(self.opponent_name)

        self.opponent.in_control = False

    def execute(self):
        self.turns_left -= 1
        if self.max_turn == self.turns_left -1:
            return {
                "combat_text" : combat_text,
                "done" : False,
                "damage" : 0
            }
        if self.turns_left == 0:
            self.opponent.in_control = True
            return {
                "combat_text" : self.combat_text_over,
                "done" : True,
                "damage" : 0,
            }
        else:
            return {
                "combat_text" : False,
                "done" : False,
                "damage" : 0
            }

class WoodlandDesertSalt(StatusEffect):
    def __init__(self, turns, opponent):
        super().__init__()
        self.type = "Woodland"
        self.name = "WoodlandDesertSalt"
        self.color = 133
        self.max_turn = turns + 1
        self.turns_left = turns + 1
        self.opponent = opponent
        self.opponent_name = opponent.name
        self.combat_text_begin = "{}'s skin grows sharp spikes of salt.".format(self.opponent_name)
        self.combat_text = "OPPONENT takes DAMAGE damage in recoil."
        self.combat_text_over = "{}'s saltspikes shatter.'".format(self.opponent_name)

        self.damage_type = "recoil"
        self.damage = opponent.stats["Strength"]

    def execute(self):
        self.turns_left -= 1
        if self.max_turn == self.turns_left -1:
            return {
                "combat_text" : combat_text_begin,
                "done" : False,
                "damage" : 0
            }
        if self.turns_left == 0:
            return {
                "combat_text" : self.combat_text_over,
                "done" : True,
                "damage" : 0,
            }
        else:
            return {
                "combat_text" : self.combat_text,
                "done" : False,
                "damage" : random.randint(1, self.damage)
            }

#Molten Strike Buff
class MoltenStrikeBuff(StatusEffect):
    def __init__(self, turns, opponent_name):
        super().__init__()
        self.type = self.name = "MoltenStrikeBuff"
        self.damage_type = "enhance_melee_hit"
        self.color = 133
        self.max_turn = turns + 1
        self.turns_left = turns + 1
        self.opponent_name = opponent_name
        if opponent_name == "you":
            self.combat_text = "{}r hands glow red, enhancing your melee hits.".format(self.opponent_name).capitalize()
            self.combat_text_over = "{}r hands are no longer glowing.".format(self.opponent_name).capitalize()
        else:
            self.combat_text = "{}'s hands glow red.".format(self.opponent_name).capitalize()
            self.combat_text_over = "{}'s hands are no longer glowing red".format(self.opponent_name).capitalize()

    def execute(self, opponent):
        self.turns_left -= 1
        if self.turns_left == 0:
            return {
                "combat_text" : self.combat_text_over,
                "done" : True,
                "damage" : False
            }
        else:
            return {
                "combat_text" : self.combat_text,
                "done" : False,
                "damage" : random.randint(1, 4)
            }

class StatBuff(StatusEffect):
    def __init__(self, turns, stat, increase, player, origin=False):
        """
            Increases <stat> by <increase> for <turn> turns.
            
            :string name =                  Name of the class
            :string readable_name =         Readable syntax of buff name
            :string description =           Description of what it does
            :string combat_text =           Currently unused #!
            :string combat_text_over =      Message when it ends
            :string type =                  What type it belongs to: t.ex Buff, Debuff
            :int color =                    Color of the message in interface
            :string origin =                Where the buff came from, to make sure we are not applying multiple

            :int max_turn =                 Max turns this effect has
            :int turns_left =               Current turns left until expired

            :string stat =                  name of stat in player.stats t.ex "Strength", "Intelligence", "Agility"
            :int increase =                 The amount of increase, t.ex Adral Brew is +4 Strength
            :Player player =                The player object
        """
        super().__init__()
        self.name = "StatBuff"
        self.readable_name = f"Increased {stat}"
        self.description = "Increase stat"
        self.combat_text = False
        self.combat_text_over = f"{player.name}'s {self.readable_name} has worn off."
        self.type = "Buff"
        self.color = 134
        self.origin = origin

        self.max_turn = turns + 1
        self.turns_left = turns + 1

        self.stat = stat
        self.increase = increase
        self.player = player
        self.player.stats[stat] += increase


    def execute(self):
        self.turns_left -= 1
        if self.turns_left == 0:
            self.player.stats[self.stat] -= self.increase
            return {
                "combat_text" : self.combat_text_over,
                "done" : True,
                "damage" : False
            }
        else:
            return {
                "combat_text" : self.combat_text,
                "done" : False,
                "damage" : 0
            }




#Outerworld spells

class MindVision():
    def __init__(self):
        self.name = "MindVision"
        self.readable_name = "Mind Vision"
        self.description = "Feel the presence of enemies in the dark for a couple of turns."

    def execute(self, player):
        player.mindvision = player.stats["Intelligence"] + player.stats["Attunement"]

class PhaseShift():
    def __init__(self):
        self.name = "PhaseShift"
        self.readable_name = "Phase Shift"
        self.description = "Shift into the abstract realm, removing your physical body."
    
    def execute(self, player):
        if player.phaseshift == 0:
            player.phaseshift = player.stats["Intelligence"] + player.stats["Attunement"]
            if player.phaseshift > 9:
                player.phaseshift = 9
        else:
            player.phaseshift = 0


class Teleport():
    def __init__(self):
        self.name = "Teleport"
        self.readable_name = "Teleport"
        self.description = "Teleport a few steps in the direction you are facing."

    def execute(self, player):
        print("Must be implemented")


class HomeTeleport():
    def __init__(self):
        self.name = "HomeTeleport"
        self.readable_name = "Home Teleport"
        self.description = "Teleport to your home."




