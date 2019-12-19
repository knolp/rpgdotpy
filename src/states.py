import sys, math
import art
import mapper
import npc
import random
import abilities
import pathfinding
import monster
import battle
import events
import helper
import time
import curses

# HELPERS #

def explain_text(text, explain_text, cols):
    return_text = text + "-" * (cols - (len(text) + len(explain_text))) + explain_text
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
                         MenuItem("Debug", 3, Debug, False)]

class main_menu():
    def __init__(self, state):
        self.game_box = state.game_box
        self.command_box = state.command_box
        self.commands = [MenuItem("New Game", 1, NewGame_1, NewGame_1_commands),
                        MenuItem("Load Character", 2, False,False),
                         MenuItem("Debug", 3, Debug, False)]


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
        #self.game_box.addstr(5,40, "STARTING A NEW GAME")
        #self.game_box.addstr(7,40, "PLEASE CHOOSE A CLASS")
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
                self.state.create_player["spellbook"] = [abilities.Fireball(), abilities.LifeBolt(), abilities.Scorch()]



    def draw_warrior(self):
        self.game_box.addstr(19,46, "Warrior:")
        self.game_box.addstr(21,10, explain_text("Strength: 6 ", self.explain_text_strength, 80))
        self.game_box.addstr(22,10, explain_text("Agility: 2 ", self.explain_text_agility, 80))
        self.game_box.addstr(23,10, explain_text("Charisma: 0 ", self.explain_text_charisma, 80))
        self.game_box.addstr(24,10, explain_text("Intellect: 0 ", self.explain_text_intellect, 80))
        self.game_box.addstr(25,10, explain_text("Alchemy: 2 ", self.explain_text_alchemy, 80))
        self.game_box.addstr(26,10, explain_text("Attunement: 0 ", self.explain_text_attunement, 80))
        art.draw_shield(self.game_box,2,35)

    def draw_mage(self):
        self.game_box.addstr(19,47, "Mage:")
        self.game_box.addstr(21,10, explain_text("Strength: 1 ", self.explain_text_strength, 80))
        self.game_box.addstr(22,10, explain_text("Agility: 1 ", self.explain_text_agility, 80))
        self.game_box.addstr(23,10, explain_text("Charisma: 3 ", self.explain_text_charisma, 80))
        self.game_box.addstr(24,10, explain_text("Intellect: 4 ", self.explain_text_intellect, 80))
        self.game_box.addstr(25,10, explain_text("Alchemy: 3 ", self.explain_text_alchemy, 80))
        self.game_box.addstr(26,10, explain_text("Attunement: 3 ", self.explain_text_attunement, 80))
        art.draw_fire(self.game_box, 2, 45)

    def draw_rogue(self):
        self.game_box.addstr(19,46, "Rogue:")
        self.game_box.addstr(21,10, explain_text("Strength: 3 ", self.explain_text_strength, 80))
        self.game_box.addstr(22,10, explain_text("Agility: 4 ", self.explain_text_agility, 80))
        self.game_box.addstr(23,10, explain_text("Charisma: 2 ", self.explain_text_charisma, 80))
        self.game_box.addstr(24,10, explain_text("Intellect: 0 ", self.explain_text_intellect, 80))
        self.game_box.addstr(25,10, explain_text("Alchemy: 4 ", self.explain_text_alchemy, 80))
        self.game_box.addstr(26,10, explain_text("Attunement: 0 ", self.explain_text_attunement, 80))
        art.draw_dagger(self.game_box, 2, 44)

    def draw_back(self):
        self.game_box.addstr(19,46, "BACK")

