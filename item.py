import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Item:
    def __init__(self, name, desc, weight, type=None):
        self.name = name
        self.desc = desc
        self.loc = None
        self.weight = weight
        self.type = type
    def describe(self):
        clear()
        print(self.desc)
        print()
        input("Press enter to continue...")
    def putInRoom(self, room):
        self.loc = room
        room.addItem(self)

class Armor(Item):
    def __init__(self, name, desc, weight, resistance, encumberance, type=None):
        Item.__init__(self, name, desc, weight, type)
        self.resistance = resistance
        self.encumberance = encumberance

class Weapon(Item):
    def __init__(self, name, desc, weight, damage, unweildly, speed, type=None):
        Item.__init__(self, name, desc, weight, type)
        self.damage = damage
        self.unweildly = unweildly
        self.speed = speed

class Usable(Item):
    def consume(self): #does what it says, you use a consumable item, it gets consumed - i.e. no long anywhere
        player = self.loc
        player.items.remove(self)
        self.loc = None
