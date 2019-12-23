import curses
import helper


@helper.add_ungetch
def select_ingredient(state):
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
            if item.readable_name not in _craft_dict.keys():
                _craft_dict[item.readable_name] = 1
                _description_dict[item.readable_name] = item.description
            else:
                _craft_dict[item.readable_name] += 1

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
            return list_of_ingredients[selected_item]

    return False


def make_potion(state):
    screen = state.stdscr
    player = state.player
    height, width = screen.getmaxyx()
    screen.clear()

