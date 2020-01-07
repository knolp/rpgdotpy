import random
import art
import items

class Limb():
    def __init__(self, owner, name, vital, grabbable, health, multiplier,fur=False, held_item=False):
        self.owner = owner
        self.name = name
        self.vital = vital
        self.grabbable = grabbable
        self.max_health = health
        self.health = health
        self.multiplier = multiplier
        self.held_item = held_item
        self.fur = fur
        self.alive = True

        self.effects = []

    def check_effects(self):
        pass

    def check_limb(self, weapon):
        dropped_item = False
        combat_text = []

        if weapon.damage_type == "Slash" and random.randint(1,100) > 95:
                combat_text.append(f"The slashing motion of {weapon.readable_name} chops the {self.name} right off.")
                combat_text.append(f"{self.name} fall to the floor.")
                self.owner.limbs.remove(self)
                if self.vital:
                    combat_text.append(f"Killing the {self.owner.readable_name} instantly.")
                    self.owner.health = -1

        if not self.alive:
            combat_text.append(f"{self.owner.readable_name}'s {self.name} is badly damaged already, causing more damage.")
        elif self.health < self.max_health and self.alive:
            self.alive = False
            combat_text.append(f"{self.owner.readable_name}'s {self.name} has taken too much damage and lost function.")
            if self.vital:
                combat_text.append(f"Killing the {self.owner.readable_name} instantly.")
                self.owner.health = -1

        if not self.alive and self.held_item:
            dropped_item = self.held_item
            self.held_item = False

            combat_text.append(f"{dropped_item.readable_name} falls off {self.owner.readable_name}'s {self.name} onto the floor.")
        
        return {
            "combat_text" : combat_text,
            "dropped_item" : dropped_item
        }


class Monster():
    def __init__(self,name):
        self.name = name
        self.loot = []
        self.special_loot = {}
        self.limbs = []
        self.has_limbs = True
        self.status_effects = []
        self.immune = []
        self.player = False
    
    def generate_loot(self):
        loot_chances = [100,75, 50, 25, 0]
        return_loot = []

        if self.special_loot:
            for key,value in self.special_loot.items():
                if random.randint(1,100) <= value:
                    return_loot.append(key)

        if self.loot:
            for value in loot_chances:
                if random.randint(1,100) <= value:
                    return_loot.append(random.choice(self.loot))
            return list(set(return_loot))
        else:
            return False

    def return_limb(self):
        selected_limb = random.choice(self.limbs)

        return selected_limb.name, selected_limb.multiplier

    def melee_attack(self):
        combat_text = []
        held_item = False

        melee_damage = random.randint(0,self.damage)

        for limb in self.limbs:
            if limb.held_item:
                held_item = True
                if limb.held_item.type == "weapon":
                    melee_damage = random.randint(0,self.damage + limb.held_item.attack)
                    combat_text.append(f"{self.readable_name} {random.choice(limb.held_item.attack_styles[limb.held_item.damage_type])} with {limb.held_item.readable_name} at you for {limb.held_item.attack} damage.")
                result = limb.held_item.effect(self, self.state.player)
                if result:
                    if result["combat_text"] != False:
                        for item in result["combat_text"]:
                            combat_text.append(item)
        if not held_item:
            combat_text = [f"{self.readable_name} {random.choice(self.attack_styles)} you for {random.randint(0,self.damage)} damage."]

        return {
            "combat_text" : combat_text,
            "damage" : melee_damage
        }








class Rat(Monster):
    def __init__(self, state):
        super().__init__("Rat")
        self.state = state
        self.race = "Rat"
        self.description = ["A regular rat."]
        self.before_name = "a"
        self.readable_name = "Rat"
        self.art = art.draw_Rat()
        self.max_health = 10
        self.health = self.max_health
        self.damage = 1
        self.attack_styles = ["attacks", "gnaws", "lunges at", "bites"]
        self.buffed_turn = 0
        self.loot = ["LeatherBoots", "ChainMail", "Longsword", "ChainHelmet"]
        self.special_loot = {
            "RatFangNecklace" : 3
        }
        self.limbs = [
            Limb(self,"head",True,False,10,2),
            Limb(self,"body",False,False,10,1),
            Limb(self,"tail",False,False,5,0.5),
            Limb(self,"left front paw",False,True,5,1),
            Limb(self,"right front paw",False,True,5,1),
            Limb(self,"left back paw",False,False,5,1),
            Limb(self,"right back paw",False,False,5,1)
        ]
        for item in self.limbs:
            item.fur = True

    def __str__(self):
        return self.name


    def melee_attack(self):
        combat_text = []

        melee_damage = random.randint(0,self.damage)
        if self.buffed_turn == 1:
            self.buffed_turn -= 1
            combat_text.append("{} is no longed frenzied.".format(self.name))
        if self.buffed_turn > 0:
            self.buffed_turn -= 1
            melee_damage += 1
            combat_text.append("{} is still frenzied, increasing it's attack.".format(self.name))
        combat_text.append("{} {} you for {} damage.".format(self.readable_name, random.choice(self.attack_styles), melee_damage))

        return {
            "combat_text" : combat_text,
            "damage" : melee_damage
        }

    def rat_screech(self):
        combat_text = []

        self.buffed_turn = 3
        combat_text.append("{} gives off a screech and goes into a frenzy.".format(self.name))

        return {
            "combat_text" : combat_text,
            "damage" : 0
        }

    def attack(self):
        roll = random.randint(1,100)

        if roll > 80 and self.buffed_turn == 0:
            return self.rat_screech()
        else:
            return self.melee_attack()

