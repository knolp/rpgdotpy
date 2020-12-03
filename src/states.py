import sys, math
import art
import mapper
import npc
import random
import items
import abilities
import pathfinding
import monster
import battle
import events
import helper
import time
import curses
import books
import cavegen

DEBUG = True
# HELPERS #

def explain_text(text, explain_text, cols):
    return_text = text + " " * (cols - (len(text) + len(explain_text))) + explain_text
    return return_text

def center(max_w, text):
    return math.floor((max_w - len(text)) / 2) 

class MenuItem():
    def __init__(self, text, position, execute_game_state, execute_command_state, active=False):
        self.text = text
        self.position = position
        self.active = active
        self.execute_game_state = execute_game_state
        self.execute_command_state = execute_command_state

    def execute_game(self):
        return self.execute_game_state

    def execute_command(self):
        return self.execute_command_state

class main_menu_temp():
    def __init__(self, game_box, command_box):
        self.game_box = game_box
        self.command_box = command_box
        self.commands = [MenuItem("New Game", 1, NewGame_1, NewGame_1_commands),
                        MenuItem("Load Character", 2, StartGame, StartGame_commands),
                         MenuItem("Load Quicksave", 3, StartGame, StartGame_commands)]

class main_menu():
    def __init__(self, state):
        self.game_box = state.game_box
        self.command_box = state.command_box
        self.commands = [MenuItem("New Game", 1, NewGame_1, NewGame_1_commands),
                        MenuItem("Load Character", 2, False,False),
                         MenuItem("Load Quicksave", 3, StartGame, StartGame_commands)]


class NewGame_1_commands():
    def __init__(self, state):
        self.game_box = state.game_box
        self.command_box = state.command_box
        self.commands = [MenuItem("Mage", 1, NewGame_2, NewGame_2_commands), 
                        MenuItem("Rogue", 2, NewGame_2, NewGame_2_commands), 
                        MenuItem("Warrior", 3, NewGame_2, NewGame_2_commands),
                        MenuItem("Back", 4, Intro, main_menu)]

class NewGame_2_commands():
    def __init__(self, state):
        self.game_box = state.game_box
        self.command_box = state.command_box
        self.commands = [MenuItem("Starter Town", 1, NewGame_3, NewGame_3_commands), 
                        MenuItem("Orc'Theral", 2, NewGame_3, NewGame_3_commands), 
                        MenuItem("Blackcliff", 3, NewGame_3, NewGame_3_commands),
                        MenuItem("Back", 4, NewGame_1, NewGame_1_commands)]

class NewGame_3_commands():
    def __init__(self, state):
        self.game_box = state.game_box
        self.command_box = state.command_box
        self.commands = [MenuItem("Human", 1, GameMenu, GameCommands), 
                        MenuItem("Orc", 2, GameMenu, GameCommands), 
                        MenuItem("Elf", 3, GameMenu, GameCommands),
                        MenuItem("Dwarf", 4, GameMenu, GameCommands),
                        MenuItem("Back", 5, NewGame_2, NewGame_2_commands)]




class StartGame_commands():
    def __init__(self, state):
        self.game_box = state.game_box
        self.command_box = state.command_box
        self.commands = [MenuItem("Back", 1, Intro, main_menu)]


#################### GAME STATES ##########################

class BluePrint():
    def __init(self, state):
        self.game_box = state.game_box
        self.command_state = state.command_state
        self.inital_rendering = False

    def draw(self):
        pass

    def execute(self):
        pass

class Debug():
    def __init__(self, state):
        self.game_box = state.game_box
        self.command_state = state.command_state

    def draw(self):
        self.game_box.addstr(20,40, "DEBUG MENU")

    def execute(self):
        pass


class Intro_temp():
    def __init__(self, game_box, command_state):
        self.game_box = game_box
        self.command_state = command_state

    def draw(self):
        height, width = self.game_box.getmaxyx()
        text = "#############################################"
        self.game_box.addstr(10, center(width, text),text)
        text = "#                                           #"
        self.game_box.addstr(11, center(width, text),text)
        text = "#                                           #"
        self.game_box.addstr(12, center(width, text),text)
        text = "#            Welcome to RPG.PY              #"
        self.game_box.addstr(13, center(width, text),text)
        text = "#                                           #"
        self.game_box.addstr(14, center(width, text),text)
        text = "#        Select an option to right          #"
        self.game_box.addstr(15, center(width, text),text)
        text = "#             to get started                #"
        self.game_box.addstr(16, center(width, text),text)
        text = "#                                           #"
        self.game_box.addstr(17, center(width, text),text)
        text = "#                                           #"
        self.game_box.addstr(18, center(width, text),text)
        text = "#############################################"
        self.game_box.addstr(19, center(width, text),text)

    def execute(self):
        pass

class Intro():
    def __init__(self, state):
        self.game_box = state.game_box
        self.state = state

    def draw(self):
        height, width = self.game_box.getmaxyx()
        text = "#############################################"
        self.game_box.addstr(10, center(width, text),text)
        text = "#                                           #"
        self.game_box.addstr(11, center(width, text),text)
        text = "#                                           #"
        self.game_box.addstr(12, center(width, text),text)
        text = "#            Welcome to RPG.PY              #"
        self.game_box.addstr(13, center(width, text),text)
        text = "#                                           #"
        self.game_box.addstr(14, center(width, text),text)
        text = "#        Select an option to right          #"
        self.game_box.addstr(15, center(width, text),text)
        text = "#             to get started                #"
        self.game_box.addstr(16, center(width, text),text)
        text = "#                                           #"
        self.game_box.addstr(17, center(width, text),text)
        text = "#                                           #"
        self.game_box.addstr(18, center(width, text),text)
        text = "#############################################"
        self.game_box.addstr(19, center(width, text),text)

    def execute(self):
        for item in self.state.command_state.commands:
            if item.active:
                if item.text == "Load Character":
                    self.state.load_player()
                    self.state.command_state.commands[1] = MenuItem("Load Character", 2, self.state.player.location,self.state.player.location.menu_commands, active=True)
                if item.text == "Load Quicksave":
                    self.state.load_player(quicksave=True)
                    self.state.command_state.commands[1] = MenuItem("Load Character", 2, self.state.player.location,self.state.player.location.menu_commands, active=True)



