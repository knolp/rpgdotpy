class Flags():
    def __init__():
        self.comment = "Here are all the flags"

    def RatMenace(self):
        questgiver = "Osk'Ghar the Rock"
        location = "Starter Town House"
        started = "RatMenace_started"

        rat_1 = "RatMenace_rat1_killed"
        rat_2 = "RatMenace_rat2_killed"
        rat_3 = "RatMenace_rat3_killed"
        rat_king = "RatMenace_rat_king_killed"

        completed = "RatMenace_completed"
        reward = "RatMenace_reward"

        BasementChest = "BasementChest_item_taken"




class HurBattleSkaFungera():
    def __init__():
        self.comment = "Lite funderingar över hur battle-systemet ska fungera"


    def player_damage(self):
        först = "kolla vapen + basedamage"
        sen = "lägga på multipliers"
        multipliers = {
            "limbs" : "typ om man träffar huvudet, definieras i monster.py per opponent",
            "critical strike" : "kolla om man crittar helt enkelt",
            "buffs" : "typ battleroars eller lightning-infused blade eller vad som helst",
            "debuffs" : "effekt från opponents",
            "special" : "kolla om man har något speciellt typ, 'ratslaying necklace' eller något sånt kanske ger mer dmg mot rats"
        }
        efter_det = "checka opponent armor eller defence och dra av"
        sist = "runda av och dra av från opponent HP"