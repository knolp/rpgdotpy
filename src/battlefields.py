class Battlefield():
    def __init__(self, name):
        self.name = name
        self.ground_items = []

        # Information
        self.weather = False
        self.hazards = False


class Dungeon(Battlefield):
    def __init__(self, name):
        super().__init__(name)
