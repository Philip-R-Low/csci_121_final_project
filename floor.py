from room import Room
from monster import Monster
from item import Item
from item import Armor
from item import Weapon
from item import Usable
import updater
import random
random.seed()

class Floor:
    def __init__(self, name, maxX, maxY, mlist, ilist):
        self.name = name
        self.maxX = maxX
        self.maxY = maxY
        self.mlist = mlist
        self.ilist = ilist
        self.finalX = random.randint(-maxX, maxX)
        self.finalY = random.randint(-maxY, maxY)
        while self.finalX == 0 and self.finalY == 0: #don't want the entrance to also be the exit
            self.finalX = random.randint(-self.maxX, self.maxX)
            self.finalY = random.randint(-self.maxY, self.maxY)
        self.nextFloor = None
        self.rooms = []
        #now to make rooms
        #since there are no doors at this point, need rooms to know who their neighbors are without adding exits
        for i in range(-maxX,maxX+1):
            for j in range(-maxY,maxY+1):
                r = Room("You are at ("+str(i)+","+str(j)+") of "+name+".")
                r.addToFloor(self)
                self.rooms.append(r)
                if j > -maxY:
                    Room.addNeighbors(r,"south",aux,"north")
                if i==0 and j==0:
                    self.start = r
                elif i==self.finalX and j==self.finalY:
                    self.end = r
                if i == -maxX and j == maxY:
                    self.topleft = r
                aux = r #auxilary for giving rooms neighbors
            if i > -maxX:
                curr_left = lcl #auxilary variables, so east and west neighbors work
                curr_right = r
                for j in range(0,2*maxY):
                    Room.addNeighbors(curr_right, "west", curr_left, "east")
                    curr_left = curr_left.neighbors[0][0]
                    curr_right =curr_right.neighbors[0][0]
            lcl = r #auxilary for giving rooms neighbors, little trickier for rows than coloms
        updater.register(self)
    def makeFloorLayout(self):
        visited = [self.start] #list of rooms visisted
        stack = [self.start] #list of rooms to check if all neighbors have at least 1 exit
        while len(stack)>0: #while there might be an unconnected room
            current = random.choice(stack) #randomness here is for the sake of getting the possibility of more than 2 exits
            stack.remove(current) #removes for now
            neighbors_remaining = []
            for x in current.neighbors:
                if x[0] not in visited:
                    neighbors_remaining.append(x[0]) #puts neighbor rooms in list
            try: #fails if neighbors are empty
                chosen = random.choice(neighbors_remaining) #takes random neighbor without door
                stack.append(current) #adds back to current because we don't know if it still has neighbors remaining
                for x in current.neighbors: #grabs direction for making exit
                    if x[0] is chosen:
                        current_direction = x[1]
                for x in chosen.neighbors: #grabs direction for making exit
                    if x[0] is current:
                        chosen_direction = x[1]
                Room.connectRooms(current, current_direction, chosen, chosen_direction) #makes exits
                visited.append(chosen) #chosen shouldn't yet be in visited, so we can put it there now
                stack.append(chosen) #we don't know anything about chosen's neighbors remaining so to the stack
            except: #we're done if there are no empty neighbors, no reason to add back to stack, so we pass
                pass
    def giveNextFloor(self, successor):
        self.nextFloor = successor
        Room.connectRooms(self.end, "down", successor.start, "up")
    def placeEnemies(self, n): #generates n random enemies from list of possible enemy types
        weights = [] #this is reconstructing the probability weights onto a new list to make random.choices happy
        for i in self.mlist:
            weights.append(i[7])
        adding = random.choices(self.mlist, weights, k=n) #makes n choices, weights by weights
        for i in range(n):
            room = random.choice(self.rooms) #picks random room to put the baddie in
            mon = Monster(adding[i][0], adding[i][1], room, adding[i][2], adding[i][3], adding[i][4], adding[i][5], adding[i][6])
    def placeRandomItem(self, room):
        weights = [] #reconstructing probably weights to make random.choices happy
        for i in self.ilist: #different types of items have their probability weight in difference places
            if i[0]=="Usable":
                weights.append(i[5])
            elif i[0]=="Weapon":
                weights.append(i[8])
            else:
                weights.append(i[7])
        a = random.choices(self.ilist, weights, k=1) #a is a list with only 1 thing, a[0] is the item information desired,
        if a[0][0]=="Weapon": #need to give the right variables depending on the class of item
            item = Weapon(a[0][1],a[0][2],a[0][3],a[0][4],a[0][5],a[0][6],a[0][7])
        elif a[0][0]=="Armor":
            item = Armor(a[0][1],a[0][2],a[0][3],a[0][4],a[0][5],a[0][6])
        else:
            item = Usable(a[0][1],a[0][2],a[0][3],a[0][4])
        item.putInRoom(room)
    def placeItems(self, n): #does previous command n times with random rooms
        for i in range(n):
            room = random.choice(self.rooms)
            self.placeRandomItem(room)
    def update(self):
        if random.random() < 0.5:
            self.placeEnemies(1) #enemies can generate into the world
    def makeMap(self, here):
        edge = "$" #this map should work on a floor of any size
        for i in range(0,2*self.maxX+1):
            edge +="$$" #make sure the top and bottom edges are the right length
        print(edge) #print the top
        row = 0 #we're going to print each row individually, we need to print the right number so were doing a while loop
        rowStart = self.topleft #grabbing this because we start at the topleft row, each row we work to the right, and then we work down the rows
        while row < 4*self.maxY-1:
            current = rowStart
            to_print = "$" #left edge
            if row % 2: #this row represents north/south doorways and corners
                colomn = 1 #this... was because I didn't want to ruin anything by swapping around the if statements
                while colomn < 4*self.maxX+2:
                    if colomn % 2: #this coordinate represents doorways
                        south = False
                        for x in current.exits: #get if the room this is associated with has a southern exit
                            if "south" == x[0]:
                                south = True
                        if south: #if it does then add a space
                            to_print += " "
                        else: #otherwise add a hashtag for a wall
                            to_print += "#"
                        current = current.getNeighbor("east")
                    else: #this coordinate represents a corner, there is no diagonal doorways so always a wall
                        to_print += "#"
                    colomn +=1
                rowStart = rowStart.getNeighbor("south") #only after we looked at a row's southern doors do we want to shift over the rowstart
            else: #this row represents rooms and east/west doorways
                colomn = 0 #yes the colomns start in different places, I know, it's weird, I know, I just don't want to break anything
                while colomn < 4*self.maxY+1:
                    if colomn % 2: #this coordinate will represent east/west doors
                        east = False
                        for x in current.exits: #check if the room has a door to the east
                            if "east" == x[0]:
                                east = True
                        if east: #if so add space for doorway
                            to_print += " "
                        else: #otherwise add hashtag for wall
                            to_print += "#"
                        current = current.getNeighbor("east")
                    else: #this coordinate will represent a room
                        if current == self.end:
                            to_print += "E" #E for exit
                        elif current == here:
                            to_print += "C" #C for character/current
                        elif current == self.start:
                            to_print += "S" #S for starting point
                        else:
                            to_print += " " #space... for random room
                    colomn += 1
            to_print +="$" #add right edge to string before printing and moving on to next row
            print(to_print)
            row += 1
        print(edge) #print bottom
