import curses
import helper
import art
import items



@helper.add_ungetch
def make_juice(state):
    screen = state.stdscr
    player = state.player
    height, width = screen.getmaxyx()
    curses.halfdelay(3)
    k = -1

    offset_x = 10
    offset_art = 20
    offset_y = 64

    text = "Empty"
    real = ""
    counter = 0


    selected_item = 0
    juice_done = False
    no_ingredients = False
    nothing_selected = False
    result = []

    while k != ord("q"):
        counter += 1
        screen.clear()
        title_text = "Select a berry or fruit to juice."
        screen.addstr(2, int((width - len(title_text)) / 2), title_text)


        #Draw Select ingredient button

        add_border(offset_x, offset_y, screen)
        if selected_item == 0:
            screen.addstr(offset_x, offset_y, f"1: {text}", curses.color_pair(5))
        else:
            screen.addstr(offset_x, offset_y, f"1: {text}")

        #Draw juice animation
        if counter % 2 == 0:
            for idx, item in enumerate(art.draw_juicer()):
                screen.addstr(offset_art + idx, offset_y + 6, item)
        else:
            for idx, item in enumerate(art.draw_juicer_alternate()):
                screen.addstr(offset_art + idx, offset_y + 6, item)

        #Draw Make Button
        add_border(35,offset_y + 8, screen, button=True)
        if selected_item == 1:
            screen.addstr(35, offset_y + 11, "JUICE", curses.color_pair(5))
        else:
            screen.addstr(35, offset_y + 11, "JUICE", curses.color_pair(6))

        if juice_done:
            screen.addstr(40, offset_y, f"{done_text}", curses.color_pair(136))
            screen.addstr(42, offset_y, "Was processed into:")
            for i in range(len(processed)):
                screen.addstr(44 + i, offset_y, processed[i], curses.color_pair(136))
        
        if no_ingredients:
            screen.addstr(40, offset_y, "You do not have any ingredients to juice.", curses.color_pair(133))

        if nothing_selected:
            screen.addstr(40,offset_y, "You cannot make juice out of nothing.", curses.color_pair(133))



        #Draw result

        k = screen.getch()

        if k == curses.KEY_DOWN:
            selected_item = 1
        elif k == curses.KEY_UP:
            selected_item = 0
        elif k == ord(" "):
            if selected_item == 1 and text == "Empty":
                nothing_selected = True
                juice_done = False
            elif selected_item == 1 and text != "Empty":
                nothing_selected = False
                juice_done = True
                done_text = player.temp_alchemy_inventory[0].readable_name
                processed = []
                result = player.temp_alchemy_inventory[0].result
                player.temp_alchemy_inventory = []
                for item in result:
                    temp = getattr(items, item)()
                    player.inventory.append(temp)
                    processed.append(temp.readable_name)
                    
                text = "Empty"
            elif selected_item == 0:
                juice_done = False
                if text != "Empty":
                    player.inventory.append(player.temp_alchemy_inventory[0])
                    player.temp_alchemy_inventory = []
                text = select_ingredient(state, juicable=True)
                if not text:
                    no_ingredients = True
                    text = "Empty"
                else:
                    no_ingredients = False

    for item in player.temp_alchemy_inventory:
        player.inventory.append(item)
    curses.cbreak()



def add_border(x,y,screen,button=False):
    if button:
        off_y = 10
    else:
        off_y = 30
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
        if item.type == "crafting":
            if juicable:
                if not item.juicable:
                    continue
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

        title_text = "Select a crafting ingredient."
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
        screen.addstr(40, offset_y + len("[Space]: "), "Select ingredient.")
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
                    player.temp_alchemy_inventory.append(item)
                    player.inventory.pop(player.inventory.index(item))
                    break
            return list_of_ingredients[selected_item]

    return "Empty"

