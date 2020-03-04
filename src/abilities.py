import random

class Ability():
    def __init__(self, name):
        self.name = name
        self.aoe = False
    
    def execute(self):
        pass





#Spells
class Fireball(Ability):
    def __init__(self):
        super().__init__("Fireball")
        self.readable_name = "Fireball"
        self.description = "Conjures a ball of fire, ready to throw at any foe."
        self.damage_type = "fire"

    def execute(self, player, opponent):
        if not opponent.player:
            combat_text = []
            combat_variables = [
                "hurls a big fireball towards",
                "conjures a great ball of fire and throws it towards",
                "casts a fireball at"
            ]
            damage_done = player.stats["Intelligence"]
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
        self.aoe = 4

    def execute(self, player, opponent):
        if not opponent.player:
            combat_text = []
            combat_variables = [
                "hurls a big fireball towards",
                "conjures a great ball of fire and throws it towards",
                "casts a fireball at"
            ]
            damage_done = player.stats["Intelligence"]
            combat_text.append("{} {} {}".format(player.name, random.choice(combat_variables), opponent.readable_name))
    
            return {
                "damage" : damage_done,
                "combat_text" : combat_text
            }

class LifeBolt(Ability):
    def __init__(self):
        super().__init__("LifeBolt")
        self.readable_name = "Lifedraining Bolt"
        self.description = "Shoots out a bolt that can drain life from your opponent."
        self.damage_type = "occult"

    
    def execute(self, player, opponent):
        combat_text = []
        combat_variables = [
            "summons a bolt from the hands and shoots it towards",
            "sends a bolt of dark energy towards",
            "shoots a dark bolt towards"
        ]
        damage_done = int(player.stats["Intelligence"] / 2)
        heal_done = random.randint(0, damage_done)
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

class Scorch(Ability):
    def __init__(self):
        super().__init__("Scorch")
        self.readable_name = "Scorch"
        self.description = "Ignites the target and causes it to burn for 5 turns"
        self.damage_type = "fire"

    def execute(self, player, opponent):
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






#DEBUFFS
class Bleed():
    def __init__(self, turns, damage, opponent_name):
        self.type = "Bleed"
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

class Stun():
    def __init__(self, turns, opponent_name):
        self.type = "Stun"
        self.color = 133
        self.max_turn = turns + 1
        self.turns_left = turns + 1
        self.opponent_name = opponent_name
        self.combat_text = "{} is stunned and unable to respond.".format(self.opponent_name)
        self.combat_text_over = "{} is no longer stunned.".format(self.opponent_name)

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


class Burn():
    def __init__(self, turns, damage, opponent_name):
        self.type = "Burn"
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


class Chill():
    def __init__(self, turns, damage, opponent_name):
        self.type = "Chill"
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


class StatBuff():
    def __init__(self, turns, stat, increase, player, origin=False):
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

