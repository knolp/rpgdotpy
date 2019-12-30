import curses
import helper
import art
import items
import time

def add_border(x,y,screen,textlength,button=False):
    if button:
        off_y = 10
    else:
        off_y = textlength

    screen.addch(x,y-1,curses.ACS_VLINE)
    screen.addch(x,y+off_y,curses.ACS_VLINE)
    
    screen.addch(x-1,y-1,curses.ACS_ULCORNER)
    screen.addch(x-1,y+off_y,curses.ACS_URCORNER)
    screen.addch(x+1,y-1,curses.ACS_LLCORNER)
    screen.addch(x+1,y+off_y,curses.ACS_LRCORNER)

    for i in range(off_y):
        screen.addch(x-1,y+i,curses.ACS_HLINE)
        screen.addch(x+1,y+i,curses.ACS_HLINE)


@helper.add_ungetch
def select_ingredient(state, juicable=False):
    screen = state.stdscr
    player = state.player
    height, width = screen.getmaxyx()
    k = -1

    offset_x = 15
    offset_y = 15

    _craft_dict = {}
    _description_dict = {}
    selected_item = 0


    for item in player.inventory:
        if item.type == "farming":
            if item.readable_name not in _craft_dict.keys():
                _craft_dict[item.readable_name] = 1
                _description_dict[item.readable_name] = item.description
            else:
                _craft_dict[item.readable_name] += 1

    if len(_craft_dict.keys()) == 0:
        return False

    list_of_ingredients = sorted([x for x in _craft_dict.keys()])
    #MAIN LOOP
    low = 0
    while k != ord("q"):
        screen.clear()

        title_text = "Select a seed to plant."
        screen.addstr(2, int((width - len(title_text)) / 2), title_text)

        #List all ingredients
        if low != 0:
            screen.addstr(offset_x - 2, offset_y + 15, "^")
        else:
            screen.addstr(offset_x + 11, offset_y + 15, "v")
        current_show = list_of_ingredients[low:]
        for i in range(len(current_show)):
            if selected_item == list_of_ingredients.index(current_show[i]):
                screen.attron(curses.color_pair(5))
                screen.addstr(offset_x + i, offset_y, f"{current_show[i]}")
                screen.addstr(offset_x + i, offset_y + len(f"{current_show[i]}"), f"  x{_craft_dict[current_show[i]]}")
                screen.attroff(curses.color_pair(5))
            else:
                screen.addstr(offset_x + i, offset_y, f"{current_show[i]}")
                screen.addstr(offset_x + i, offset_y + len(f"{current_show[i]}"), f"  x{_craft_dict[current_show[i]]}", curses.color_pair(136))
            
            if i == 9:
                break

        #Show description of selected item
        screen.addstr(30, offset_y+ 45, "Description: ",curses.color_pair(136))
        screen.addstr(30,offset_y + 45 + len("Description: "),f"{_description_dict[list_of_ingredients[selected_item]]}")

        #Draw commands
        #screen.attron(curses.color_pair(135))
        screen.addstr(40, offset_y, "[Space]: ",curses.color_pair(136))
        screen.addstr(40, offset_y + len("[Space]: "), "Select seed.")
        screen.addstr(42, offset_y, "[Q]: ",curses.color_pair(136))
        screen.addstr(42, offset_y + len("[Q]: "), "Quit and go back.")
        
        k = screen.getch()
        if k == curses.KEY_UP:
            selected_item -= 1
            if selected_item < 0:
                selected_item = 0
            if selected_item <= low:
                low -= 1
                if low <= 0:
                    low = 0
        elif k == curses.KEY_DOWN:
            selected_item += 1
            if selected_item > len(list_of_ingredients) - 1:
                selected_item = len(list_of_ingredients) - 1
            if selected_item >= 9 and selected_item != len(list_of_ingredients) - 1:
                low += 1
        
        elif k == ord(" "):
            for item in player.inventory:
                if item.readable_name == list_of_ingredients[selected_item]:
                    return player.inventory.pop(player.inventory.index(item))

    return "Empty"

@helper.add_ungetch
def farming(state, identity):
    screen = state.stdscr
    player = state.player
    height, width = screen.getmaxyx()
    curses.halfdelay(3)
    k = -1

    offset_x = 20
    offset_y = int(width/2)

    selected_item = 0
    planted = False
    ready = False
    no_seeds = False

    for item in player.active_farms:
            if item[0] == identity:
                planted = True
    

    while k != ord("q"):
        screen.clear()
        if planted:
            button_text = "Harvest"
        else:
            button_text = "Select seed to plant"

        if not planted:
            if no_seeds:
                screen.addstr(offset_x, offset_y - int(len("You have no seeds.")/2), "You have no seeds.")
            else:
                screen.addstr(offset_x, offset_y - int(len("There is no seed planted in this farming patch.") / 2), "There is no seed planted in this farming patch.")
            screen.addstr(offset_x + 10, offset_y - int(len(button_text) / 2), button_text, curses.color_pair(5))

        if planted:
            for item in player.active_farms:
                if item[0] == identity:
                    plant_name = item[1]
                    timer = item[2]
                    result = item[3]
                    harvest_time = item[4]
            screen.addstr(offset_x, offset_y - int(len(plant_name) / 2), plant_name)

            date_planted = time.gmtime(timer)
            date_text = f"Planted at: {date_planted.tm_year - 1200}/{date_planted.tm_mon:02}/{date_planted.tm_mday:02}  {date_planted.tm_hour:02}:{date_planted.tm_min:02}"
            screen.addstr(offset_x + 2, offset_y - int(len(date_text) /2), date_text)

            date_harvested = time.gmtime(timer + harvest_time)
            harvest_text = f"Ready for harvest at: {date_harvested.tm_year - 1200}/{date_harvested.tm_mon:02}/{date_harvested.tm_mday:02}  {date_harvested.tm_hour:02}:{date_harvested.tm_min:02}"
            screen.addstr(offset_x + 3, offset_y - int(len(harvest_text) /2), harvest_text)

            if state.timer.tid >= timer + harvest_time:
                screen.addstr(offset_x + 10, offset_y - int(len(button_text)/2), button_text, curses.color_pair(5))
                ready = True
            else:
                screen.addstr(offset_x + 10, offset_y - int(len(button_text)/2), button_text, curses.color_pair(152))
                ready = False

        k = screen.getch()

        if k == ord(" "):
            if planted:
                if ready:
                    text = [
                        "You harvest the plant and gain",
                        "",
                        "",
                    ]
                    for item in result:
                        player.inventory.append(helper.get_item(item)())
                        text.append(item)
                    helper.popup(screen, state, text)
                    for item in player.active_farms:
                        if item[0] == identity:
                            player.active_farms.pop(player.active_farms.index(item))
                    planted = False
                else:
                    answer = helper.yes_no(screen, state, [
                        "The plant is not done yet.",
                        "",
                        "Harvesting this plant will kill it.",
                        "",
                        "Are you sure?"
                    ])
                    if answer:
                        for item in player.active_farms:
                            if item[0] == identity:
                                player.active_farms.pop(player.active_farms.index(item))
                        planted = False
            else:
                seed_to_plant = select_ingredient(state)
                if not seed_to_plant:
                    no_seeds = True
                else:
                    player.active_farms.append([identity,seed_to_plant.readable_name,state.timer.tid, seed_to_plant.result, seed_to_plant.harvest_time])
                    planted = True