class Flags():
    def __init__(self):
        self.comment = "Here are all the flags"

    def RatMenace(self, quest):
        questgiver = "Osk'Ghar the Rock"
        location = "Starter Town House"
        started = "RatMenace_started"

        rat_1 = "RatMenace_rat1_killed"
        rat_2 = "RatMenace_rat2_killed"
        rat_3 = "RatMenace_rat3_killed"
        rat_king = "RatMenace_rat_king_killed"

        completed = "RatMenace_completed"
        reward = "RatMenace_reward"

        BasementChest = "BasementChest_item_taken_{ITEMNAME}"

    
    def BrownBearInn(self, map):
        evankripter = {
            "EvanKripter_met" = "har träffat evan kripter i brown bear inn"
        }
        larsmagnus = {
            "LarsMagnus_met" = "har träffat Lars Magnus i brown bear inn"
        }

    def WakeUpCall(self, quest):
        questgiver = "Lars Magnus"
        location = "Brown Bear Inn"

        started = "WakeUpCall_started"
        deverberries = "WakeUpCall_deverberries_picked"




class HurBattleSkaFungera():
    def __init__(self):
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



class PlayerHousing():
    def __init__(self):
        self.comment = "Någon form av player-housing där man kan lägga till och uppgradera saker, typ alchemy-station, teleportation etc"

    
    def tankar():
        self.saker = {
            "alchemy-station" : "där man kan göra potions/poisons/elixirs etc",
            "teleport-pad / inhyrd magiker" : "Där man kan TP:a till andra teleport-hubs i städer",
            "säng" : "kanske ger regenbuff eller recover HP eller liknande",
            "andra crafting-saker" : "Typ leatherworking eller göra pilar eller vad som",
            "egen levelup service-grej" : "Slippa gå till altars för att levla upp",
            "altars" : "attuna med sin gud i hemmet, ge offergåvor eller något"
        }