class Hello():
    def __init__(self, a,b):
        self.a = a
        self.b = b

    def hello(self):
        print(f"{self.a} :-) {self.b}")




lista = [Hello("hhe", "asd"), Hello("egege", "hehehe")]

egege = lista[1]

for item in lista:
    del item

egege.hello()