class NewGame_1():
    def __init__(self, state):
        self.state = state
        self.game_box = state.game_box
        self.command_state = state.command_state
        self.explain_text_strength = " Melee power"
        self.explain_text_agility = " Melee finesse"
        self.explain_text_charisma = " Personality and speech"
        self.explain_text_intellect = " Magical potencys"
        self.explain_text_alchemy = " Brewing potions"
        self.explain_text_attunement = "Buff/debuff potency"
        self.vocation_max_health = {
            "Warrior" : 30,
            "Rogue" : 20,
            "Mage" : 20,
            "Back" : 20
        }

    def draw(self):
        height, width = self.game_box.getmaxyx()
        #self.game_box.addstr(5,40, "STARTING A NEW GAME")
        choose_text = "Choose a class"
        self.game_box.addstr(37, center(width, choose_text) , choose_text)
        for item in self.command_state.commands:
            if item.active:
                if item.text == "Rogue":
                    self.draw_rogue()
                elif item.text == "Warrior":
                    self.draw_warrior()
                elif item.text == "Mage":
                    self.draw_mage()
                elif item.text == "Back":
                    self.draw_back()

    def execute(self):
        for item in self.command_state.commands:
            if item.active:
                self.state.create_player["vocation"] = item.text
                self.state.create_player["max_health"] = self.vocation_max_health[item.text]
                self.state.create_player["health"] = self.vocation_max_health[item.text]
                self.state.create_player["spells"] = [False, False, False, False, False]
                self.state.create_player["spellbook"] = [abilities.Fireball(), abilities.GreatFireball(), abilities.WoodlandCharm(), abilities.Infest()]



    def draw_warrior(self):
        self.game_box.addstr(19,46, "Warrior:")
        self.game_box.addstr(21,10, explain_text("Strength: 6 ", self.explain_text_strength, 80), curses.color_pair(136))
        self.game_box.addstr(22,10, explain_text("Agility: 2 ", self.explain_text_agility, 80))
        self.game_box.addstr(23,10, explain_text("Charisma: 0 ", self.explain_text_charisma, 80), curses.color_pair(136))
        self.game_box.addstr(24,10, explain_text("Intellect: 0 ", self.explain_text_intellect, 80))
        self.game_box.addstr(25,10, explain_text("Alchemy: 2 ", self.explain_text_alchemy, 80), curses.color_pair(136))
        self.game_box.addstr(26,10, explain_text("Attunement: 0 ", self.explain_text_attunement, 80))
        art.draw_shield(self.game_box,2,35)

    def draw_mage(self):
        self.game_box.addstr(19,47, "Mage:")
        self.game_box.addstr(21,10, explain_text("Strength: 1 ", self.explain_text_strength, 80), curses.color_pair(136))
        self.game_box.addstr(22,10, explain_text("Agility: 1 ", self.explain_text_agility, 80))
        self.game_box.addstr(23,10, explain_text("Charisma: 3 ", self.explain_text_charisma, 80), curses.color_pair(136))
        self.game_box.addstr(24,10, explain_text("Intellect: 4 ", self.explain_text_intellect, 80))
        self.game_box.addstr(25,10, explain_text("Alchemy: 3 ", self.explain_text_alchemy, 80), curses.color_pair(136))
        self.game_box.addstr(26,10, explain_text("Attunement: 3 ", self.explain_text_attunement, 80))
        art.draw_fire(self.game_box, 2, 45)

    def draw_rogue(self):
        self.game_box.addstr(19,46, "Rogue:")
        self.game_box.addstr(21,10, explain_text("Strength: 3 ", self.explain_text_strength, 80), curses.color_pair(136))
        self.game_box.addstr(22,10, explain_text("Agility: 4 ", self.explain_text_agility, 80))
        self.game_box.addstr(23,10, explain_text("Charisma: 2 ", self.explain_text_charisma, 80), curses.color_pair(136))
        self.game_box.addstr(24,10, explain_text("Intellect: 0 ", self.explain_text_intellect, 80))
        self.game_box.addstr(25,10, explain_text("Alchemy: 4 ", self.explain_text_alchemy, 80), curses.color_pair(136))
        self.game_box.addstr(26,10, explain_text("Attunement: 0 ", self.explain_text_attunement, 80))
        art.draw_dagger(self.game_box, 2, 44)

    def draw_back(self):
        self.game_box.addstr(19,46, "BACK")

class NewGame_2():
    def __init__(self, state):
        self.state = state
        self.game_box = state.game_box
        self.command_state = state.command_state
        self.starter_town_art = [
            "                    |####                ",
            "                    |####                ",
            "      MM            |                    ",
            "     MMMM           M                    ",
            "    MMMMMM         MMM                   ",
            "   MMMMMMMM       MMMMM            M     ",
            "  MMMMMMMMMM       ###            MMM    ",
            "   ########      #######         MMMMM   ",
            "   ########   #############       ###    ",
            "   ########   #############       ###    ",
            "  ###########################   #######  ",
            " ############################# ######### ",
            "#########################################",
            "###################+++###################",
            "##################+++++##################",
            "##################     ##################",
            "##################     ##################"
        ]
        self.orctheral_art = [
            "                    |                    ",
            "                                         ",
            "                 \\  O  /                 ",
            "                   OOO                   ",
            "                - OOOOO -                ",
            "                   OOO                   ",
            "                 /  O  \\                 ",
            "        /\\                     /\\        ",
            "       /##\\         |         /##\\       ",
            "      /####\\                 /####\\      ",
            "     /##  ##\\---ooo---ooo---/##  ##\\     ",
            "    /##    ##\\             /##    ##\\    ",
            "   /##      ##\\           /##      ##\\   ",
            "  /##        ##\\   (()   /##        ##\\  ",
            " /###        ###\\  )((  /###        ###\\ ",
            "/####        ####\\ ### /####        ####\\",
            "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
        ]
        self.blackcliff_art = [
            "                                         ",
            "  ##\                                    ",
            "  ##v\                                   ",
            "  ##vv\                                  ",
            "  ##vvv\                                 ",
            "  ##vvv/                              WWW",
            "  ##vv/                              WWWW",
            "  ##v/                              WWWWW",
            "  ##/            #                 W#####",
            "###################----             ###  ",
            "##################                  ###  ",
            "###############                     #####",
            "#############                 BBBBBBBBBBB",
            "###########                   | |        ",
            "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
            "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
            "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
        ]

    def draw(self):
        height, width = self.game_box.getmaxyx()
        text = "Choose a starting area"
        self.game_box.addstr(37, center(width, text), text)
        for item in self.command_state.commands:
            if item.active:
                if item.text == "Starter Town":
                    for idx, text in enumerate(self.starter_town_art):
                        self.game_box.addstr(3 + idx, center(width, text),text)
                    text = "A basic town in the southern part of the realm"
                    self.game_box.addstr(20, center(width, text),text)
                    text = "Notable features:"
                    self.game_box.addstr(22, center(width, text),text)
                    self.game_box.attron(curses.color_pair(136))
                    text = "* Osk'Ghar the Blacksmith"
                    self.game_box.addstr(24, center(width, text),text)
                    text = "* The Grand Arena"
                    self.game_box.addstr(25, center(width, text),text)
                    text = "* The Hall of Justice"
                    self.game_box.addstr(26, center(width, text),text)
                    text = "* The temple of Mux'Ton, the god of death"
                    self.game_box.addstr(27, center(width, text), text)
                    self.game_box.attroff(curses.color_pair(136))

                if item.text == "Orc'Theral":
                    for idx, text in enumerate(self.orctheral_art):
                        self.game_box.addstr(3 + idx, center(width, text),text)
                    text = "The Orc hometown in the east"
                    self.game_box.addstr(20, center(width, text),text)
                    text = "Notable features:"
                    self.game_box.addstr(22, center(width, text),text)
                    self.game_box.attron(curses.color_pair(136))
                    text = "* The Desert of Orchai"
                    self.game_box.addstr(24, center(width, text),text)
                    text = "* The Temple of Stone"
                    self.game_box.addstr(25, center(width, text),text)
                    text = "* Hiltir Mining Corporation"
                    self.game_box.addstr(26, center(width, text),text)
                    self.game_box.attroff(curses.color_pair(136))

                if item.text == "Blackcliff":
                    for idx, text in enumerate(self.blackcliff_art):
                        self.game_box.addstr(3 + idx, center(width, text),text)
                    text = "The largest fishing colony in the west"
                    self.game_box.addstr(20, center(width, text),text)
                    text = "Notable features:"
                    self.game_box.addstr(22, center(width, text),text)
                    self.game_box.attron(curses.color_pair(136))
                    text = "* The Mage Tower"
                    self.game_box.addstr(24, center(width, text),text)
                    text = "* Blackcliff Port"
                    self.game_box.addstr(25, center(width, text),text)
                    text = "* The White Forest"
                    self.game_box.addstr(26, center(width, text),text)
                    self.game_box.attroff(curses.color_pair(136))

                if item.text == "Back":
                    text = "BACK"
                    self.game_box.addstr(20, center(width, text),text)


    def execute(self):
        for item in self.command_state.commands:
            if item.active:
                if item.text == "Starter Town":
                    self.state.create_player["location"] = "StarterTown"
                elif item.text == "Orc'Theral":
                    self.state.create_player["location"] = "StarterTown"
                elif item.text == "Blackcliff":
                    self.state.create_player["location"] = "StarterTown"


