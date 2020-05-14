import curses
import random
import time
from curses.textpad import Textbox, rectangle

import art
import helper
import states


class Battle():
    def __init__(self, state, opponent, battlefield, run=True):
        self.debug = False
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
            "opponent": 133,
            "player": 134,
            "buff": 4,
            "neutral": 0,
            "opponent_effect": 135,
            "player_effect": 136,
            "loot": 136
        }

        self.opponent_effects = {
            "stunned": False,
            "blinded": False,
        }

        self.player_effects = {
            "stunned": False,
            "blinded": False
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
        """
            Dice for generating rolls

            :param sides = sides of the die

            :returns integer
        """
        return random.randint(1, sides)

    def update_log(self, text):
        """
            Add information to the combat log, most important.

            :param text = list("<type>", "<information string>)

            types:
                player = green text (indicating good)
                opponent = red text (indicating bad)
                neutral = ??? text (indicating neutral information) ex. opponent is stunned
                opponent_effect = blue text (indicating good effects)
                player_effect = orange text (indicating bad effects)
                loot = orange text (loot drops) #! Change this

            max length for combat_log is 36 rows
        """
        text.append(self.turn)
        self.combat_log.append(text)
        if len(self.combat_log) > 36:
            self.combat_log.pop(0)

    def check_opponent(self):
        """
            This is where the opponent get's it turn

            TODO: Maybe add more than just attack, maybe usage of consumables or something
            TODO: Or maybe better off having all that on the monster class
        """
        self.update_log(["neutral", " "])
        if self.opponent_effects["stunned"]:
            # self.update_log(["effect", "{} is stunned and unable to respond."])
            return
        if self.opponent.health <= 0:
            return
        attack = self.opponent.attack()
        for item in attack["combat_text"]:
            self.update_log(["opponent", item])
        damage = attack["damage"]
        for _, value in self.player.equipment.items():
            if not value:
                continue
            if value.type != "armor":
                continue
            else:
                ret_dict = value.effect(self.player, self.opponent, on_damage_taken=True)
                if ret_dict["success"] != True:
                    continue
                if ret_dict["multiplier"]:
                    damage *= ret_dict["multiplier"]
                if ret_dict["additive"]:
                    damage += ret_dict["additive"]
                if ret_dict["damage"]:
                    self.opponent.health -= ret_dict["damage"]
                if ret_dict["combat_text"]:
                    for text in ret_dict["combat_text"]:
                        self.update_log(["player", text])

        self.player.health -= damage

    def check_effects(self):
        """
            Check the opponent for effects

            1. Execute them
            2. Check if they are done
            3. if done, remove
        """
        if len(self.opponent.status_effects) == 0:
            return
        for item in self.opponent.status_effects:
            if item.type == "Stun":
                self.opponent_effects["stunned"] = True
            result = item.execute()
            if result["combat_text"] is not False:
                self.update_log(["opponent_effect", result["combat_text"]])
            if result["done"] is True:
                if item.type == "Stun":
                    self.opponent_effects["stunned"] = False
                self.opponent.status_effects.remove(item)
            if result["damage"] is not False:
                self.opponent.health -= result["damage"]
            
            try:
                if result["heal-player"] is not False:
                    self.player.health += result["heal"]
            except:
                pass

    def check_player_effects(self):
        """
            Check the player for effects and

            1. Execute them
            2. check if they are done
            3. if done, remove.
        """
        if len(self.player.status_effects) == 0:
            return
        for item in self.player.status_effects:
            if item.type == "Stun":
                self.player_effects["stunned"] = True
            result = item.execute()
            if result["combat_text"] is not False:
                self.update_log(["player_effect", result["combat_text"]])
            if result["done"] is True:
                if item.type == "Stun":
                    self.player_effects["stunned"] = False
                self.player.status_effects.remove(item)
            if result["damage"] is not False:
                self.player.health -= result["damage"]

    def limb_damage_modifier(self, aoe=False):
        """
            Get the modifier from the limb of opponent

            Modifier = damage scaling
            Limb = Limb object of opponent

            :return Tuple
        """
        if not aoe:
            limb, modifier = self.opponent.return_limb()
            return limb, modifier
        else:
            limbs = self.opponent.return_multiple_limbs(aoe)
            return limbs

    def unarmed_attack(self):
        """
            Unarmed attacks

            Scale with strength


            TODO: Add check for items that scale unarmed attacks

            :return None
        """
        damage = self.player.stats["Strength"]
        self.update_log(["player", "{} attacks with fists".format(self.player.name)])
        if self.opponent.has_limbs:
            limb, modifier = self.limb_damage_modifier()
            damage = int(damage * modifier)
            self.update_log(["player", "It hits {} in the {}, dealing {} damage.".format(self.opponent.readable_name, limb, damage)])
        else:
            self.update_log(["player", "It hits {} for {} damage.".format(self.opponent.readable_name, limb, damage)])
        self.opponent.health -= damage
        recoil = random.randint(0, self.player.stats["Strength"])
        self.update_log(["player", "The attack bruises {}'s knuckles, dealing {} damage in recoil.".format(self.player.name, recoil)])
        self.player.health -= recoil

    def player_attack(self):
        """
            This is where the player melee attack is performed

            The general idea is:
            
            1. Get base damage
                1.1 add in gear attack
            2. Add in strength modifier
            3. Check weapon modifier, if so, add that one
            4. Check which limb hit, and add appropiate modifier
            5. Check weapon effects, stuns, debuffs etc.

            TODO: Add critical change, critical hit damage, check jewellery and other armor modifiers

            :return None

        """
        if self.player_effects["stunned"]:
            return
        weapon = self.player.equipment["right_hand"]

        # If no weapon, skip to unarmed attack
        if weapon is False:
            self.unarmed_attack()
            return

        # Add weapon damage
        weapon_damage = random.randint(1, weapon.attack)

        # Add in gear damage
        gear_damage = 0
        for k, value in self.player.equipment.items():
            if value:
                gear_damage += value.attack
        weapon_damage += gear_damage
        
        # Add in strength modifier
        strength_modifier = random.randint(int(0.75 * self.player.stats["Strength"]), self.player.stats["Strength"])
        self.update_log(["player", "{} attacks with {}".format(self.player.name, weapon.readable_name)])

        # MODIFIERS and DAMAGE CALC

        # Add strength modifier for melee hits
        damage = weapon_damage + strength_modifier

        # Weapon modifier t.ex Rat mace, Moonlight sword intelligence scaling
        weapon_unique_modifier = weapon.modifier(self.player, self.opponent)
        if weapon_unique_modifier:
            damage = damage * weapon_unique_modifier

        # Add limb damage
        if self.opponent.has_limbs:
            # Limb modifier, t.ex 2x damage against head
            limb, modifier = self.limb_damage_modifier()
            damage = int(damage * modifier)

            self.update_log(["player", "It hits {} in the {}, dealing {} ({}) damage.".format(self.opponent.readable_name, limb, damage, weapon.damage_type)])

            # Find the limb and deal damage to it and the result of that
            for opp_limb in self.opponent.limbs:
                if opp_limb.name == limb:
                    opp_limb.health -= damage
                    
                    # If the limb dies or get chopped off
                    limb_result = opp_limb.check_limb_weapon(weapon)
                    for item in limb_result["combat_text"]:
                        self.update_log(["opponent_effect", item])
        else:

            # Update combat log with attack message and damage
            self.update_log(["player", "it hits {} for {} ({}) damage.".format(self.opponent.readable_name, damage, weapon.damage_type)])

        # Remove damage from opponent health pool
        self.opponent.health -= damage

        # EFFECTS ex. Bleed, burn, chill, stun
        effect = weapon.effect(self.player, self.opponent)
        if effect:
            if effect["combat_text"] is not False:
                for item in effect["combat_text"]:
                    self.update_log(["player", item])

    def select_spell(self):
        """
            Select spell from main combat menu

            :return Spell (if spell selected)
            :return False (if no spell selected)
        """

        k = -1
        start = 10
        offset = 15

        selected_item = self.selected_spell
        height, width = self.screen.getmaxyx()

        if self.player.spells:
            spell_list = [spell for spell in self.player.spells if spell is not False]
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
                curses.ungetch(curses.KEY_F0)

            if k == curses.KEY_UP:
                if len(spell_list) != 0:
                    selected_item -= 1
                    if selected_item <= 0:
                        selected_item = 0
                curses.ungetch(curses.KEY_F0)

            if k == ord(" "):
                if len(spell_list) != 0:
                    self.selected_spell = selected_item
                    return self.player.spells.index(spell_list[selected_item])
                curses.ungetch(curses.KEY_F0)

            k = self.screen.getch()
        return "False"

    def player_run(self):
        """
            If selected Run from main combat menu

            Note: Run is only added if enabled when combat is started, default False.

            :return bool (if successful or not)
        """
        chance = self.dice(100)
        if chance > 70:
            self.update_log(["neutral", "You ran away."])
            return True
        else:
            self.update_log(["neutral", "You failed to run away."])
            return False

    def player_spell(self, spell_index):
        """
            Here the player attacks with a spell

            Right now it is:

            1. perform spell
            2. remove damage

            TODO: Rework completely, add limb damage, check gear for mods, etc
        """

        # Execute spell, get base damage
        spell = self.player.spells[spell_index]
        attack = spell.execute(self.player, self.opponent, self.state)
        damage = attack["damage"]
        if damage == "back":
            return False
        damage_type = spell.damage_type
        for item in attack["combat_text"]:
            self.update_log(["player", item])

        # add intelligence scaling
        if self.debug:
            self.update_log(["neutral", f"Damage is now (base): {int(damage)}"])
        damage += int(self.player.get_combined_stats()["Intelligence"] * (damage * 0.1)) #10% additive-base for each intellect-point
        if self.debug:
            self.update_log(["neutral", f"Damage is now (int scaling): {int(damage)}"])

        list_of_multipliers = []
        list_of_additives = []
        list_of_additive_bases = []
        list_of_converts = []
        list_of_conditional_multipliers = []
        list_of_conditional_additives = []

        # Check armor
        for _, value in self.player.equipment.items():
            if not value:
                continue
            if value.type != "armor":
                continue
            else:
                ret_dict = value.effect(self.player, self.opponent, spell=spell)
                if ret_dict["success"] != True:
                    continue
                if ret_dict["multiplier"]:
                    list_of_multipliers.append(ret_dict["multiplier"])
                if ret_dict["additive"]:
                    list_of_additives.append(ret_dict["additive"])
                if ret_dict["additive-base"]:
                    list_of_additive_bases.append(ret_dict["additive-base"])
                if ret_dict["convert"]:
                    list_of_converts.append(ret_dict["convert"])
                if ret_dict["conditional-multiplier"]:
                    list_of_conditional_multipliers.append(ret_dict["conditional-multiplier"])
                if ret_dict["conditional-additive"]:
                    list_of_conditional_additives.append(ret_dict["conditional-additive"])
                if ret_dict["combat_text"]:
                    for text in ret_dict["combat_text"]:
                        self.update_log(["player", text])

        #Loop through all gear effects:
        #Start with convert
        if list_of_converts:
            damage_type = random.choice(list_of_converts)
            self.update_log(["neutral", f"Converted damage type to {damage_type}"])

        if self.debug:
            self.update_log(["neutral", f"Damage is now: {int(damage)}"])
        #Then all additives and additive base
        if list_of_additives:
            for item in list_of_additives:
                damage += item
                self.update_log(["neutral", f"Additive {item}"])

            if self.debug:
                self.update_log(["neutral", f"Damage is now: {int(damage)}"])

        if list_of_additive_bases:
            for item in list_of_additive_bases:
                damage += attack["damage"] + item
                self.update_log(["neutral", f"Additive-base base: {attack['damage']} add: {item}"])
            if self.debug:
                self.update_log(["neutral", f"Damage is now: {int(damage)}"])

        if list_of_conditional_additives:
            for item in list_of_conditional_additives:
                if item[0] == damage_type:
                    damage += item[1]
                    self.update_log(["neutral", f"Conditional additive, cond: {item[0]} add: {item[1]}"])
            if self.debug:
                self.update_log(["neutral", f"Damage is now: {int(damage)}"])

        #Then all multipliers
        if list_of_multipliers:
            for item in list_of_multipliers:
                damage *= item
                self.update_log(["neutral", f"Multiplier, mult: {item}"])
            if self.debug:
                self.update_log(["neutral", f"Damage is now: {int(damage)}"])

        if list_of_conditional_multipliers:
            for item in list_of_conditional_multipliers:
                if item[0] == damage_type:
                    damage *= item[1]
                    self.update_log(["neutral", f"Conditional mult, cond{item[0]} mult: {item[1]}"])
            if self.debug:
                self.update_log(["neutral", f"Damage is now: {int(damage)}"])

        

        # Get limb damage
        if self.opponent.has_limbs:
            if spell.aoe:
                # If spell has AoE radius it hits multiple limbs
                limbs = self.limb_damage_modifier(aoe=spell.aoe)
                before_limbs_damage = damage

                for limb in limbs:
                    if spell.no_direct_damage:
                        damage = 0
                        break
                    limb_damage = before_limbs_damage * limb[1]
                    self.update_log(["player", "It hits {} in the {}, dealing {} ({}) damage.".format(self.opponent.readable_name, limb[0], limb_damage, damage_type)])

                    for opp_limb in self.opponent.limbs:
                        if opp_limb.name == limb[0]:
                            opp_limb.health -= limb_damage
                            
                            # If the limb dies or get chopped off
                            limb_result = opp_limb.check_limb_weapon(spell)
                            for item in limb_result["combat_text"]:
                                self.update_log(["opponent_effect", item])
            else:
                # Limb modifier, t.ex 2x damage against head
                limb, modifier = self.limb_damage_modifier()
                damage = int(damage * modifier)

                if spell.no_direct_damage:
                    damage = 0
                    
                else:
                    self.update_log(["player", "It hits {} in the {}, dealing {} ({}) damage.".format(self.opponent.readable_name, limb, damage, damage_type)])

                # Find the limb and deal damage to it and the result of that
                for opp_limb in self.opponent.limbs:
                    if opp_limb.name == limb:
                        opp_limb.health -= damage
                        
                        # If the limb dies or get chopped off
                        limb_result = opp_limb.check_limb_weapon(spell)
                        for item in limb_result["combat_text"]:
                            self.update_log(["opponent_effect", item])
        else:

            # Update combat log with attack message and damage
            self.update_log(["player", "it hits {} for {} ({}) damage.".format(self.opponent.readable_name, damage, weapon.damage_type)])




        self.opponent.health -= damage
        return True

    def check_player(self):
        pass

    def check_turn_events(self):
        pass

    def remove_temp_debuffs(self):
        """
            removes temporary combat debuffs and restores stuff
        """
        self.player.in_control = True
        debuffs_to_remove = [
            "WoodlandDeverberrySkin"
        ]
        for item in self.player.status_effects:
            if item.name in debuffs_to_remove:
                self.player.status_effects.pop(self.player.status_effects.index(item))

    def play(self):
        """
            Main combat loop interface

            1. Add encounter start info to the update_log so it doesn't appear empty at start
            2. Loop begins
            3. Check if player dead.
            4. Check if opponent dead.
                4.1. If so, handle loot, and loot interface

            5. Render everything
            6. Player chooses command and command gets executed
            7. Opponent response
            8. Repeat until something dies.

            :return bool (if succesful or not)
        """
        #Give opponent knowledge of battlefield
        self.opponent.battlefield = self.battlefield
        self.update_log(["opponent", "{} encounters {} {}".format(self.player.name, self.opponent.before_name, self.opponent.readable_name)])
        opener = self.opponent.opener()
        if opener:
            for item in opener["combat_text"]:
                self.update_log(["opponent", item])
        self.update_log(["neutral", ""])
        k = -1
        selected_command = 0
        offset = 40

        opponent_offset = 15
        opponent_offset_y = 100
        opponent_art_offset = 2

        while k != ord("q"):
            print(self.battlefield.ground_items)
            self.screen.clear()
            if self.player.health <= 0:
                helper.popup(self.screen, self.state, ["You have died"])
                self.state.game_state = states.Intro(self.state)
                self.state.command_state = states.main_menu(self.state)
                self.state.map_screen = False
                self.state.command_state.commands[0].active = True
                self.state.player = False
                self.state.first_time = True
                break
            if self.opponent.health <= 0 and not self.opponent_killed:
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
                    "Loot and Exit",
                    "Exit"
                ]
                selected_command = 0
                self.opponent_killed = True
                # return True
            elif not self.opponent_killed:
                if not self.player.in_control:
                    self.commands = [
                        "You are not in control"
                    ]
                    selected_command = 0
                else:
                    self.commands = [
                        "Attack",
                        "Block",
                        "Spell",
                        "Item",
                    ]
                    

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

            percent_health = round(self.player.health / self.player.max_health, 2) #hur många %
            percent_lost = 1 - percent_health # hur mycket som inte är HP
            self.screen.addstr(37, 0, "HP:") #Base
            self.screen.attron(curses.color_pair(5)) # På med grönt
            self.screen.addstr(37, 5, "{}".format(" " * int(100 * percent_health))) # hela rad = 100, så typ 0.6 * 100 = 60 rutor
            self.screen.attroff(curses.color_pair(5)) #Av med grönt
            self.screen.addstr(37, 5 + int(100 * percent_health), "{}".format(" " * int(100 * percent_lost)), curses.color_pair(2)) # Adda på percent_lost efter första addstr

            for i in range(len(self.commands)):
                if i == selected_command:
                    self.screen.attron(curses.color_pair(5))
                    self.screen.addstr(offset + i, 10, self.commands[i])
                    self.screen.attroff(curses.color_pair(5))
                else:
                    self.screen.addstr(offset + i, 10, self.commands[i])

            self.screen.attron(curses.color_pair(133))
            for idx, text in enumerate(self.opponent.art):
                self.screen.addstr(opponent_art_offset + idx, opponent_offset_y, text)
            self.screen.attroff(curses.color_pair(133))

            self.screen.addstr(opponent_offset, opponent_offset_y, "Opponent: {}".format(self.opponent.readable_name))
            for i, v in enumerate(self.opponent.description):
                self.screen.addstr(opponent_offset + i + 1, opponent_offset_y, v)
            
            # Todo REWORK
            #self.screen.addstr(opponent_offset + 5, opponent_offset_y, "HP: {} / {}".format(self.opponent.health, self.opponent.max_health))
            percentage = self.opponent.health / self.opponent.max_health
            if percentage == 1:
                keyword = "Great Health"
            elif percentage >= 0.7:
                keyword = "Fine"
            elif percentage >= 0.3:
                keyword = "Damaged"
            elif percentage >= 0.1:
                keyword = "Badly injured"
            else:
                keyword = "Barely hanging on"
            self.screen.addstr(opponent_offset + 5, opponent_offset_y, f"Shape: {keyword}")

            # TODO END

            self.screen.addstr(opponent_offset + 7, opponent_offset_y, "Debuffs:")
            # allocate 6 for status effects
            for i, status in enumerate(self.opponent.status_effects):
                self.screen.attron(curses.color_pair(status.color))
                self.screen.addstr(opponent_offset + 8 + i, 120, "{} ({})".format(status.type, status.turns_left))
                self.screen.attroff(curses.color_pair(status.color))

            for i, limb in enumerate(self.opponent.limbs):

                limb_name = limb.name.capitalize()
                if limb.vital:
                    limb_name = f"*{limb_name}"
                else:
                    limb_name = f" {limb_name}"

                limb_info = f"{limb_name}: {limb.health}/{limb.max_health}"
                if limb.held_item:
                    limb_info = f"{limb_info} : {limb.held_item.readable_name}"

                if limb.alive:
                    self.screen.addstr(opponent_offset + 14 + i, opponent_offset_y, limb_info)
                else:
                    self.screen.addstr(opponent_offset + 14 + i, opponent_offset_y, limb_info, curses.color_pair(133))

            k = self.screen.getch()

            if k == curses.KEY_UP:
                if selected_command != 0:
                    selected_command -= 1
                curses.ungetch(curses.KEY_F0)

            elif k == curses.KEY_DOWN:
                if selected_command != len(self.commands) - 1:
                    selected_command += 1
                curses.ungetch(curses.KEY_F0)

            elif k == ord(" "):
                self.turn += 1
                if self.commands[selected_command] == "You are not in control":
                    self.player_attack()
                if self.commands[selected_command] == "Attack":
                    self.player_attack()

                if self.commands[selected_command] == "Block":
                    self.player.health -= 100

                if self.commands[selected_command] == "Run":
                    self.update_log(["neutral", "Attempting to run away."])
                    run_successful = self.player_run()
                    if run_successful:
                        self.remove_temp_debuffs()
                        return False

                if self.commands[selected_command] == "Spell":
                    spell = self.select_spell()
                    if spell != "False":
                        res = self.player_spell(spell)
                        if not res:
                            continue
                    else:
                        continue
                if self.commands[selected_command] == "Loot and Exit":
                    self.loot(random_loot)
                    self.remove_temp_debuffs()
                    return True

                if self.commands[selected_command] == "Exit":
                    curses.ungetch(curses.KEY_F0)
                    self.remove_temp_debuffs()
                    return True

                if not self.opponent_killed:
                    self.check_effects()
                    self.check_player_effects()
                    self.check_opponent()
                    self.update_log(["neutral", ""])
                curses.ungetch(curses.KEY_F0)
        self.remove_temp_debuffs()

    def loot(self, random_loot):
        """
            Loot interface

            :param random_loot = loot generated in monster class, specific to that mob

            :return None
        """
        k = -1
        start = 10
        offset = 15
        # random_loot = self.opponent.generate_loot()
        # if random_loot:
        #     loot_list = [helper.get_item(item)() for item in random_loot]
        # else:
        #     loot_list = []
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
                curses.ungetch(curses.KEY_F0)
            k = self.screen.getch()
        curses.ungetch(curses.KEY_F0)


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
            screen.addstr(18, 34, "Yes")
            screen.attroff(curses.color_pair(5))
            screen.addstr(18, 40, "No")
        else:
            screen.addstr(18, 34, "Yes")
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