class NewGame_2():
    def __init__(self, state):
        self.state = state
        self.game_box = state.game_box
        self.command_state = state.command_state

    def draw(self):
        height, width = self.game_box.getmaxyx()
        text = "Choose a starting area"
        self.game_box.addstr(2, center(width, text), text)
        for item in self.command_state.commands:
            if item.active:
                if item.text == "Starter Town":
                    text = "A basic town in the southern part of the realm"
                    self.game_box.addstr(20, center(width, text),text)
                    text = "Notable features:"
                    self.game_box.addstr(22, center(width, text),text)
                    text = "* Osk'Ghar the Blacksmith"
                    self.game_box.addstr(24, center(width, text),text)
                    text = "* The Grand Arena"
                    self.game_box.addstr(25, center(width, text),text)
                    text = "* The Hall of Justice"
                    self.game_box.addstr(26, center(width, text),text)
                    text = "* The temple of Mux'Ton, the god of death"
                    self.game_box.addstr(27, center(width, text), text)

                if item.text == "Orc'Theral":
                    text = "The Orc hometown in the east"
                    self.game_box.addstr(20, center(width, text),text)
                    text = "Notable features:"
                    self.game_box.addstr(22, center(width, text),text)
                    text = "* The Desert of Orchai"
                    self.game_box.addstr(24, center(width, text),text)
                    text = "* The Temple of Stone"
                    self.game_box.addstr(25, center(width, text),text)
                    text = "* Hiltir Mining Corporation"
                    self.game_box.addstr(26, center(width, text),text)

                if item.text == "Blackcliff":
                    text = "The largest fishing colony in the west"
                    self.game_box.addstr(20, center(width, text),text)
                    text = "Notable features:"
                    self.game_box.addstr(22, center(width, text),text)
                    text = "* The Mage Tower"
                    self.game_box.addstr(24, center(width, text),text)
                    text = "* Blackcliff Port"
                    self.game_box.addstr(25, center(width, text),text)
                    text = "* The White Forest"
                    self.game_box.addstr(26, center(width, text),text)

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
                    text = "* Sneaky Tounge: Increased chance to trick people"
                    self.game_box.addstr(22, center(width, text),text)
                    text = "* Eagle Eyes: Increased perception of surroundings"
                    self.game_box.addstr(23, center(width, text),text)
                    text = "* Weak-bodied: Weakness to flesh wounds"
                    self.game_box.addstr(24, center(width, text),text)

                if item.text == "Orc":
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

                if item.text == "Elf":
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
                    text = "* Nature Bond: Attuned to all gods of the land"
                    self.game_box.addstr(22, center(width, text),text)
                    text = "* Large Mind: Efficient at learning new strategies"
                    self.game_box.addstr(23, center(width, text),text)
                    text = "* Elvish Hivemind: Can occupy the minds of other Elves at will"
                    self.game_box.addstr(24, center(width, text),text)
                    text = "* Arcane Deficiency: Weakness to the Arcane arts"
                    self.game_box.addstr(25, center(width, text),text)

                if item.text == "Dwarf":
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

        self.state.game_box.addstr(start, 2, "Spells:")
        start += 2
        for item in self.state.player.spells:
            if item != False:
                self.state.game_box.addstr(start, 4, item.readable_name)
            else:
                self.state.game_box.addstr(start, 4, "None")
            start += 1

        start += 1
        self.state.game_box.addstr(start, 2, "Spellbook:")
        start += 2
        for item in self.state.player.spellbook:
            self.state.game_box.addstr(start, 4, item.readable_name)
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

    def check_events(self):
        print("NOT IMPLETMENTED")
        print(self.state.game_map)