class NewGame_3():
    def __init__(self, state):
        self.state = state
        self.game_box = state.game_box
        self.command_state = state.command_state

    def draw(self):
        height, width = self.game_box.getmaxyx()
        text = "Choose a race"
        self.game_box.addstr(2, center(width, text), text)
        for item in self.command_state.commands:
            if item.active:
                if item.text == "Human":
                    self.game_box.attron(curses.color_pair(136))
                    text = "HUMAN"
                    self.game_box.addstr(6, center(width, text),text)
                    self.game_box.attroff(curses.color_pair(136))
                    text = "A recent addition to the many races of Beladir"
                    self.game_box.addstr(10, center(width, text),text)
                    text = "Once being freed from the grips of the elves"
                    self.game_box.addstr(12, center(width, text),text)
                    text = "the Humans have now settled all over the lands"
                    self.game_box.addstr(13, center(width, text),text)
                    text = "and have built up quite a reputation for themselves"
                    self.game_box.addstr(14, center(width, text),text)
                    text = "for being great service providers and merchants"
                    self.game_box.addstr(15, center(width, text),text)
                    text = "But they are not to be underestimated in combat"
                    self.game_box.addstr(18, center(width, text),text)
                    text = "Racial Profiencies:"
                    self.game_box.addstr(20, center(width, text),text)
                    self.game_box.attron(curses.color_pair(136))
                    text = "* Sneaky Tounge: Increased chance to trick people"
                    self.game_box.addstr(22, center(width, text),text)
                    text = "* Eagle Eyes: Increased perception of surroundings"
                    self.game_box.addstr(23, center(width, text),text)
                    text = "* Weak-bodied: Weakness to flesh wounds"
                    self.game_box.addstr(24, center(width, text),text)
                    self.game_box.attroff(curses.color_pair(136))

                if item.text == "Orc":
                    self.game_box.attron(curses.color_pair(136))
                    text = "ORC"
                    self.game_box.addstr(6, center(width, text),text)
                    self.game_box.attroff(curses.color_pair(136))
                    text = "The native race of the eastern parts of Beladir"
                    self.game_box.addstr(10, center(width, text),text)
                    text = "Due to extreme deforestation, the Orcs reside in a large desert"
                    self.game_box.addstr(12, center(width, text),text)
                    text = "over time this has made them reslient and fierce"
                    self.game_box.addstr(13, center(width, text),text)
                    text = "Their lands have begun to run out of resources to keep up with their"
                    self.game_box.addstr(15, center(width, text),text)
                    text = "large population and they will need to seek out new territories"
                    self.game_box.addstr(16, center(width, text),text)
                    text = "Any other race is not to be spared in this process"
                    self.game_box.addstr(18, center(width, text),text)
                    text = "Racial Profiencies:"
                    self.game_box.addstr(20, center(width, text),text)
                    self.game_box.attron(curses.color_pair(136))
                    text = "* Tough Skin: Resilient to many status effects"
                    self.game_box.addstr(22, center(width, text),text)
                    text = "* Ravager: Melee combat effiency on open plains"
                    self.game_box.addstr(23, center(width, text),text)
                    text = "* Workers Hands: Highly efficient crafters"
                    self.game_box.addstr(24, center(width, text),text)
                    text = "* Large Hands: Capable of dual-wielding two-handed weapons"
                    self.game_box.addstr(25, center(width, text),text)
                    text = "* Dry Throat: Weakness to water"
                    self.game_box.addstr(26, center(width, text),text)
                    self.game_box.attroff(curses.color_pair(136))

                if item.text == "Elf":
                    self.game_box.attron(curses.color_pair(136))
                    text = "ELF"
                    self.game_box.addstr(6, center(width, text),text)
                    self.game_box.attroff(curses.color_pair(136))
                    text = "The oldest native race in Beladir"
                    self.game_box.addstr(10, center(width, text),text)
                    text = "They have some sense of individuality, but are yet all connected"
                    self.game_box.addstr(12, center(width, text),text)
                    text = "through a state known as 'Elvish Hivemind'"
                    self.game_box.addstr(13, center(width, text), text)
                    text = "Their prophecy has not yet been completed but their spiritual"
                    self.game_box.addstr(15, center(width, text),text)
                    text = "shamans say the time is near, and the gods shall prove it"
                    self.game_box.addstr(16, center(width, text),text)
                    text = "They created the Humans in their image"
                    self.game_box.addstr(18, center(width, text),text)
                    text = "Racial Profiencies:"
                    self.game_box.addstr(20, center(width, text),text)
                    self.game_box.attron(curses.color_pair(136))
                    text = "* Nature Bond: Attuned to all gods of the land"
                    self.game_box.addstr(22, center(width, text),text)
                    text = "* Large Mind: Efficient at learning new strategies"
                    self.game_box.addstr(23, center(width, text),text)
                    text = "* Elvish Hivemind: Can occupy the minds of other Elves at will"
                    self.game_box.addstr(24, center(width, text),text)
                    text = "* Arcane Deficiency: Weakness to the Arcane arts"
                    self.game_box.addstr(25, center(width, text),text)
                    self.game_box.attroff(curses.color_pair(136))

                if item.text == "Dwarf":
                    self.game_box.attron(curses.color_pair(136))
                    text = "DWARF"
                    self.game_box.addstr(6, center(width, text),text)
                    self.game_box.attroff(curses.color_pair(136))
                    text = "Another recent refugee in the lands of Beladir"
                    self.game_box.addstr(10, center(width, text),text)
                    text = "This race of deep cave dwellers came to these lands"
                    self.game_box.addstr(12, center(width, text),text)
                    text = "after the sundering of their own homelands."
                    self.game_box.addstr(13, center(width, text),text)
                    text = "Once a proudly religious culture that is now starting to fear"
                    self.game_box.addstr(15, center(width, text),text)
                    text = "that the gods have abandonded them in their journey for a new home"
                    self.game_box.addstr(16, center(width, text),text)
                    text = "Racial Profiencies:"
                    self.game_box.addstr(20, center(width, text),text)
                    self.game_box.attron(curses.color_pair(136))
                    text = "* Pale Skin: Immune to some diseases"
                    self.game_box.addstr(22, center(width, text),text)
                    text = "* Abandoned: Has no obligation to any native gods"
                    self.game_box.addstr(23, center(width, text),text)
                    text = "* Murky Eyes: Efficient at combat in the dark"
                    self.game_box.addstr(24, center(width, text),text)
                    text = "* Deep Dweller: Native food may cause problems"
                    self.game_box.addstr(25, center(width, text),text)
                    text = "* Vertically Handicapped: Surface Travel takes longer"
                    self.game_box.addstr(26, center(width, text),text)
                    self.game_box.attroff(curses.color_pair(136))

                if item.text == "Back":
                    text = "BACK"
                    self.game_box.addstr(20, center(width, text),text)

    def execute(self):
        just_exit = False
        for item in self.command_state.commands:
            if item.active:
                if item.text != "Back":
                    self.state.create_player["race"] = item.text
                else:
                    just_exit = True
        if just_exit:
            pass

        else:
            name = helper.input_text(self.state.game_box,["Choose a name:"], self.state)
            self.state.create_player["name"] = name
            self.state.create_player["flags"] = []
            self.state.make_player()

            self.state.game_box.clear()
            self.state.command_box.clear()
            self.state.game_box.refresh()
            self.state.command_box.refresh()





class StartGame():
    def __init__(self, state):
        self.game_box = state.game_box
        self.command_state = state.command_state

    def draw(self):
        self.game_box.addstr(20,40,"STARTGAME")

    def execute(self):
        pass



#####################################################################

 #                       GAME COMMAND STATES

#####################################################################