@helper.add_ungetch
def make_potion(state):
    screen = state.stdscr
    player = state.player
    height, width = screen.getmaxyx()
    screen.clear()
    curses.halfdelay(3)
    
    ingredient_1 = "Empty"
    ingredient_2 = "Empty"
    ingredient_3 = "Empty"
    ingredient_4 = "Empty"

    ingredients = ["Empty","Empty","Empty","Empty"]

    ingredient_y = int(width/2) - 15

    selected_item = 0
    potion_done = False
    no_ingredients = False

    k = -1
    counter = 0

    lista = [1,2,3,4]

    while k != ord("q"):
        screen.clear()
        title_text = "Select ingredients to brew with."
        screen.addstr(2, int((width - len(title_text)) / 2), title_text)
        
        add_border(10,ingredient_y, screen)
        if selected_item == 0:
            screen.addstr(10, ingredient_y, f"1: {ingredients[0]}", curses.color_pair(5))
        else:
            screen.addstr(10, ingredient_y, f"1: {ingredients[0]}")
        add_border(13,ingredient_y, screen)
        if selected_item == 1:
            screen.addstr(13, ingredient_y, f"2: {ingredients[1]}", curses.color_pair(5))
        else:
            screen.addstr(13, ingredient_y, f"2: {ingredients[1]}")
        add_border(16,ingredient_y, screen)
        if selected_item == 2:
            screen.addstr(16, ingredient_y, f"3: {ingredients[2]}", curses.color_pair(5))
        else:
            screen.addstr(16, ingredient_y, f"3: {ingredients[2]}")
        add_border(19,ingredient_y, screen)
        if selected_item == 3:
            screen.addstr(19, ingredient_y, f"4: {ingredients[3]}", curses.color_pair(5))
        else:
            screen.addstr(19, ingredient_y, f"4: {ingredients[3]}")






        counter += 1
        if counter % 2 == 0:
            for idx, item in enumerate(art.draw_alchemy()):
                if idx >= 2:
                    screen.attron(curses.color_pair(150))
                screen.addstr(23 + idx, int(width/2) - 7, item)
                if idx >= 2:
                    screen.attroff(curses.color_pair(150))
            for idx, item in enumerate(art.draw_alchemy_fire()):
                if idx == 0:
                    screen.attron(curses.color_pair(136))
                else:
                    screen.attron(curses.color_pair(149))
                screen.addstr(29 + idx, int(width/2) - 7, item)
                if idx == 0:
                    screen.attroff(curses.color_pair(136))
                else:
                    screen.attroff(curses.color_pair(149))

        else:
            for idx, item in enumerate(art.draw_alchemy_alternate()):
                if idx >= 2:
                    screen.attron(curses.color_pair(150))
                screen.addstr(23 + idx, int(width/2) - 7, item)
                if idx >= 2:
                    screen.attroff(curses.color_pair(150))
            for idx, item in enumerate(art.draw_alchemy_fire_alternate()):
                if idx == 0:
                    screen.attron(curses.color_pair(136))
                else:
                    screen.attron(curses.color_pair(149))
                screen.addstr(29 + idx, int(width/2) - 7, item)
                if idx == 0:
                    screen.attroff(curses.color_pair(136))
                else:
                    screen.attroff(curses.color_pair(149))


        add_border(35,ingredient_y + 8, screen, button=True)
        if selected_item == 4:
            screen.addstr(35, ingredient_y + 11, "BREW", curses.color_pair(5))
        else:
            screen.addstr(35, ingredient_y + 11, "BREW", curses.color_pair(6))

        if potion_done:
            screen.addstr(45, ingredient_y, "You created the ")
            screen.addstr(45,ingredient_y + len("You created the "), f"{potion_done}", curses.color_pair(136))
        
        if no_ingredients:
            screen.addstr(45, ingredient_y, "You have no ingredients.")


        k = screen.getch()

        if k == curses.KEY_DOWN:
            selected_item += 1
            if selected_item > 4:
                selected_item = 4
        elif k == curses.KEY_UP:
            selected_item -= 1
            if selected_item < 0:
                selected_item = 0

        elif k == ord(" "):
            if selected_item <= 3:
                potion_done = False
                count_crafting = 0
                for item in player.inventory:
                    if item.type == "crafting":
                        count_crafting += 1

                if count_crafting != 0:
                    if ingredients[selected_item] == "Empty":
                        ingredients[selected_item] = select_ingredient(state)
                    else:
                        for item in player.temp_alchemy_inventory:
                            if item.readable_name == ingredients[selected_item]:
                                player.inventory.append(item)
                                player.temp_alchemy_inventory.pop(player.temp_alchemy_inventory.index(item))
                                break
                        ingredients[selected_item] = select_ingredient(state)
                else:
                    no_ingredients = True
            else:
                potion_done = True
                if player.recipes:
                    list_of_recipe_ingredients = [(sorted(x.ingredients), x) for x in player.recipes]
                    for item in list_of_recipe_ingredients:
                        if item[0] == sorted(ingredients):
                            player.inventory.append(getattr(items,item[1].result)())
                            potion_done = getattr(items,item[1].result)().readable_name
                            print(potion_done)
                            break
                        else:
                            potion_done = "Nothing."
                
                if potion_done != "Nothing.":
                    player.temp_alchemy_inventory = []
                    ingredients = ["Empty","Empty","Empty","Empty"]
                else:
                    for item in player.temp_alchemy_inventory:
                        player.inventory.append(item)
                    player.temp_alchemy_inventory = []
                    ingredients = ["Empty","Empty","Empty","Empty"]

    
    curses.cbreak()
    for item in player.temp_alchemy_inventory:
        player.inventory.append(item)
    player.temp_alchemy_inventory = []
    return False


