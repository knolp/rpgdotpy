import curses

class Book():
    def __init__(self, name):
        self.name = name

    
    def read(self, screen):
        #insert read book here
        screen.clear()
        k = -1

        selected_page = 0
        max_page = len(self.pages) - 1
        
        while k != ord("q"):
            screen.clear()
            start = 10
            for item in self.pages[selected_page]:
                if start == 10:
                    screen.attron(curses.color_pair(135))
                if "[" in item:
                    before, keyword, after = item.split("[")[0], item.split("[")[1].split("]")[0], item.split("]")[1]
                    screen.addstr(start,34,before)
                    screen.attron(curses.color_pair(136))
                    screen.addstr(start,34 + len(before),keyword)
                    screen.attroff(curses.color_pair(136))
                    screen.addstr(start, 34 + len(before) + len(keyword), after)
                else:
                    screen.addstr(start, 34, item)

                if start == 10:
                    screen.attroff(curses.color_pair(135))

                start += 1

            if selected_page != 0:
                screen.addch(47,32,curses.ACS_LARROW)

            screen.addstr(47,34, f"Page {selected_page + 1} of {max_page + 1}")

            if selected_page < max_page:
                screen.addch(47,36 + len(f"Page {selected_page + 1} of {max_page + 1}"),curses.ACS_RARROW)

            k = screen.getch()

            if k == curses.KEY_LEFT:
                selected_page = max(0,selected_page - 1)
            elif k == curses.KEY_RIGHT:
                selected_page = min(len(self.pages) - 1,selected_page + 1)
        curses.ungetch(curses.KEY_F0)


class BasicAlchemy(Book):
    def __init__(self):
        super().__init__("BasicAlchemy")
        self.readable_name = "Basic Alchemy"
        self.author = "Edith Lang"


        page_1 = [
            "Basic Alchemy",
            "",
            "A collection of beginner recipes.",
            "",
            "Chapters:",
            "",
            "1: For the mind"
        ]

        page_2 = [
            "Prewords:",
            "",
            "To be able to make these brews and potions one must",
            "first have access to the following",
            "",
            "[A brewing station]",
            "[A juicer]",
            "[A dryer]",
            "[A pestle and mortar]",
            "",
            "And ofcourse a passion for herbs and alchemy!"
        ]

        page_3 = [
            "Chapter 1: For the Mind",
            "",
            "Altering the state of the mind is an easy task",
            "for even the simplest of brews.",
            "",
            "But do not take it easy, for changing the mind can",
            "lead to disastrous results if done incorrectly.",
            "I advise to follow the steps exactly.",
            "",
            "Or else you might end up as [Melder, the Deranged King]"
        ]

        page_4 = [
            "Ad'ral Brew",
            "",
            "[1x Deverberry]",
            "[1x Barbura Leaf]",
            "",
            "Start by preparing the [deverberry], by juicing it.",
            "",
            "   (Be sure to save the [skin] as it)",
            "   (can act as a great activator for a [Woodland Charm])",
            "",
            "Then dry out the [leaves] and add it to a vial of water.",
            "Stir until you can see no trace of leaves and it has",
            "become a distinct [brown] color."
        ]

        self.pages = [page_1, page_2, page_3, page_4]