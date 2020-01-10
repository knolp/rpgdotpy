class Steel():
    mat = "steel"

    def show(self):
        print(self.mat)





class Longsword():
    def __init__(self,name):
        self.name = name
        self.material = Steel()

    def show(self):
        print(self.material.mat)







l = Longsword("slayer of beasts")
l.material.show()