class GameCommands():
    def __init__(self, state):
        self.game_box = state.game_box
        self.command_box = state.command_box
        self.state = state
        self.commands = [MenuItem("Inventory", 1,Inventory, InventoryCommands), 
                        MenuItem("Skills", 2, False, False), 
                        MenuItem("Save", 3, False, False),
                        MenuItem("Quit", 4, False, False)]


class GameMenu():
    def __init__(self, state):
        self.state = state

    def draw(self):
        self.state.game_box.addstr(2,2, "Character Information:")
        self.state.game_box.addstr(3,2,self.state.player.name)
        self.state.game_box.addstr(4,2, "{} {}".format(self.state.player.race, self.state.player.vocation))
        self.state.game_box.addstr(5,2,self.state.player.location.name)
        self.state.game_box.addstr(6,2, "{} / {} HP".format(self.state.player.health, self.state.player.max_health))

        start = 10

        #self.state.game_box.addstr(8,2, "Flags:")
        #for item in self.state.player.flags:
        #	self.state.game_box.addstr(start, 2, item)
        #	start += 1

        self.state.game_box.addstr(start, 2, "Status Effects")
        start += 2
        for item in self.state.player.status_effects:
            self.state.game_box.addstr(start, 4, f"{item.readable_name}: {item.description}")
            start += 1

        start += 1

    def execute(self):
        for item in self.state.command_state.commands:
            if item.active:
                if item.text == "Save":
                    self.state.save_player()


class IngameMenu():
    def __init__(self, state):
        self.game = True
        self.game_box = state.game_box
        self.command_box = state.command_box
        self.commands = [MenuItem("1: Attack", 1, False, False), 
                        MenuItem("P: Spellbook", 2, False, False), 
                        MenuItem("I: Inventory", 3, False, False),
                        MenuItem("E: Equipment", 4, False, False),
                        MenuItem("Space: Action", 5, False, False),
                        MenuItem("Tab: Menu", 6, False, False)]


class InventoryCommands():
    def __init__(self, state):
        self.game_box = state.game_box
        self.command_box = state.command_box
        self.commands = [MenuItem("Inventory", 1, False, False), 
                        MenuItem("Inventory", 2, False, False), 
                        MenuItem("Inventory", 3, False, False),
                        MenuItem("Back", 4, GameMenu, GameCommands)]


class Inventory():
    def __init__(self, state):
        self.game_box = state.game_box
        state.map_screen = False
        self.command_state = state.command_state

    def draw(self):
        height, width = self.game_box.getmaxyx()
        text = "#############################################"
        self.game_box.addstr(10, center(width, text),text)
        text = "#                                           #"
        self.game_box.addstr(11, center(width, text),text)
        text = "#                                           #"
        self.game_box.addstr(12, center(width, text),text)
        text = "#                                           #"
        self.game_box.addstr(13, center(width, text),text)
        text = "#                                           #"
        self.game_box.addstr(14, center(width, text),text)
        text = "#                 INVENTORY                 #"
        self.game_box.addstr(15, center(width, text),text)
        text = "#                                           #"
        self.game_box.addstr(16, center(width, text),text)
        text = "#                                           #"
        self.game_box.addstr(17, center(width, text),text)
        text = "#                                           #"
        self.game_box.addstr(18, center(width, text),text)
        text = "#############################################"
        self.game_box.addstr(19, center(width, text),text)

    def execute(self):
        pass



#####################################################################

 #                       GAME MAP STATES 

#####################################################################

class MapState():
    def __init__(self, state):
        self.state = state
        self.fov = False
        self.cave = False

    def check_events(self):
        print("NOT IMPLETMENTED")
        print(self.state.game_map)

    def draw(self):
        if self.state.player.phaseshift:
            self.game_map.draw_map(self.state, inverted=True)    
        else:
            self.game_map.draw_map(self.state)