class StarterTown(MapState):
    name = "Starter Town"
    raw_name = "StarterTown"
    menu_commands = GameCommands
    objects = [
            npc.ErolKipman(13, 37)
        ]
    game_map = mapper.GameMap("map1.txt", objects)

    def __init__(self, state):
        super().__init__(state)
        if state.first_time == True:
            state.change_map_screen()
            state.first_time = False
        objects = [
            npc.ErolKipman(13, 37),
        ]
        self.game_map = mapper.GameMap("map1.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu
        self.random_monsters = [monster.Rat]

    def draw(self):
        self.game_map.draw_map(self.state.game_box)
        #self.game_map.draw_vision(self.state, self.state.game_box)

    def execute(self):
        pass

    def check_events(self):
        # Check door
        if self.state.player.x == 17 and self.state.player.y == 47:
            events.StarterTown_door(self.state)
        elif self.state.player.x == 1:
            events.StarterTown_north(self.state)

        if self.state.player.x == 8 and self.state.player.y == 73:
            events.StarterTown_haunted_house_entrance(self.state)

        # Check NPCs
        for npc in self.game_map.objects:
            if self.state.player.x == npc.x and self.state.player.y == npc.y:
                self.state.action = "Talk"
                break
            else:
                self.state.action = "None"

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
            npc.OskGhar(16,52)
        ]
        self.game_map = mapper.GameMap("map2.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu


    def draw(self):
        self.game_map.draw_map(self.state.game_box)
        #self.game_map.draw_vision(self.state, self.state.game_box)

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
            npc.BasementChest(7,10),
        ]
    game_map = mapper.GameMap("StarterTown_house_basement_hallway.txt", objects)

    def __init__(self, state):
        super().__init__(state)
        if state.first_time == True:
            state.change_map_screen()
            state.first_time = False
        objects = [
            npc.BasementChest(7,10)
        ]
        if "RatMenace_rat_king_killed" not in state.player.flags:
            objects.append(npc.RatKing(30, 45, state))


        self.game_map = mapper.GameMap("StarterTown_house_basement_hallway.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu


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


    def draw(self):
        self.game_map.draw_vision(self.state, self.state.game_box)

    def execute(self):
        pass

    def check_events(self):
        if self.state.player.x == 29 and self.state.player.y == 66:
            events.StarterTown_haunted_house_2_dungeon_door_left(self.state)
        if self.state.player.x == 29 and self.state.player.y == 82:
            events.StarterTown_haunted_house_2_dungeon_door_right(self.state)





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
            
        ]
        self.first_time = True
        self.game_map = mapper.GameMap("GreenForest.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu


    def draw(self):
        self.game_map.draw_map(self.state.game_box)

    def execute(self):
        pass

    def check_events(self):
        if self.state.player.x == 37:
            events.GreenForest_south(self.state)

        # BROWN BEAR INN
        
        if self.state.player.x == 10 and self.state.player.y == 21:
            events.GreenForest_brown_bear_inn_entrance(self.state)

        if self.state.player.x == 10 and self.state.player.y == 22:
            helper.popup(self.state.stdscr, self.state, [
                "BROWN BEAR INN",
                "",
                "Come inside and have a drink or rent a room for the night"
                ])
            self.state.player.x, self.state.player.y = self.state.player.last_pos

        # HALL OF JUSTICE

        if self.state.player.x == 14 and self.state.player.y in [72,73]:
            events.GreenForest_hall_of_justice_entrance(self.state)
        
        if self.state.player.x == 14 and self.state.player.y == 74:
            helper.popup(self.state.stdscr, self.state, [
                "Hall of Justice",
                "",
                "For all your goverment needs."
                ])
            self.state.player.x, self.state.player.y = self.state.player.last_pos


        # PLAYER HOUSE
        if self.state.player.x == 24 and self.state.player.y == 31:
            events.GreenForest_player_house_entrance(self.state)

        # TANNER


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
            npc.EvanKripter(19,31),
            npc.BaldirKragg(19,17),
            npc.BodvarKragg(23,17),
            npc.LarsMagnus(23,35)
        ]
        self.first_time = True
        self.game_map = mapper.GameMap("BrownBearInn.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu


    def draw(self):
        self.game_map.draw_map(self.state.game_box)

    def execute(self):
        pass

    def check_events(self):
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
        self.game_map.draw_map(self.state.game_box)

    def execute(self):
        pass

    def check_events(self):
        if self.state.player.x == 34 and self.state.player.y == 48:
            events.HallOfJustice_exit(self.state)

        if self.state.player.x in [20,21,22,23] and self.state.player.y == 15 and self.state.check_action:
            for item in self.game_map.objects:
                if item.name == "Becca Lithe":
                    item.action(self.state.game_box, self.state)

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
        objects = [
        ]
        if "StarterTown_house_alchemy_table" in state.player.flags:
            objects.append(npc.AlchemyTable(16, 75, state))
        self.first_time = True
        self.game_map = mapper.GameMap("StarterTownPlayerHouse.txt", objects)
        self.menu = GameMenu
        self.menu_commands = GameCommands
        self.ingame_menu = IngameMenu


    def draw(self):
        self.game_map.draw_map(self.state.game_box)

    def execute(self):
        pass

    def check_events(self):
        if self.state.player.x == 34 and self.state.player.y == 48:
            events.StarterTown_player_house_exit(self.state)


            