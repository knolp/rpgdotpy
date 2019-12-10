import random

class Ability():
    def __init__(self, name):
        self.name = name
    
    def execute(self):
        pass





#Spells
class Fireball(Ability):
    def __init__(self):
        super().__init__("Fireball")
        self.readable_name = "Fireball"
        self.description = "Conjures a great ball of fire, ready to throw at any foe."

    def execute(self, player, opponent):
        combat_text = []
        combat_variables = [
            "hurls a big fireball towards",
            "conjures a great ball of fire and throws it towards",
            "casts a fireball at"
        ]
        damage_done = player.stats["Intelligence"]
        combat_text.append("{} {} {}".format(player.name, random.choice(combat_variables), opponent.readable_name))
        combat_text.append("It deals {} damage.".format(damage_done))

        return {
            "damage" : damage_done,
            "combat_text" : combat_text
        }

class LifeBolt(Ability):
    def __init__(self):
        super().__init__("LifeBolt")
        self.readable_name = "Lifedraining Bolt"
        self.description = "Shoots out a bolt that can drain life from your opponent."

    
    def execute(self, player, opponent):
        combat_text = []
        combat_variables = [
            "summons a bolt from the hands and shoots it towards",
            "sends a bolt of dark energy towards",
            "shoots a dark bolt towards"
        ]
        damage_done = int(player.stats["Intelligence"] / 2)
        heal_done = random.randint(0,damage_done)
        combat_text.append("{} {} {}".format(player.name, random.choice(combat_variables), opponent.readable_name))
        if player.health + heal_done < player.max_health:
            player.health += heal_done
            combat_text.append("It deals {} damage and heals you for {}".format(damage_done, heal_done))
        else:
            player.health = player.max_health
            combat_text.append("It deals {} damage and heals you for {}".format(damage_done, player.max_health - player.health))

        return {
            "damage" : damage_done,
            "combat_text" : combat_text
        }

class Scorch(Ability):
    def __init__(self):
        super().__init__("Scorch")
        self.readable_name = "Scorch"
        self.description = "Ignites the target and causes it to burn for 5 turns"

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


class Chilled():
    def __init__(self, turns, weakness, opponent_name):
        self.type = "Chill"
        self.max_turn = turns + 1
        self.turns_left = turns + 1
        self.weakness = weakness
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
                "damage" : self.damage
            }