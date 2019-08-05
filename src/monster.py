import random
import art

class Monster():
    def __init__(self,name):
        self.name = name
        self.loot = []
        self.special_loot = {}
        self.limbs = {}
        self.has_limbs = True
        self.status_effects = []

    
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
        list_of_limbs = [k for k,v in self.limbs.items()]
        selected_limb = random.choice(list_of_limbs)

        return selected_limb, self.limbs[selected_limb]








class Rat(Monster):
    def __init__(self):
        super().__init__("Rat")
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
        self.limbs = {
            "head" : 2,
            "body" : 1,
            "tail" : 0.5,
            "left front paw" : 1,
            "right front paw" : 1,
            "left back paw" : 1,
            "right back paw" : 1
        }

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
    def __init__(self):
        super().__init__("RatKing")
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
        self.random_loot = []
        self.special_loot = {
            "RatFangNecklace" : 3
        }
        self.limbs = {
            "head" : 2,
            "body" : 1,
            "tail" : 0.5,
            "left front paw" : 1,
            "right front paw" : 1,
            "left back paw" : 1,
            "right back paw" : 1
        }

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
    def __init__(self):
        super().__init__("SkeletonGrunt")
        self.race = "Skeleton"
        self.description = [
            "A skeleton of a human soldier who died."
        ]
        self.before_name = "a"
        self.readable_name = "Skeleton Grunt"
        self.art = art.draw_SkeletonGrunt()
        self.max_health = 100
        self.health = self.max_health
        self.damage = 2
        self.attack_styles = ["attacks", "claws", "bashes"]
        self.buffed_turn = 0
        self.loot = []
        self.random_loot = ["LeatherBoots"]
        self.special_loot = {
            "Longsword" : 3
        }
        self.limbs = {
            "head" : 2,
            "body" : 1
        }

    def melee_attack(self):
        pass

    def special_attack(self):
        pass

    def attack(self):
        pass


if __name__ == "__main__":
    opp = Rat()

    for i in range(100):
        print(opp.generate_loot())