class RatKing(Monster):
    def __init__(self, state):
        super().__init__("RatKing")
        self.state = state
        self.race = "Rat"
        self.description = [
            "A large, fat rat standing on two legs,",
            "clutching a coin purse in one paw and",
            "a stick in the other."
        ]
        self.before_name = "The"
        self.readable_name = "Rat King"
        self.art = art.draw_RatKing()
        self.max_health = 600
        self.health = self.max_health
        self.damage = 7
        self.attack_styles = ["attacks", "gnaws", "bashes", "slams his staff at", "smashes his staff"]
        self.buffed_turn = 0
        self.coins = 20
        self.loot = []
        self.special_loot = {
            "RatFangNecklace" : 3
        }
        self.limbs = [
            Limb(self,"head",True,False,10,2),
            Limb(self,"body",False,False,10,1),
            Limb(self,"tail",False,False,5,0.5),
            Limb(self,"left front paw",False,True,5,1),
            Limb(self,"right front paw",False,True,5,1),
            Limb(self,"left back paw",False,False,5,1),
            Limb(self,"right back paw",False,False,5,1)
        ]
        for item in self.limbs:
            item.fur = True

    def __str__(self):
        return self.name


    def melee_attack(self):
        combat_text = []

        melee_damage = random.randint(0,self.damage)
        if self.buffed_turn == 1:
            self.buffed_turn -= 1

        if self.buffed_turn > 0:
            self.buffed_turn -= 1

        combat_text.append("{} {} you for {} damage.".format(self.readable_name, random.choice(self.attack_styles), melee_damage))

        return {
            "combat_text" : combat_text,
            "damage" : melee_damage
        }

    def coin_toss(self):
        combat_text = []
        coins = random.randint(1,10)
        if self.coins != 0:
            if coins <= self.coins:
                self.coins -= coins
            else:
                coins = self.coins
                self.coins = 0
            combat_text.append("{} picks up {} coins from his purse.".format(self.readable_name, coins))
            combat_text.append("{} tosses them at you, dealing {} damage.".format(self.readable_name, coins))
        else:
            combat_text.append("{} tries to pick up some coins from his purse.".format(self.readable_name))
            combat_text.append("But the purse seems to be empty.")
            coins = 0

        return {
            "combat_text" : combat_text,
            "damage" : coins
        }

    def attack(self):
        roll = random.randint(1,100)

        if roll > 80 and self.buffed_turn == 0:
            return self.coin_toss()
        else:
            return self.melee_attack()


class SkeletonGrunt(Monster):
    def __init__(self, state):
        super().__init__("SkeletonGrunt")
        self.state = state
        self.race = "Skeleton"
        self.description = [
            "A skeleton of a human soldier."
        ]
        self.before_name = "a"
        self.readable_name = "Skeleton Grunt"
        self.art = art.draw_SkeletonGrunt()
        self.max_health = 100
        self.health = self.max_health
        self.damage = 2
        self.immune = ["Bleed"]
        self.attack_styles = ["bashes at", "swings"]
        self.buffed_turn = 0
        self.loot = ["LeatherBoots"]
        self.special_loot = {
            "Longsword" : 3
        }
        self.limbs = [
            Limb(self,"skull",False,False,10,2),
            Limb(self,"torso",False,False,10,1),
            Limb(self,"right arm",False,True,5,1, held_item=items.ChromaticBlade()),
            Limb(self,"left arm",False,True,5,1),
            Limb(self,"right leg",False,False,5,1),
            Limb(self,"left leg",False,False,5,1),
        ]
    def __str__(self):
        return self.name

    

    def special_attack(self):
        pass

    def attack(self):
        return self.melee_attack()


if __name__ == "__main__":
    opp = Rat()

    for i in range(100):
        print(opp.generate_loot())