import os
import random

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self):
        self.location = None
        self.items = []
        self.equipped = [] #equipped items on separate list because they need special treatment
        self.damage = 5 #maximum damage on attack, modified by strength
        self.resistance = 0 #ammount of damage blocked on attack, modified by armor
        self.evasion = 10 #chance to dodge a monster strike
        self.accuracy = 80 #chase to hit a monster strike - monsters also have evasion though - modified by dexterity
        self.maxHealth = 20 #modified by strength
        self.health = 20
        self.rr = 20 #number of turns between regeneration ticks, modified by level
        self.maxMP = 6 #modified by intelligence
        self.manaPoints = 6
        self.attackSpeed = 10 #modified by weapon
        self.str = 10 #Strenght
        self.dex = 10 #Dexterity
        self.int = 10 #Intelligence
        self.carryWeight = 20 #modified by strenght
        self.background = None #player picks this at begining of game
        self.exp = 0
        self.level = 1
        self.alive = True
        self.inCombat = False #turns true when in combat (duh)
        self.spellsC = [] #spells the player knows that can be used in combat
        self.spellsNC = [] #spells for out of combat
        self.invisible = False #invis players can't be attacked by suprise
    def displayMe(self):
        clear()
        print("Class: "+self.background)
        print("Level: "+str(self.level))
        print("Experience: "+str(self.exp)+"/1000")
        print("Health: "+str(self.health)+"/"+str(self.maxHealth))
        print("Mana: "+str(self.manaPoints)+"/"+str(self.maxMP))
        print("Strength: "+str(self.str))
        print("Dexterity: "+str(self.dex))
        print("Intelligence: "+str(self.int))
        print("Carrying: "+str(self.checkCarryWeight())+"/"+str(self.carryWeight))
        print("Attack Speed: "+str(self.attackSpeed))
        print("When hit you block up to "+str(self.resistance)+" damage.")
        print()
        #this next part is so the player knows all the slots, and so there is a set order of printing
        #showInventory doesn't have a set order of printing so I wanted a set order somewhere
        weapon, head, chest, legs, feet, hands = "None", "None", "None", "None", "None", "None"
        for i in self.equipped:
            if type(i).__name__ == "Weapon":
                weapon = i.name
            elif i.type == "head":
                head = i.name
            elif i.type == "chest":
                chest = i.name
            elif i.type == "legs":
                legs = i.name
            elif i.type == "feet":
                feet = i.name
            elif i.type == "hands":
                hands = i.name
        print("Weapon: "+weapon)
        print("Headgear: "+head)
        print("Body Armor: "+chest)
        print("Leg Cover: "+legs)
        print("Feet: "+feet)
        print("Hands: "+hands)
        print()
        input("Press enter to continue...")
    def goDirection(self, direction):
        self.location = self.location.getDestination(direction)
    def pickup(self, item):
        self.items.append(item)
        item.loc = self
        self.location.removeItem(item)
    def checkCarryWeight(self, item=None):
        #the reason why item would be none: if you're doing the me command and want to see available carryweight
        #reason why item wouldn't be none: to say if you can pick up an item, stops player from going over carryweight
        if item is not None:
            carryingWeight = item.weight
        else:
            carryingWeight = 0
        for i in self.items:
            carryingWeight += i.weight
        for i in self.equipped:
            carryingWeight += i.weight
        #the condition below is to make sure the player can pick up an item that weighs nothing when their inventory is empty
        #found this issue while trying to pickup to the map with empty inventory
        if carryingWeight== 0 and item is not None:
            carryingWeight+=1
        if carryingWeight<=50:
            return carryingWeight
        else:
            return False
    def showInventory(self):
        clear()
        print("You currently have equipped:")
        print()
        for i in self.equipped:
            if type(i).__name__ == "Armor":
                print(i.type+": "+i.name)
            else:
                print("Weapon: "+i.name)
        print()
        print("You are currently carrying:")
        print()
        for i in self.items:
            previous = self.items[:self.items.index(i)] #i not included
            remaining = self.items[self.items.index(i):] #i included
            alreadyPrinted = False
            for j in previous: #checking for matching names
                if i.name == j.name:
                    alreadyPrinted = True
            if not alreadyPrinted: #if we go through this loop we know nothing before this has the same name
                numberOfThese = 0 #0 since i is in remaining
                for j in remaining:
                    if i.name==j.name:
                        numberOfThese+=1
                if numberOfThese==1:
                    print(i.name)
                else:
                    print(i.name+" x"+str(numberOfThese))
        print()
        input("Press enter to continue...")
    def combatStatus(self):
        #combat status, because printSituation isn't helpful in combat but this info is
        mon = self.inCombat
        print()
        print("Your health is " + str(self.health) + ".")
        print(mon.name + "'s health is " + str(mon.health) + ".")
    def attackMonster(self, mon): #attack initiates combat
        self.inCombat = mon
        mon.enterCombat(self)
        clear()
        print("You initiate combat with " + mon.name)
    def strike(self): #strike is a basic attack with fist or equipped weapon
        mon = self.inCombat
        clear()
        hitRoll = random.randint(1,100)
        if hitRoll < 100-self.accuracy: #shows if you just miss
            print("You miss the "+mon.name)
        elif hitRoll < 100-self.accuracy+mon.evasion: #whereas this is if the difference is the enemy dodges
            print("The "+mon.name+" dodges your strike.")
        else: #and here is if you hit
            damage = random.randint(1,self.damage)
            print("You hit the "+ mon.name + " for "+str(damage)+" damage.")
            mon.take_damage(damage)
    def getItemByName(self, name):
        for i in self.items:
            if i.name.lower() == name.lower():
                return i
        return False
    def getEquippedItemByName(self, name):
        #basically getItemByName but for self.equiped
        for i in self.equipped:
            print(i.name)
            if i.name.lower() == name.lower():
                print("match")
                return i
        return False
    def drop(self, item):
        self.items.remove(item)
        item.putInRoom(self.location)
    def equip(self,item):
        #only one weapon and type of armor allowed at a time
        for i in self.equipped:
            if type(i) == type(item) and (i.type == item.type or type(i).__name__ == "Weapon"):
                #the first condition always needs to be true, the second is only for armor and the third is so weapons don't have any issue
                self.unequip(i)
        self.equipped.append(item)
        self.items.remove(item)
        if type(item).__name__ == "Weapon":
            self.damage += item.damage
            self.accuracy -= item.unweildly
            self.attackSpeed = item.speed
        else: #since you can only equip weapons and armor if you hit this else it's armor
            self.resistance += item.resistance
            self.evasion -= item.encumberance
    def unequip(self, item):
        self.equipped.remove(item)
        self.items.append(item)
        if type(item).__name__ == "Weapon":
            self.damage -= item.damage
            self.accuracy += item.unweildly
            self.attackSpeed = 10
        else: #since you can only equip weapons and armor if you hit this else it's armor
            self.resistance -= item.resistance
            self.evasion += item.encumberance
    def increaseStr(self, n): #helper functions so increasing base stats is more efficient
        self.str += n
        self.maxHealth += n
        self.health += n
        self.damage += n//2
        self.carryWeight += 2*n
    def increaseDex(self, n):
        self.dex += n
        self.evasion += 2*n
        self.accuracy += 2*n
    def increaseInt(self, n):
        self.int += n
        self.maxMP += n//2
        self.manaPoints += n//2
    def gainExp(self, n):
        self.exp += n
        if self.exp >= 1000: #levels are always 1000 exp, but you gain less exp at higher levels from a given enemy
            print("You have leveled up")
            self.exp -= 1000
            self.level += 1
            self.health += 5
            self.rr -= 1
            self.maxHealth += 5
            self.maxMP += 1
            self.manaPoints += 1
            increase = None #use increase for if stat increases to reduce redundent lines
            if not self.level % 4: #levels divisible by 4
                print("You must choose to increase Strength, Dexterity, or Intelligence")
                print("Please pick one now by typing S, D, or I")
                while increase != "S" and increase != "D" and increase != "I":
                    if increase is not None:
                        print("Invald choice, pick again")
                    increase = input()
            elif not self.level%2: #levels divisible by 2 but not 4
                if self.background == "warrior":
                    increase = "S"
                elif self.background == "rogue":
                    increase = "D"
                else:
                    increase = "I"
            if increase == "S":
                print("You feel stronger")
                self.increaseStr(2)
            elif increase == "D":
                print("You feel more nimble")
                self.increaseDex(2)
            elif increase == "I":
                self.increaseInt(2)
