import items

class Recipe():
    def __init__(self, name):
        self.name = name




class AdralBrew(Recipe):
    def __init__(self):
        super().__init__("AdralBrew")
        self.ingredients = ["Deverberry Juice", "Barbura Leaf (Dried)", "Empty", "Empty"]
        self.result = "AdralBrew"
        self.description = [
            "This is an old elven brew, made before the creation of man.",
            "It's effect heightens the senses and makes the body alert."
        ]

class BrawlersElixir(Recipe):
    def __init__(self):
        super().__init__("BrawlersElixir")
        self.ingredients = ["Desert Salt", "Troll Hair", "Ariam Leaf", "Empty"]
        self.result = "BrawlersElixir"
        self.description = [
            "This is an old elven brew, made before the creation of man.",
            "It's effect heightens the senses and makes the body alert."
        ]