class StarterTown(MapState):
    name = "Starter Town"
    raw_name = "StarterTown"
    menu_commands = GameCommands
    objects = [
            npc.ErolKipman(13, 37),
        ]
    game_map = mapper.GameMap("map1.txt", objects)

    def __init__(self, state):
        super().__init__(state)
        if state.first_time == True:
            state.change_map_screen()
            state.first_time = False
        objects = [
            npc.ErolKipman(15, 58),
        ]
        self.game_map = mapper.GameMap("map1.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu
        self.random_monsters = [monster.Rat]
        self.turn = 0

    def draw(self):
        if self.state.player.phaseshift:
            self.game_map.draw_map(self.state, inverted=True)    
        else:
            self.game_map.draw_map(self.state)
        #self.game_map.draw_vision(self.state, self.state.game_box)

    def execute(self):
        pass

    def check_events(self):
        for item in self.game_map.objects:
            if not item.check_inbound():
                self.game_map.objects.pop(self.game_map.objects.index(item))
            item.turn_action()
        if self.state.player.turn % 2 == 0:
            smoke = npc.Smoke(11,50)
            self.game_map.objects.append(smoke)

        # Check door
        if self.state.player.x == 17 and self.state.player.y == 47:
            events.StarterTown_door(self.state)
        elif self.state.player.x == 1:
            events.StarterTown_north(self.state)
        elif self.state.player.y == 1:
            events.StarterTown_west(self.state)

        if self.state.player.x == 8 and self.state.player.y == 73:
            events.StarterTown_haunted_house_entrance(self.state)

        # Check NPCs
        #for npc in self.game_map.objects:
        #    if self.state.player.x == npc.x and self.state.player.y == npc.y:
        #        self.state.action = "Talk"
        #        break
        #    else:
        #        self.state.action = "None"

class StarterTown_house(MapState):
    name = "Starter Town House"
    raw_name = "StarterTown_house"
    menu_commands = GameCommands
    objects = [
        npc.OskGhar(16,52)
        ]
    game_map = mapper.GameMap("map2.txt", objects)

    def __init__(self, state):
        super().__init__(state)
        if state.first_time == True:
            state.change_map_screen()
            state.first_time = False
        objects = [
            npc.WoodenChest(15,45,"OskGhar_reward_chest",[
                items.RatSmasher()
            ],
            requirement="RatMenace_reward"),
            npc.OskGhar(16,52)
        ]
        self.game_map = mapper.GameMap("map2.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu


    def draw(self):
        if self.state.player.phaseshift:
            self.game_map.draw_map(self.state, inverted=True)    
        else:
            self.game_map.draw_map(self.state)

    def execute(self):
        pass

    def check_events(self):
        if self.state.player.x == 24 and self.state.player.y == 47:
            events.StarterTown_house_door(self.state)

        if self.state.player.x == 13 and self.state.player.y == 32:
            events.StarterTown_house_basement_door_entrance(self.state)


class StarterTown_house_basement(MapState):
    name = "Starter Town House Basement"
    raw_name = "StarterTown_house_basement"
    menu_commands = GameCommands
    objects = [
        npc.BasementLever(14,62),
        npc.BasementLever(14,73),
        npc.Rock(19,68)
        ]
    game_map = mapper.GameMap("StarterTown_house_basement.txt", objects)

    def __init__(self, state):
        super().__init__(state)
        if state.first_time == True:
            state.change_map_screen()
            state.first_time = False
        objects = [
            npc.BasementLever(14,62),
            npc.BasementLever(14,73),
            npc.Rock(19,68),
        ]

        if "RatMenace_rat1_killed" not in state.player.flags:
            objects.append(npc.Rat(27,77, state,  flag="RatMenace_rat1_killed", radar=True))

        if "RatMenace_rat2_killed" not in state.player.flags:
            objects.append(npc.Rat(30,88, state, flag="RatMenace_rat2_killed", radar=True))

        if "RatMenace_rat3_killed" not in state.player.flags:
            objects.append(npc.Rat(32,79, state, flag="RatMenace_rat3_killed", radar=True))

        self.game_map = mapper.GameMap("StarterTown_house_basement.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu

        self.fov = True

    def draw(self):
        self.game_map.draw_vision(self.state, self.state.game_box)

    def execute(self):
        pass

    def check_events(self):

        list_of_objects = [item.name for item in self.game_map.objects]

        if self.state.player.x == 24 and self.state.player.y == 47:
            events.StarterTown_house_basement_door_exit(self.state)

        if self.state.player.x == 37 and self.state.player.y == 83:
            events.StarterTown_house_basement_door_to_hallway_entrance(self.state)
        
        if self.state.player.x == 19 and self.state.player.y == 68 and "Rock" in list_of_objects:
            for item in self.game_map.objects:
                if item.name == "Rock":
                    item.action(self.state.game_box, self.state)
                    self.state.player.x, self.state.player.y = self.state.player.last_pos

        # if self.state.player.x == 27 and self.state.player.y == 77 and "Rat" in list_of_objects:
        # 	for item in self.game_map.objects:
        # 		if item.name == "Rat":
        # 			if item.x == 27 and item.y == 77:
        # 				item.action()
        # 				self.state.player.flags.append("RatMenace_rat1_killed")
        # 				self.game_map.objects.remove(item)

        # if self.state.player.x == 30 and self.state.player.y == 88 and "Rat" in list_of_objects:
        # 	for item in self.game_map.objects:
        # 		if item.name == "Rat":
        # 			if item.x == 30 and item.y == 88:
        # 				item.action()
        # 				self.state.player.flags.append("RatMenace_rat2_killed")
        # 				self.game_map.objects.remove(item)

        # if self.state.player.x == 32 and self.state.player.y == 79 and "Rat" in list_of_objects:
        # 	for item in self.game_map.objects:
        # 		if item.name == "Rat":
        # 			if item.x == 32 and item.y == 79:
        # 				result = item.action()
        # 				if result == True:
        # 					self.state.player.flags.append("RatMenace_rat3_killed")
        # 					self.game_map.objects.remove(item)
        # 				else:
        # 					self.state.player.x = 31


class StarterTown_house_basement_hallway(MapState):
    """
        TOP FLOOR, EMPTY ROOM
    """
    name = "Starter Town House Basement Hallway"
    raw_name = "StarterTown_house_basement_hallway"
    menu_commands = GameCommands
    objects = [
        ]
    game_map = mapper.GameMap("StarterTown_house_basement_hallway.txt", objects)

    def __init__(self, state):
        super().__init__(state)
        if state.first_time == True:
            state.change_map_screen()
            state.first_time = False
        objects = [
            npc.WoodenChest(7,10,"BasementChest", [items.Rapier(), items.MoonlightSword()])
        ]
        if "RatMenace_rat_king_killed" not in state.player.flags:
            objects.append(npc.RatKing(30, 45, state))


        self.game_map = mapper.GameMap("StarterTown_house_basement_hallway.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu

        self.fov = True


    def draw(self):
        self.game_map.draw_vision(self.state, self.state.game_box)
        #self.game_map.draw_map(self.state.game_box)

    def execute(self):
        pass

    def check_events(self):
        list_of_objects = [item.name for item in self.game_map.objects]

        if self.state.player.x == 1 and self.state.player.y == 83:
            events.StarterTown_house_basement_hallway_door_exit(self.state)
        
        if self.state.player.x == 30 and self.state.player.y == 45 and "RatKing" in list_of_objects:
            for item in self.game_map.objects:
                if item.name == "RatKing":
                    result = item.action()
                    if result == True:
                        self.state.player.flags.append("RatMenace_rat_king_killed")
                        self.game_map.objects.remove(item)
                    else:
                        self.state.player.x = 29


class StarterTown_haunted_house_1(MapState):
    """
        Before falling down the hole
    """
    name = "Haunted House"
    raw_name = "StarterTown_haunted_house_1"
    menu_commands = GameCommands
    objects = []
    game_map = mapper.GameMap("StarterTown_haunted_house_1.txt", objects)

    def __init__(self, state):
        super().__init__(state)
        if state.first_time == True:
            state.change_map_screen()
            state.first_time = False
        objects = [
        ]
        self.game_map = mapper.GameMap("StarterTown_haunted_house_1.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu

        self.fov = True


    def draw(self):
        self.game_map.draw_vision(self.state, self.state.game_box)

    def execute(self):
        pass

    def check_events(self):
        if self.state.player.x == 24 and self.state.player.y == 47:
            events.StarterTown_haunted_house_exit(self.state)

        if (self.state.player.x, self.state.player.y) in [(16,45),(16,46),(16,47),(17,44),(17,45),(17,46),(17,47),(17,48),(18,46),(18,47),(18,48)]:
            events.StarterTown_haunted_house_hole_entrance(self.state)

class StarterTown_haunted_house_2(MapState):
    """
        After Falling down hole
    """
    name = "Haunted House"
    raw_name = "StarterTown_haunted_house_2"
    menu_commands = GameCommands
    objects = []
    game_map = mapper.GameMap("StarterTown_haunted_house_1.txt", objects)

    def __init__(self, state):
        super().__init__(state)
        if state.first_time == True:
            state.change_map_screen()
            state.first_time = False
        objects = [
            npc.SkeletonGrunt(12,64, self.state),
            npc.SkeletonGrunt(18,66, self.state),
            npc.DeverBerries(6,17, self.state)
        ]
        if "HauntedHouse_skeleton_1" not in self.state.player.flags:
            objects.append(npc.SkeletonGrunt(6,43, self.state))
        self.game_map = mapper.GameMap("StarterTown_haunted_house_2.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu

        self.fov = True


    def draw(self):
        self.game_map.draw_vision(self.state, self.state.game_box)

    def execute(self):
        pass

    def check_events(self):
        if self.state.player.x == 29 and self.state.player.y == 66:
            events.StarterTown_haunted_house_2_dungeon_door_left(self.state)
        if self.state.player.x == 29 and self.state.player.y == 82:
            events.StarterTown_haunted_house_2_dungeon_door_right(self.state)
        if self.state.player.x == 1 and self.state.player.y == 72:
            events.StarterTown_haunted_house_3_entrance(self.state)


class StarterTown_haunted_house_3(MapState):
    """
        After Falling down hole
    """
    name = "Haunted House"
    raw_name = "StarterTown_haunted_house_3"
    menu_commands = GameCommands
    objects = []
    game_map = mapper.GameMap("StarterTown_haunted_house_3.txt", objects)

    def __init__(self, state):
        super().__init__(state)
        if state.first_time == True:
            state.change_map_screen()
            state.first_time = False
        objects = [
        ]
        self.game_map = mapper.GameMap("StarterTown_haunted_house_3.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu

        self.fov = True


    def draw(self):
        self.game_map.draw_vision(self.state, self.state.game_box)

    def execute(self):
        pass

    def check_events(self):
        if self.state.player.x == 37 and self.state.player.y == 72:
            events.StarterTown_haunted_house_3_back_exit(self.state)
        if self.state.player.x == 21 and self.state.player.y == 14:
            if "StarterTown_sewer_door_unlocked" not in self.state.player.flags:
                self.state.player.flags.append("StarterTown_sewer_door_unlocked")
            events.StarterTown_haunted_house_3_sewer_exit(self.state)





class GreenForest(MapState):
    name = "Green Forest"
    raw_name = "GreenForest"
    menu_commands = GameCommands
    objects = []
    game_map = mapper.GameMap("GreenForest.txt", objects)


    def __init__(self, state):
        super().__init__(state)
        if state.first_time == True:
            state.change_map_screen()
            state.first_time = False
        objects = [
            npc.AriamBush(32,65,state,"StarterTown_ariam_bush"),
            npc.ErolKipman(30,36),
            npc.ErolKipman(30,55)
        ]
        self.first_time = True
        self.game_map = mapper.GameMap("GreenForest.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu


    def draw(self):
        if self.state.player.phaseshift:
            self.game_map.draw_map(self.state, inverted=True)    
        else:
            self.game_map.draw_map(self.state)
        self.state.stdscr.addstr(11,72,"H.O.J", curses.color_pair(151))

    def execute(self):
        pass

    def check_events(self):
        if self.state.player.x == 37:
            events.GreenForest_south(self.state)
        if self.state.player.y == 1:
            events.GreenForest_west(self.state)
        # BROWN BEAR INN
        
        if self.state.player.x == 10 and self.state.player.y == 21:
            events.GreenForest_brown_bear_inn_entrance(self.state)

        if self.state.player.x == 10 and self.state.player.y == 22:
            helper.popup(self.state.stdscr, self.state, [
                "[Brown Bear Inn]",
                "",
                "Come inside and have a drink or rent a room for the night"
                ])
            self.state.player.x, self.state.player.y = self.state.player.last_pos

        # HALL OF JUSTICE

        if self.state.player.x == 14 and self.state.player.y in [72,73]:
            events.GreenForest_hall_of_justice_entrance(self.state)
        
        if self.state.player.x == 14 and self.state.player.y == 74:
            helper.popup(self.state.stdscr, self.state, [
                "[Hall of Justice]",
                "",
                "For all your goverment needs."
                ])
            self.state.player.x, self.state.player.y = self.state.player.last_pos


        # PLAYER HOUSE
        if self.state.player.x == 24 and self.state.player.y == 31:
            if "StarterTown_house_bought" in self.state.player.flags:
                events.GreenForest_player_house_entrance(self.state)
            else:
                helper.popup(self.state.stdscr, self.state,[
                    "The door is locked.",
                    "",
                    "You do not have the required [key]."
                ])
                self.state.player.x, self.state.player.y = self.state.player.last_pos

        if self.state.player.x == 24 and self.state.player.y == 32:
            if "StarterTown_house_bought" not in self.state.player.flags:
                text = [
                    "House for sale.",
                    "",
                    "Speak to us at the [Hall of Justice] for purchase.",
                    "",
                    "Regards,",
                    "[Becca Lithe]"
                ]
            else:
                text = [
                    "",
                    "",
                    f"  {self.state.player.name}'s House"
                ]
            helper.popup(self.state.stdscr, self.state, text)
            self.state.player.x, self.state.player.y = self.state.player.last_pos

        # TANNER
        if self.state.player.x == 24 and self.state.player.y == 11:
            events.GreenForest_tanner_entrance(self.state)
        if self.state.player.x == 24 and self.state.player.y == 12:
            helper.popup(self.state.stdscr, self.state, [
                "[Tannery of Didric Burton]",
                "",
                "Renowned Tanner and Master Craftsman.",
                "",
                "Banned people:",
                "[Abyrro Quatz] and anybody else from the magic guild."
                ])
            self.state.player.x, self.state.player.y = self.state.player.last_pos

        #Sewer back entrance:
        if self.state.player.x == 21 and self.state.player.y == 86:
            if "StarterTown_sewer_door_unlocked" not in self.state.player.flags:
                helper.popup(self.state.stdscr, self.state, [
                    "This seems to be locked from the inside."
                ])
                self.state.player.x, self.state.player.y = self.state.player.last_pos
            else:
                events.GreenForest_sewer_entrance(self.state)

class BrownBearInn(MapState):
    name = "Brown Bear Inn"
    raw_name = "BrownBearInn"
    menu_commands = GameCommands
    objects = []
    game_map = mapper.GameMap("BrownBearInn.txt", objects)


    def __init__(self, state):
        super().__init__(state)
        if state.first_time == True:
            state.change_map_screen()
            state.first_time = False
        objects = [
        ]
        if "WakeUpCall_done" not in self.state.player.flags:
            objects.append(npc.EvanKripter(19,31))
            objects.append(npc.BaldirKragg(19,17))
            objects.append(npc.BodvarKragg(23,17))
            objects.append(npc.LarsMagnus(23,35))
        if "AbyrroQuatz_hides_completed" not in self.state.player.flags:
            self.abyrro = npc.AbyrroQuatz(30,33)
            objects.append(self.abyrro)
        self.first_time = True
        self.game_map = mapper.GameMap("BrownBearInn.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu

        #event stuff
        self.abyrro_path = []
        if "BrownBearInn_event_started" not in self.state.player.flags:
            self.abyrro.quest = True
            self.state.able_to_move = False
            self.abyrro_path = [(30,33),(31,33), (32,33)]
            for i in range(34,50):
                self.abyrro_path.append((32,i))
            backwards = self.abyrro_path[::-1]
            self.abyrro_path.append("action")
            self.abyrro_path.extend(backwards)
            self.abyrro_path_length = len(self.abyrro_path)
            self.state.player.flags.append("BrownBearInn_event_started")
            curses.halfdelay(1)


    def draw(self):
        if self.state.player.phaseshift:
            self.game_map.draw_map(self.state, inverted=True)    
        else:
            self.game_map.draw_map(self.state)

    def execute(self):
        pass

    def check_events(self):
        if "BrownBearInn_event_started" in self.state.player.flags and "BrownBearInn_event_done" not in self.state.player.flags:
            if not self.abyrro_path:
                self.state.player.flags.append("BrownBearInn_event_done")
                
                curses.nocbreak()
                curses.ungetch(curses.KEY_F0)
            else:
                abyrro_pos = self.abyrro_path.pop(0)
                if abyrro_pos == "action":
                    self.abyrro.quest = False
                    self.state.able_to_move = True
                    self.abyrro.action(self.state.stdscr, self.state)
                else:
                    self.abyrro.x, self.abyrro.y = abyrro_pos
        if self.state.player.x == 34 and self.state.player.y == 49:
            events.BrownBearInn_exit(self.state)


class HallOfJustice(MapState):
    name = "Hall of Justice"
    raw_name = "HallOfJustice"
    menu_commands = GameCommands
    objects = []
    game_map = mapper.GameMap("HallOfJustice.txt", objects)


    def __init__(self, state):
        super().__init__(state)
        if state.first_time == True:
            state.change_map_screen()
            state.first_time = False
        objects = [
            npc.BeccaLithe(21,17)
        ]
        self.first_time = True
        self.game_map = mapper.GameMap("HallOfJustice.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu


    def draw(self):
        if self.state.player.phaseshift:
            self.game_map.draw_map(self.state, inverted=True)    
        else:
            self.game_map.draw_map(self.state)

    def execute(self):
        pass

    def check_events(self):
        if self.state.player.x == 34 and self.state.player.y == 48:
            events.HallOfJustice_exit(self.state)

        if self.state.player.x in [20,21,22,23] and self.state.player.y == 15 and self.state.check_action:
            for item in self.game_map.objects:
                if item.name == "Becca Lithe":
                    item.action(self.state.game_box, self.state)
        if self.state.player.x == 26 and self.state.player.y == 10 and self.state.check_action:
            helper.popup(self.state.stdscr, self.state, [
                "Office of [Becca Lite]",
                "Head of Starter Town real-estate."
            ])

class StarterTownPlayerHouse(MapState):
    name = "Starter Town Player House"
    raw_name = "StarterTownPlayerHouse"
    menu_commands = GameCommands
    objects = []
    game_map = mapper.GameMap("StarterTownPlayerHouse.txt", objects)


    def __init__(self, state):
        super().__init__(state)
        if state.first_time == True:
            state.change_map_screen()
            state.first_time = False
        objects = []
        patches = []
        patch_number = 0
        for i in range(80,91,2):
            for j in range(4,12):
                patches.append((j,i ,f"Farming_patch_{patch_number}"))
                patch_number += 1
        if "StarterTown_house_herb_patch" in state.player.flags:
            ids = [x[0] for x in state.player.active_farms]
            time = [x[2] + x[4] for x in state.player.active_farms]
            for item in patches:
                if item[2] in ids:
                    if time[ids.index(item[2])] <= state.timer.tid:
                        objects.append(npc.FarmingPatch(item[0], item[1], state, item[2], color=155))
                    else:
                        objects.append(npc.FarmingPatch(item[0], item[1], state, item[2], color=154))
                else:
                    objects.append(npc.FarmingPatch(item[0], item[1], state, item[2], color=153))
        if "StarterTown_house_alchemy_table" in state.player.flags:
            objects.append(npc.AlchemyTable(16, 75, state))
        if "StarterTown_house_alchemy_table" in state.player.flags:
            objects.append(npc.Juicer(16,74, state))
        self.first_time = True
        self.game_map = mapper.GameMap("StarterTownPlayerHouse.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu


    def draw(self):
        self.game_map.draw_map(self.state)

    def execute(self):
        pass

    def check_events(self):
        for item in self.game_map.objects:
            if item.name == "FarmingPatch":
                if item.identity in [x[0] for x in self.state.player.active_farms]:
                    for plant in self.state.player.active_farms:
                        if item.identity == plant[0]:
                            if plant[2] + plant[4] <= self.state.timer.tid:
                                item.color = 155
                            else:
                                item.color = 154
                else:
                    item.color = 153
        if self.state.player.x == 18 and self.state.player.y == 75 and self.state.check_action:
            for item in self.game_map.objects:
                if item.name == "AlchemyTable":
                    item.action(self.state.stdscr, self.state)

        elif self.state.player.x == 18 and self.state.player.y == 74 and self.state.check_action:
            for item in self.game_map.objects:
                if item.name == "Juicer":
                    item.action(self.state.stdscr, self.state)

        elif self.state.player.x == 34 and self.state.player.y == 48:
            events.StarterTown_player_house_exit(self.state)

class TannerHouse(MapState):
    name = "Tanner"
    raw_name = "TannerHouse"
    menu_commands = GameCommands
    objects = []
    game_map = mapper.GameMap("tanner.txt", objects)


    def __init__(self, state):
        super().__init__(state)
        if state.first_time == True:
            state.change_map_screen()
            state.first_time = False
        objects = [
            npc.DidricBurton(18,32)
        ]
        self.first_time = True
        self.game_map = mapper.GameMap("tanner.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu


    def draw(self):
        if self.state.player.phaseshift:
            self.game_map.draw_map(self.state, inverted=True)    
        else:
            self.game_map.draw_map(self.state)


    def execute(self):
        pass

    def check_events(self):
        if self.state.player.x == 26 and self.state.player.y == 47:
            events.GreenForest_tanner_exit(self.state)





class TradeDistrict(MapState):
    name = "Trade District"
    raw_name = "TradeDistrict"
    menu_commands = GameCommands
    objects = []
    game_map = mapper.GameMap("TradeDistrict.txt", objects)


    def __init__(self, state):
        super().__init__(state)
        if state.first_time == True:
            state.change_map_screen()
            state.first_time = False
        objects = [
        ]
        self.first_time = True
        self.game_map = mapper.GameMap("TradeDistrict.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu


    def draw(self):
        if self.state.player.phaseshift:
            self.game_map.draw_map(self.state, inverted=True)    
        else:
            self.game_map.draw_map(self.state)


    def execute(self):
        pass

    def check_events(self):
        if self.state.player.y == 96:
            events.TradeDistrict_east(self.state)
        if self.state.player.y == 1:
            events.go_west(self.state,"StarterTownLeftWall")
        elif self.state.player.x == 37:
            events.TradeDistrict_south(self.state)
        if self.state.player.x == 19 and self.state.player.y == 20:
            events.TradeDistrict_alchemist_entrance(self.state)


class TradeDistrictAlchemist(MapState):
    name = "Trade District (Alchemist)"
    raw_name = "TradeDistrictAlchemist"
    menu_commands = GameCommands
    objects = []
    game_map = mapper.GameMap("TradeDistrict_alchemist.txt", objects)


    def __init__(self, state):
        super().__init__(state)
        if state.first_time == True:
            state.change_map_screen()
            state.first_time = False
        objects = [
            npc.EmpaLinka(19,32),
            npc.SingleBookCase(14,45, state, books.BasicAlchemy()),
            npc.EmptyBookCase(14,46,state,[
                "You do not see any interesting books here."
            ])
        ]
        self.first_time = True
        self.game_map = mapper.GameMap("TradeDistrict_alchemist.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu


    def draw(self):
        if self.state.player.phaseshift:
            self.game_map.draw_map(self.state, inverted=True)    
        else:
            self.game_map.draw_map(self.state)

    def execute(self):
        pass

    def check_events(self):
        if self.state.player.x == 24 and self.state.player.y == 47:
            events.TradeDistrict_alchemist_exit(self.state)
        if self.state.player.x == 15 and self.state.check_action:
            for item in self.game_map.objects:
                if item.x == 14 and item.y == self.state.player.y:
                    item.action(self.state.stdscr, self.state)
        if (self.state.player.x, self.state.player.y) in [(18,35),(19,35),(20,35)] and self.state.check_action:
            for item in self.game_map.objects:
                if item.name == "Empa Linka":
                    item.action(self.state.game_box, self.state)
            

class HuntersCamp(MapState):
    name = "Forest (Hunters Camp)"
    raw_name = "HuntersCamp"
    menu_commands = GameCommands
    objects = []
    game_map = mapper.GameMap("HuntersCamp.txt", objects)


    def __init__(self, state):
        super().__init__(state)
        if state.first_time == True:
            state.change_map_screen()
            state.first_time = False
        objects = [
        ]
        self.first_time = True
        self.game_map = mapper.GameMap("HuntersCamp.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu


    def draw(self):
        if self.state.player.phaseshift:
            self.game_map.draw_map(self.state, inverted=True)    
        else:
            self.game_map.draw_map(self.state)

    def execute(self):
        pass

    def check_events(self):
        if self.state.player.x == 1:
            events.HuntersCamp_north(self.state)
        elif self.state.player.y == 96:
            events.HuntersCamp_east(self.state)
        elif self.state.player.x == 11 and self.state.player.y in [43,44]:
            events.RandomCave(self.state, target = [events.RandomCave, [events.RandomCave, events.StarterTown_door]])
        elif self.state.player.y == 1:
            events.go_west(self.state,"StarterTownDocks")

class RandomCave(MapState):
    name = "Randomly generated cave"
    raw_name = "RandomCave"
    menu_commands = GameCommands
    objects = []
    #game_map = mapper.GameMap("test.txt", objects)


    def __init__(self, state, target):
        super().__init__(state)
        if state.first_time == True:
            state.change_map_screen()
            state.first_time = False
        objects = [
        ]
        self.first_time = True
        self.cave_dict = cavegen.create_map(state.player.seed)
        self.state.player.x, self.state.player.y = self.cave_dict["player_pos"][0] + 1, self.cave_dict["player_pos"][1] + 1
        self.door_pos = self.cave_dict["door_pos"][0] + 1, self.cave_dict["door_pos"][1] + 1
        self.game_map = mapper.GameMap(self.cave_dict["map"], objects, file=False)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu
        self.fov = True
        self.cave = True
        self.target = target
        self.free_squares = []
        for x in range(len(self.cave_dict["raw_map"])):
            for y in range(len(self.cave_dict["raw_map"][0])):
                if self.cave_dict["raw_map"][x][y] == 0:
                    self.free_squares.append((y,x))
        for i in range(4):
            pos = random.choice(self.free_squares)
            objects.append(npc.Rat(pos[1] + 1, pos[0] + 1, self.state, radar=True))


    def draw(self):
        #if self.state.player.phaseshift:
        #    self.game_map.draw_map(self.state, inverted=True)    
        #else:
        #    self.game_map.draw_map(self.state)
        self.game_map.draw_vision(self.state, self.state.game_box, draw_seen=False)

    def execute(self):
        pass

    def check_events(self):
        monsters = [x for x in self.game_map.objects if x.type == "monster"]
        if DEBUG:
            start_time = time.time()
        for monster in monsters:
            if monster.visible: #If we can see the monster
                monster.path = []
                path = cavegen.pathfind(self.cave_dict["raw_map"], (monster.x - 1, monster.y - 1), (self.state.player.y - 1, self.state.player.x - 1))
                monster.path_to_target = path[1:]
            else: #If we cannot see the monster
                monster.path_to_target = []
                monster.x += random.randint(-1, 1)
                monster.y += random.randint(-1, 1)
                continue
            if not monster.path: #If the monster does not have a full path
                path = cavegen.pathfind(self.cave_dict["raw_map"], (monster.x - 1, monster.y - 1), (random.choice(self.free_squares)))
                monster.path = path.copy()
            if monster.path and not monster.path_to_target:
                monster.x, monster.y = monster.path[0][0] + 1, monster.path[0][1] + 1
                monster.path.pop(0)
            if monster.path_to_target:
                if self.state.player.turn % monster.speed == 0:
                    break
                monster.x, monster.y = monster.path_to_target[0][0] + 1, monster.path_to_target[0][1] + 1
                monster.path_to_target.pop(0)
        if DEBUG:
            self.state.log_info(f"Time elapsed for monster-loop = {time.time() - start_time}")

        if (self.state.player.x, self.state.player.y) == self.door_pos:
            if not type(self.target) == type([]):
                self.target(self.state)
            else:
                self.target[0](self.state, self.target[1])
            #current_module = __import__(__name__)
            #self.state.player.location = getattr(current_module, self.target[0])
            #self.state.player.x, self.state.player.y = self.target[1],self.target[2]
            #self.state.update_map()

class StarterTownDocks(MapState):
    name = "Docks"
    raw_name = "StarterTownDocks"
    menu_commands = GameCommands
    objects = []
    game_map = mapper.GameMap("StarterTownDocks.txt", objects)


    def __init__(self, state):
        super().__init__(state)
        if state.first_time == True:
            state.change_map_screen()
            state.first_time = False
        objects = [
            npc.EdwardGryll(17,14)
        ]
        self.first_time = True
        self.game_map = mapper.GameMap("StarterTownDocks.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu


    def draw(self):
        if self.state.player.phaseshift:
            self.game_map.draw_map(self.state, inverted=True)    
        else:
            self.game_map.draw_map(self.state)

    def execute(self):
        pass

    def check_events(self):
        if self.state.player.y == 96:
            events.go_east(self.state,"HuntersCamp")
        if self.state.player.x == 1:
            events.go_north(self.state,"StarterTownLeftWall")


class StarterTownLeftWall(MapState):
    name = "Left Wall"
    raw_name = "StarterTownLeftWall"
    menu_commands = GameCommands
    objects = []
    game_map = mapper.GameMap("StarterTown_left_wall.txt", objects)


    def __init__(self, state):
        super().__init__(state)
        if state.first_time == True:
            state.change_map_screen()
            state.first_time = False
        objects = [
            npc.Rat(7,50,self.state,radar=False),
            npc.Rat(8,42,self.state,radar=False)
        ]
        self.first_time = True
        self.game_map = mapper.GameMap("StarterTown_left_wall.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu


    def draw(self):
        if self.state.player.phaseshift:
            self.game_map.draw_map(self.state, inverted=True)    
        else:
            self.game_map.draw_map(self.state)

    def execute(self):
        pass

    def check_events(self):
        if self.state.player.x == 37:
            events.go_south(self.state,"StarterTownDocks")
        if self.state.player.y == 96:
            events.go_east(self.state,"TradeDistrict")
        if self.state.player.y == 1:
            events.go_west(self.state,"StarterTownLeftSeaWall")

        if self.state.player.x == 3 and self.state.player.y == 33:
            events.GrandPalace_interior_entrance_enter(self.state)
        if self.state.player.x == 23 and self.state.player.y == 48:
            events.LeftWall_library_enter(self.state)

class StarterTownLeftSeaWall(MapState):
    name = "Left Sea Wall"
    raw_name = "StarterTownLeftSeaWall"
    menu_commands = GameCommands
    objects = []
    game_map = mapper.GameMap("StarterTown_left_sea_wall.txt", objects)


    def __init__(self, state):
        super().__init__(state)
        if state.first_time == True:
            state.change_map_screen()
            state.first_time = False
        objects = [
        ]
        self.first_time = True
        self.game_map = mapper.GameMap("StarterTown_left_sea_wall.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu


    def draw(self):
        if self.state.player.phaseshift:
            self.game_map.draw_map(self.state, inverted=True)    
        else:
            self.game_map.draw_map(self.state)

    def execute(self):
        pass

    def check_events(self):
        if self.state.player.y == 96:
            events.go_east(self.state,"StarterTownLeftWall")


class GrandPalace_interior_entrance(MapState):
    name = "Grand Palace"
    raw_name = "GrandPalace_interior_entrance"
    menu_commands = GameCommands
    objects = []
    game_map = mapper.GameMap("GrandPalace_interior_entrance.txt", objects)


    def __init__(self, state):
        super().__init__(state)
        if state.first_time == True:
            state.change_map_screen()
            state.first_time = False
        objects = [
        ]
        self.first_time = True
        self.game_map = mapper.GameMap("GrandPalace_interior_entrance.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu


    def draw(self):
        if self.state.player.phaseshift:
            self.game_map.draw_map(self.state, inverted=True)    
        else:
            self.game_map.draw_map(self.state)

    def execute(self):
        pass

    def check_events(self):
        if self.state.player.x == 35 and self.state.player.y == 48:
            events.GrandPalace_interior_entrance_exit(self.state)


class LeftWallLibrary(MapState):
    name = "Startertown Library"
    raw_name = "LeftWallLibrary"
    menu_commands = GameCommands
    objects = []
    game_map = mapper.GameMap("LeftWall_library.txt", objects)


    def __init__(self, state):
        super().__init__(state)
        if state.first_time == True:
            state.change_map_screen()
            state.first_time = False
        objects = [
        ]
        for i in range(17,32 + 1):
            if i != 22:
                objects.append(npc.EmptyBookCase(21,i,state,[
                    "You do not see any interesting books here."
                ]))
            else:
                objects.append(npc.SingleBookCase(21,i,state,books.FallOfBrym()))
            objects.append(npc.EmptyBookCase(17,i,state,[
                "You do not see any interesting books here."
            ]))
            objects.append(npc.EmptyBookCase(13,i,state,[
                "You do not see any interesting books here."
            ]))
        for i in range(52,67 + 1):
            objects.append(npc.EmptyBookCase(21,i,state,[
                "You do not see any interesting books here."
            ]))
            objects.append(npc.EmptyBookCase(17,i,state,[
                "You do not see any interesting books here."
            ]))
            objects.append(npc.EmptyBookCase(13,i,state,[
                "You do not see any interesting books here."
            ]))
        self.first_time = True
        self.game_map = mapper.GameMap("LeftWall_library.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu


    def draw(self):
        if self.state.player.phaseshift:
            self.game_map.draw_map(self.state, inverted=True)    
        else:
            self.game_map.draw_map(self.state)

    def execute(self):
        pass

    def check_events(self):
        if self.state.player.x == 24 and self.state.player.y == 47:
            events.LeftWall_library_exit(self.state)

        if self.state.check_action:
            for item in self.game_map.objects:
                if item.y == self.state.player.y and item.x == self.state.player.x - 1:
                    item.action(self.state.stdscr, self.state)
