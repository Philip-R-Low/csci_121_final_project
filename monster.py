import os
import random
import updater

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Monster:
    def __init__(self, name, health, room, strength, speed, level, ev, acc):
        self.name = name
        self.health = health
        self.room = room
        self.strength = strength #maximum damage in combat
        self.speed = speed #attack speed in combat
        self.level = level
        self.evasion = ev #chance to dodge in combat
        self.accuracy = acc #chance to hit in combat
        self.spotted_player = False #if the monster has spotted the player
        self.inCombat = None
        room.addMonster(self)
        updater.register(self)
    def update(self):
        #the order of these conditions are important
        #the player shouldn't be suprise attacked by a monster if they haven't seen it yet
        #but the player shouldn't have to chase a monster
        #so the attack goes first, then check for player, then the move
        active = random.random() #active means attacking the player if the player is in the same room and not invis, moving otherwise
        if active < .5 and self.spotted_player and self.room.hasPlayer:
            if self.room.hasPlayer[0].invisible:
                pass
            else:
                self.attackPlayer(self.room.hasPlayer[0])
        if len(self.room.hasPlayer):
            self.spotted_player=True
        if active < .5 and not self.spotted_player and len(self.room.hasPlayer):
            #if the player has seen the monster, or moves to the monster it sits
            self.moveTo(self.room.randomNeighbor())
    def moveTo(self, room):
        self.room.removeMonster(self)
        self.room = room
        room.addMonster(self)
    def die(self):
        player = self.inCombat
        print()
        print("You win. " + self.name + " is dead.")
        player.inCombat = False
        player.gainExp(max(100+40*(self.inCombat.level-self.level),20))
        print()
        input("Press enter to continue...")
        if random.random() < .5: #roll for loot
            self.room.floor.placeRandomItem(self.room)
        self.room.removeMonster(self)
        updater.deregister(self)
    def enterCombat(self, player):
        self.inCombat = player
    def attackPlayer(self, player):
        player.inCombat = self
        self.enterCombat(player)
        clear()
        print("The " + self.name+" attacks you by suprise")
        self.strike()
    def strike(self):
        player = self.inCombat
        hitRoll = random.randint(1,100)
        if hitRoll < 100-self.accuracy:
            print("The "+self.name+" misses you.")
        elif hitRoll < 100-self.accuracy+player.evasion:
            print("You dodge the "+self.name+".")
        else:
            damage = random.randint(1,self.strength)
            complete_block = random.randint(0,1)
            damage = max(complete_block, damage-player.resistance)
            player.health -= damage
            print("The "+self.name+" hits you for "+str(damage)+" damage")
        if player.health <= 0:
            print("You die.")
            print()
            input("Press enter to exit...")
            self.inCombat.alive = False
    def take_damage(self, n):
        #helper function for player strikes and spells
        self.health -= n
        if self.health <= 0:
            self.die()
