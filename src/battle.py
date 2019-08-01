import random
import time
import helper
import states
import art
import curses
from curses.textpad import Textbox, rectangle

class Battle():
    def __init__(self, state, opponent, battlefield, run=True):
        self.state = state
        self.game_screen = state.game_box
        self.info_screen = state.command_box
        self.screen = state.stdscr
        self.player = state.player
        self.opponent = opponent
        self.opponent_killed = False
        self.battlefield = battlefield
        self.combat_log = []
        self.turn = 1
        self.used_turns = []
        self.loot_list = []
        self.selected_spell = 0
        self.combat_log_color = {
            "opponent" : 133,
            "player" : 134,
            "buff" : 4,
            "neutral" : 0,
            "effect" : 135,
            "loot" : 136
        }

        self.opponent_effects = {
            "stunned" : False,
            "blinded" : False,
        }

        self.commands = [
            "Attack",
            "Block",
            "Spell",
            "Item",
        ]
        if run:
            self.commands.append("Run")

    def dice(self, sides):
        return random.randint(1,sides)

    def update_log(self, text):
        text.append(self.turn)
        self.combat_log.append(text)
        if len(self.combat_log) > 28:
            self.combat_log.pop(0)

    def check_opponent(self):
        self.update_log(["neutral", " "])
        if self.opponent_effects["stunned"]:
            #self.update_log(["effect", "{} is stunned and unable to respond."])
            return
        if self.opponent.health <= 0:
            return
        attack = self.opponent.attack()
        for item in attack["combat_text"]:
            self.update_log(["opponent", item])
        self.player.health -= attack["damage"]

    def check_effects(self):
        if len(self.opponent.status_effects) == 0:
            return
        for item in self.opponent.status_effects:
            if item.type == "Stun":
                self.opponent_effects["stunned"] = True
            result = item.execute()
            if result["combat_text"] != False:
                self.update_log(["effect", result["combat_text"]])
            if result["done"] == True:
                if item.type == "Stun":
                    self.opponent_effects["stunned"] = False
                self.opponent.status_effects.remove(item)
            if result["damage"] != False:
                self.opponent.health -= result["damage"]
        
    def limb_damage_modifier(self):
        limb, modifier = self.opponent.return_limb()
        return limb, modifier

    def player_attack(self):
        weapon = self.player.equipment["right_hand"]
        weapon_damage = random.randint(0,weapon.attack)
        strength_modifier = random.randint(int(0.75 * self.player.stats["Strength"]), self.player.stats["Strength"])
        self.update_log(["player", "{} attacks with {}".format(self.player.name, weapon.name)])

        # MODIFIERS and DAMAGE CALC

        weapon_unique_modifier = weapon.modifier(self.player, self.opponent)

        damage = weapon_damage + strength_modifier
        if weapon_unique_modifier:
            damage = damage * weapon_unique_modifier
        if self.opponent.has_limbs:
            limb, modifier = self.limb_damage_modifier()
            damage = int(damage * modifier)
            self.update_log(["player", "It hits {} in the {}, dealing {} ({}) damage.".format(self.opponent.readable_name, limb, damage, weapon.damage_type)])
        else:
            self.update_log(["player", "it hits {} for {} ({}) damage.".format(self.opponent.readable_name, damage, weapon.damage_type )])
        self.opponent.health -= damage

        #EFFECTS
        effect = weapon.effect(self.player, self.opponent)
        if effect:
            if effect["combat_text"] != False:
                self.update_log(["player", effect["combat_text"]])


    def select_spell(self):
        k = -1
        start = 10
        offset = 15

        selected_item = self.selected_spell
        height, width = self.screen.getmaxyx()

        if self.player.spells:
            spell_list = [spell for spell in self.player.spells if spell != False]
        else:
            spell_list = []

        while k != ord("q"):
            self.screen.clear()

            start = 10
            spell_text = "Select a spell to cast"
            self.screen.addstr(8, int((width / 2) - (len(spell_text) / 2)), spell_text)

            if spell_list:
                for i in range(len(spell_list)):
                    if selected_item == i:
                        self.screen.attron(curses.color_pair(5))
                    self.screen.addstr(start, offset, spell_list[i].readable_name)
                    if selected_item == i:
                        self.screen.attroff(curses.color_pair(5))
                    start += 1
            else:
                helper.popup(self.screen, self.state, ["No spells available"])
                return "False"

            if k == curses.KEY_DOWN:
                if len(spell_list) != 0:
                    selected_item += 1
                    if selected_item >= len(spell_list) - 1:
                        selected_item = len(spell_list) - 1

            if k == curses.KEY_UP:
                if len(spell_list) != 0:
                    selected_item -= 1
                    if selected_item <= 0:
                        selected_item = 0

            if k == ord(" "):
                if len(spell_list) != 0:
                    self.selected_spell = selected_item
                    return self.player.spells.index(spell_list[selected_item])

            k = self.screen.getch()
        return "False"


    def player_run(self):
        chance = self.dice(100)
        if chance > 70:
            self.update_log(["neutral", "You ran away."])
            return True
        else:
            self.update_log(["neutral","You failed to run away."])
            return False

    def player_spell(self,spell_index):
        attack = self.player.spells[spell_index].execute(self.player, self.opponent)
        damage = attack["damage"]
        for item in attack["combat_text"]:
            self.update_log(["player", item])

        self.opponent.health -= damage

    def check_player(self):
        pass

    def check_turn_events(self):
        pass

    def play(self):
        self.update_log(["opponent","{} encounters {} {}".format(self.player.name, self.opponent.before_name ,self.opponent.readable_name)])
        self.update_log(["neutral", ""])
        k = -1
        selected_command = 0
        offset = 30

        opponent_offset = 15
        opponent_art_offset = 2

        while k != ord("q"):
            if self.player.health <= 0:
                helper.popup(self.screen, self.state, ["You have died"])
                self.state.game_state = states.Intro(self.state)
                self.state.command_state = states.main_menu(self.state)
                self.state.map_screen = False
                self.state.command_state.commands[0].active = True
                self.state.player = False
                self.state.first_time = True
                break
            if self.opponent.health <= 0 and self.opponent_killed == False:
                self.update_log(["opponent", "{} was killed.".format(self.opponent.readable_name)])
                self.update_log(["neutral", ""])
                random_loot = self.opponent.generate_loot()
                if random_loot:
                    self.loot_list = [helper.get_item(item)() for item in random_loot]
                else:
                    self.loot_list = []

                if self.loot_list:
                    for item in self.loot_list:
                        self.update_log(["loot", "{} dropped item: {}".format(self.opponent.readable_name, item.readable_name)])
                else:
                    self.update_log(["loot", "{} dropped no loot.".format(self.opponent.readable_name)])
                
                self.commands = [
                    "Loot",
                    "Exit"
                ]
                selected_command = 0
                self.opponent_killed = True
                #return True
            self.screen.clear()


            combat_log_start = 0
            self.used_turns = []
            for item in self.combat_log:
                if item[2] not in self.used_turns:
                    self.screen.addstr(combat_log_start, 0, "Turn {}:".format(item[2]))
                    self.used_turns.append(item[2])
                self.screen.attron(curses.color_pair(self.combat_log_color[item[0]]))
                if item[0] == "opponent":
                    self.screen.addstr(combat_log_start, 14, item[1])
                else:
                    self.screen.addstr(combat_log_start, 10, item[1])
                self.screen.attroff(curses.color_pair(self.combat_log_color[item[0]]))

                combat_log_start += 1

            percent_health = round(self.player.health / self.player.max_health, 2)
            percent_lost = 1 - percent_health
            self.screen.addstr(37,0, "HP:")
            self.screen.attron(curses.color_pair(5))
            self.screen.addstr(37,5,"{}".format("-" * int(100 * percent_health)))
            self.screen.attroff(curses.color_pair(5))
            self.screen.addstr(37,int(105 * percent_health),"{}".format("-" * int(100 * percent_lost)))

            for i in range(len(self.commands)):
                if i == selected_command:
                    self.screen.attron(curses.color_pair(5))
                    self.screen.addstr(offset + i, 10, self.commands[i])
                    self.screen.attroff(curses.color_pair(5))
                else:
                    self.screen.addstr(offset + i, 10, self.commands[i])

            self.screen.attron(curses.color_pair(133))
            for idx, text in enumerate(self.opponent.art):
                self.screen.addstr(opponent_art_offset + idx, 100, text)
            self.screen.attroff(curses.color_pair(133))
                
            self.screen.addstr(opponent_offset, 100, "Opponent: {}".format(self.opponent.readable_name))
            for i,v in enumerate(self.opponent.description):
                self.screen.addstr(opponent_offset + i + 1, 100, v)
            self.screen.addstr(opponent_offset + 5, 100, "HP: {} / {}".format(self.opponent.health, self.opponent.max_health))
            

            k = self.screen.getch()

            if k == curses.KEY_UP:
                if selected_command != 0:
                    selected_command -= 1

            elif k == curses.KEY_DOWN:
                if selected_command != len(self.commands) - 1:
                    selected_command += 1

            elif k == ord(" "):
                self.turn += 1
                if self.commands[selected_command] == "Attack":
                    self.player_attack()

                if self.commands[selected_command] == "Block":
                    pass

                if self.commands[selected_command] == "Run":
                    self.update_log(["neutral", "Attempting to run away."])
                    run_successful = self.player_run()
                    if run_successful:
                        return False

                if self.commands[selected_command] == "Spell":
                    spell = self.select_spell()
                    if spell != "False":
                        self.player_spell(spell)
                    else:
                        continue
                if self.commands[selected_command] == "Loot":
                    self.loot(random_loot)
                    #return True
                
                if self.commands[selected_command] == "Exit":
                    return True
                    
                if self.opponent_killed == False:
                    self.check_effects()
                    self.check_opponent()
                    self.update_log(["neutral",""])
            
    def loot(self, random_loot):
        k = -1
        start = 10
        offset = 15
        #random_loot = self.opponent.generate_loot()
        #if random_loot:
        #    loot_list = [helper.get_item(item)() for item in random_loot]
        #else:
        #    loot_list = []
        selected_item = 0
        height, width = self.screen.getmaxyx()


        while k != ord("q"):
            self.screen.clear()

            start = 10
            loot_text = "{} dropped the following loot".format(self.opponent.readable_name)
            self.screen.addstr(8, int((width / 2) - (len(loot_text) / 2)), loot_text)

            if self.loot_list:
                for i in range(len(self.loot_list)):
                    if selected_item == i:
                        self.screen.attron(curses.color_pair(5))
                    self.screen.addstr(start, offset, self.loot_list[i].readable_name)
                    if selected_item == i:
                        self.screen.attroff(curses.color_pair(5))
                    start += 1
            else:
                self.screen.addstr(start, offset, "No loot")

            if k == curses.KEY_DOWN:
                if len(self.loot_list) != 0:
                    selected_item += 1
                    if selected_item >= len(self.loot_list) - 1:
                        selected_item = len(self.loot_list) - 1

            if k == curses.KEY_UP:
                if len(self.loot_list) != 0:
                    selected_item -= 1
                    if selected_item <= 0:
                        selected_item = 0

            if k == ord(" "):
                if len(self.loot_list) != 0: 
                    self.player.inventory.append(self.loot_list.pop(selected_item))
                selected_item = 0
            k = self.screen.getch()


def yes_no(screen, state, text):
	screen.clear()
	k = -1
	yes_selected = True
	
	while k != ord(" "):
		start = 10
		for item in text:
			screen.addstr(start, 34, item)
			start += 1
		if yes_selected:
			screen.attron(curses.color_pair(5))
			screen.addstr(18,34, "Yes")
			screen.attroff(curses.color_pair(5))
			screen.addstr(18, 40, "No")
		else:
			screen.addstr(18,34, "Yes")
			screen.attron(curses.color_pair(5))
			screen.addstr(18, 40, "No")
			screen.attroff(curses.color_pair(5))

		k = screen.getch()

		if k == curses.KEY_LEFT:
			yes_selected = True
		elif k == curses.KEY_RIGHT:
			yes_selected = False
	
	return yes_selected





if __name__ == "__main__":
    pass