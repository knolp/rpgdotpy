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

    list_of_ingredients = [x for x in _craft_dict.keys()]
    #MAIN LOOP
    while k != ord("q"):
        screen.clear()

        title_text = "Select a crafting ingredient."
        screen.addstr(2, int((width - len(title_text)) / 2), title_text)

        #List all ingredients
        low = max(0,(selected_item + 1)- 9)
        if low != 0:
            screen.addstr(offset_x - 2, offset_y + 10, "^")
        high = max(9, selected_item + 1)
        if high == 9 and len(list_of_ingredients) >= 9:
            screen.addstr(offset_x + 9 + 2, offset_y + 10, "v")
        current_show = list_of_ingredients[low:high]
        for i in range(len(current_show)):
            if selected_item == list_of_ingredients.index(current_show[i]):
                screen.attron(curses.color_pair(5))
                screen.addstr(offset_x + i, offset_y, f"{current_show[i]} x{_craft_dict[current_show[i]]}")
                screen.attroff(curses.color_pair(5))
            else:
                screen.addstr(offset_x + i, offset_y, f"{current_show[i]} x{_craft_dict[current_show[i]]}")

        #Show description of selected item
        screen.addstr(30,offset_y,f"Description: {_description_dict[list_of_ingredients[selected_item]]}")
        screen.addstr(31,offset_y,f"Selected item: {selected_item}")
        screen.addstr(32, offset_y,f"low = {low} : high = {high}")
        screen.addstr(33,offset_y,f"itemlist: {''.join(list_of_ingredients)}")
        
        k = screen.getch()
        if k == curses.KEY_UP:
            selected_item -= 1
            if selected_item < 0:
                selected_item = 0
        elif k == curses.KEY_DOWN:
            selected_item += 1
            if selected_item > len(list_of_ingredients) - 1:
                selected_item = len(list_of_ingredients) - 1
        
        elif k == ord(" "):
            return list_of_ingredients[selected_item]

    return False


def make_potion(state):
    screen = state.stdscr
    player = state.player
    height, width = screen.getmaxyx()
    screen.clear()

