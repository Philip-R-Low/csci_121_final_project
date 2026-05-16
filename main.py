from room import Room
from player import Player
from item import Item
from item import Armor
from item import Weapon
from item import Usable
from monster import Monster
from floor import Floor
import os
import updater
import random

#Enemy data
#Order: Name, Health, Max Damage, attack speed, level, evasion chance, base hit chance, probability weight
rat = ["Rat", 8, 3, 10, 1, 10, 60, 5]
bat = ["Bat", 8, 3, 8, 1, 30, 50, 5]
roach = ["Giant Roach", 5, 1, 6, 1, 50, 50, 5]
cat = ["Feral Cat", 25, 6, 10, 2, 30, 50, 4]
snake = ["Snake", 15, 5, 8, 2, 10, 60, 4]
hyena = ["Hyena", 25, 7, 10, 2, 5, 70, 4]
wolf = ["Wolf", 30, 10, 10, 3, 5, 60, 3]
jackal = ["Jackal", 25, 8, 10, 2, 5, 70, 4]
croc = ["Crocodile", 50, 20, 15, 4, 5, 60, 2]
lizard = ["Monitor Lizard", 40, 10, 10, 3, 15, 80, 3]
bear = ["Bear", 60, 20, 17, 4, 5, 5, 60, 2]

#Item data
#Weapons
#Order: Class, name, description, weight, damage, unweildly, type, speed, probability weight
dagger = ["Weapon", "Dagger", "A dagger. Fast swing. It increases your potential damage by 4 and does not lower your accuracy", 1, 4, 0, 6, "Dagger", 7]
sword = ["Weapon", "Sword", "A sword. Average swing. It increases your potential damage by 6 but lowers accuracy by 5%", 3, 6, 5, 10, "Sword", 4]
axe = ["Weapon", "Axe", "An Axe. Slow swing. It increases your potential damage by 8, but lowers accuracy by 10%", 5, 8, 10, 12, "Axe", 1]
spear = ["Weapon", "Spear", "A spear. Fast swing. It increases your potential damage by 6, but lowers accuracy by 10%", 5, 6, 10, 8, "Axe", 3]
#Armor
#Order: Class, name, description, weight, resistance, encumberance, type, probability weight
hat = ["Armor", "Hat", "A plain cloth hat. Reduces damage taken by 1", 1, 1, 0, "head", 2]
helmet = ["Armor", "Helmet", "A simple metal helmet. Reduces damage taken by 2 but reduces evasion by 1.", 2, 2, 1, "head", 2]
tshirt = ["Armor", "Tshirt", "A t-shirt with a corporate logo on it. Reduces damage by 1", 1, 1, 0, "chest", 10]
leather = ["Armor", "Leather Jacket", "A leater jacket. Reduces damage taken by 4, but reduces evasion by 2.", 2, 4, 2, "chest", 5]
studded = ["Armor", "Studded Leather Jacket", "A leather jacket. Someone put small pieces of metal on it. Reduces damage taken by 5, but reduces evasion by 2.", 3, 5, 2, "chest", 2]
chain = ["Armor", "Chainmail Shirt", "A shirt made of chains. Reduces damage taken by 10, but reduces evasion by 10.", 5, 10, 10, "chest", 3]
scale = ["Armor", "Scalemail Shirt", "A chestplate made of overlapping metal plates. Reduces damage taken by 15, but reduces evasion by 15.", 8, 15, 15, "chest", 3]
pants = ["Armor", "Pants", "Denim Jeans. Reduces damage taken by 1, but reduces evasion by 1.", 1, 1, 1, "legs", 8]
pleather = ["Armor", "Leather Pants", "Leather Pants. Reduces damage taken by 3 but reduces evasion by 2." ,2, 3, 2, "legs", 5]
pchain = ["Armor", "Chainmail Pants", "Who wear pants made of chains? You if you equip this. Reduces damage taken by 5, but reduces evasion by 5", 4, 5, 5, "legs", 3]
pscale = ["Armor", "Scale Pants", "Pants made of overlapping metal plates. Reduces damage taken by 7, but reduces evasion by 7", 6, 7, 7, "legs", 3]
shoes = ["Armor", "Shoes", "Normal tenis shoes. Reduces damage taken by 1", 1, 1, 0, "feet", 8]
boots = ["Armor", "Boots", "Combat boots. Reduces damage taken by 3 but decreases evasion by 1", 2, 3, 1, "feet", 4]
gloves = ["Armor", "Gloves", "Gardening gloves. Reduces damage taken by 1, but decreases evasion by 2", 0, 1, 2, "hands", 5]
gauntlets = ["Armor", "Gauntlets", "Gloves, but metal. Reduces damage taken by 3, but decreases evasion by 3", 2, 3, 3, "hands", 2]
#Usables
#Order: class, name, description, weight, type, probability weight
spellbook = ["Usable", "Spellbook", "A spellbook, read it to learn a random spell.", 1, "consume", 1]
hpot = ["Usable", "Health Potion", "A health potion, use it to heal by up to 10.", 1, "consume", 6]
mpot = ["Usable", "Mana Potion", "A mana potion, use it to restore up to 10 mana points.", 1, "consume", 4]
ipot = ["Usable", "Invisibility Potion", "A potion that makes you invisible, use it to stop enemies from attacking you or increase evasion in combat", 1, "consume", 1]

player = Player()
#floor data
#floors need to know what items and enemies they can generate
f1m = [rat,bat,cat,roach]
f1i = [dagger,sword,axe,spear,tshirt,leather,pants,pleather,shoes,boots,spellbook,hpot,mpot]
f2m = [rat,bat,cat,roach,snake,hyena]
f2i = [dagger,sword,axe,spear,tshirt,leather,studded,chain,pants,pleather,pchain,shoes,boots,gloves,spellbook,hpot,mpot,ipot]
f3m = [rat,bat,cat,snake,hyena,jackal,wolf]
f3i = [dagger,sword,axe,spear,tshirt,leather,studded,chain,scale,pants,pleather,pchain,pscale,shoes,boots,gloves,gauntlets,spellbook,hpot,mpot,ipot]
f4m = [snake,hyena,jackal,wolf,bear,croc,lizard]
#since f3i has all items, it's the item list for floor 4 as well

#spell data
all_spells = ['Ice Shard', 'Fireball', 'Lightning Bolt', 'Flame', 'Frost', 'Zap', 'Cure', 'Blink', 'Teleport', 'Inferno', 'Ice Blast', 'Thunder Nova', 'Drain Touch', 'Invisibility']
combat_spells = ['Ice Shard', 'Fireball', 'Lightning Bolt', 'Flame', 'Frost', 'Zap', 'Cure', 'Blink', 'Teleport', 'Inferno', 'Ice Blast', 'Thunder Nova', 'Drain Touch', 'Invisibility']
noncombat_spells = ['Cure','Teleport','Invisibility']
spell_level = {'Ice Shard':1,'Fireball':1,'Lightning Bolt':1, 'Flame':1, 'Frost':1, 'Zap':1, 'Cure':1, 'Blink':2, 'Teleport':2, 'Inferno':3, 'Ice Blast':3, 'Thunder Nova':3, 'Drain Touch':4, 'Invisibility':4}
spell_mana = {'Ice Shard':3,'Fireball':3,'Lightning Bolt':3, 'Flame':1, 'Frost':1, 'Zap':1, 'Cure':5, 'Blink':8, 'Teleport':8, 'Inferno':10, 'Ice Blast':10, 'Thunder Nova':10, 'Drain Touch':8, 'Invisibility':10}
spell_desc = {'Ice Shard':'Deal 3d6 ice damage', 'Fireball':'Deal 3d6 fire damage', 'Lightning Bolt':'Deal 3d6 Lightning damage', 'Flame':'Choose X amount of time to use. Deal Xd3 fire damage',
'Frost': 'Choose X amount of time to use. Deal Xd3 ice damage', 'Zap': 'Choose X amount of time to use. Deal Xd3 lightning damage', 'Cure': 'Heal up to 4 times your level health', 'Blink':'Teleport to a connected room, ending combat',
    'Teleport':'Teleport to a random room on your current floor', 'Inferno': 'Deal 10d10 fire damage','Ice Blast': 'Deal 10d10 ice damage', 'Thunder Nove': 'Deal 10d10 lightning damage',
    'Drain Touch':'Deal 5d6 necrotic damage, heal that much', 'Invisibility': 'Turn invisible'}

def createWorld():
    f1 = Floor("Floor 1", 10, 10, f1m, f1i)
    f1.makeFloorLayout()
    f1.placeItems(20)
    f1.placeEnemies(40)
    f2 = Floor("Floor 2", 10, 10, f2m, f2i)
    f2.makeFloorLayout()
    f1.giveNextFloor(f2)
    f2.placeItems(20)
    f2.placeEnemies(30)
    f3 = Floor("Floor 3", 10, 10, f2m, f3i)
    f3.makeFloorLayout()
    f2.giveNextFloor(f3)
    f3.placeItems(20)
    f3.placeEnemies(30)
    f4 = Floor("Floor 4", 10, 10, f2m, f3i)
    f4.makeFloorLayout()
    f3.giveNextFloor(f4)
    f4.placeItems(20)
    f4.placeEnemies(30)
    player.location = f1.start
    f1.start.hasPlayer = [player] #this is so the starting room knows the player is there
    map = Usable("Map", "Who needs a map? You. You need a map.", 0)
    map.putInRoom(f1.start)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def printSituation():
    clear()
    print(player.location.desc)
    print()
    if player.location.hasMonsters():
        print("This room contains the following monsters:")
        for m in player.location.monsters:
            print(m.name)
        print()
    if player.location.hasItems():
        print("This room contains the following items:")
        for i in player.location.items:
            print(i.name)
        print()
    print("You can go in the following directions:")
    for e in player.location.exitNames():
        print(e)
    #I added hearing as a feauture so that the player
    hear_Anything = False
    for e in player.location.exits:
        if len(e[1].monsters)>0:
            hear_Anything = True
    if hear_Anything:
        print()
        for e in player.location.exits:
            if len(e[1].monsters)>0:
                print("You hear noises to the "+e[0])
    if player.location == player.location.floor.end and player.location.floor.nextFloor == None:
        #This is basically the "victory screen" but it does't end the game
        print("You found the final destination... for now.")
        print("I hope you enjoyed, more features and gameplay to come.")
    print()

def showHelp():
    clear()
    #certain commands are only usable in combat, and other are only usable out of combat
    if player.inCombat == False:
        print("go <direction> -- moves you in the given direction")
        print("inventory -- opens your inventory")
        print("pickup <item> -- picks up the item")
        print("drop <item> -- drops the item")
        print("wait -- twiddle your thumbs and let time pass")
        print("attack <moster> -- initiates combat with an enemy")
    else:
        print("strike -- attack with your weapon or fist")
        print("retreat -- run away from your enemy. Warning: they will get a free attack in.")
    print("equip <item> -- equips an item from inventory")
    print("unequip <item> -- unequips an item")
    print("spells -- describes spells you know and gives their mana cost")
    print("me -- displays player's information")
    print("use <item> -- uses an item that isn't a weapon or armor")
    print("inspect <item/monster> -- inspects an item in your inventory, equipped or in the room, or a monster in the room")
    print("quit -- exits the game")
    print()
    input("Press enter to continue...")

createWorld()
clear()
#the player picks a class
while player.background != "warrior" and player.background != "mage" and player.background != "rogue":
    if player.background!= None: #doesn't show on first input
        print("Invalid class")
    print("Pick a class")
    #I found players often didn't realize they had starting items so I put this message in
    print("This choice will determine your starting capabilities and items.")
    print("Warrior, Rogue, or Mage")
    print()
    c = input().lower()
    player.background = c.lower()
if player.background == "warrior":
    player.increaseStr(6)
    s = Weapon("Sword", "A sword. Average swing. It increases your potential damage by 6 but lowers accuracy by 5%", 3, 6, 5, 10, "Sword")
    s.putInRoom(player.location)
    player.pickup(s)
    player.equip(s)
elif player.background == "rogue":
    player.increaseDex(6)
    k = Weapon("Dagger", "A dagger. Fast swing. It increases your potential damage by 4 and does not lower your accuracy", 1, 4, 0, 6, "Dagger")
    k.putInRoom(player.location)
    player.pickup(k)
    player.equip(k)
    s = Armor("Shoes", "Normal tenis shoes. Reduces damage taken by 1", 1, 1, 0, "feet")
    s.putInRoom(player.location)
    player.pickup(s)
    player.equip(s)
elif player.background == "mage":
    player.increaseInt(6)
    for i in range(0,2):
        s = Usable("Spellbook", "A spellbook, read it to learn a random spell.", 1, "consume")
        s.putInRoom(player.location)
        player.pickup(s)
playing = True
regen_timer = 0
while playing and player.alive:
    if player.inCombat == False:
        printSituation() #combat situation is different from normal situation
    commandSuccess = False
    timePasses = False
    combatTimer = 0 #this is to avoid calling before defining
    while player.inCombat != False and player.alive and playing:
        if combatTimer > player.inCombat.speed:
            #I considered making enemies attack at 0 or 1 instead of at their speed, but harmed a few spells so I decided against it
            player.inCombat.strike() #player.inCombat is the monster, to reduce lines I don't always define a variable for it
            combatTimer-=player.inCombat.speed
        if not player.alive:
            break #this is to not allow the player to attack once after death
        player.combatStatus()
        commandSuccess = True
        command = input("What now? ")
        commandWords = command.split()
        if len(command)==0:
            print("Please give a command.")
            commandSuccess = False
        elif commandWords[0].lower() == "strike": #strike is a basic attack
            player.strike()
            combatTimer+=player.attackSpeed
        elif commandWords[0].lower() == "retreat":
            player.inCombat.strike() #enemy get's free attack
            print()
            input("Press enter to continue...") #make sure the player sees the result
            player.inCombat.inCombat = False
            player.inCombat = False
        elif commandWords[0].lower() == "help":
            showHelp()
        elif commandWords[0].lower() == "quit":
            playing = False
        elif commandWords[0].lower() == "equip":
            targetName = command[6:]
            target = player.getItemByName(targetName)
            if target != False:
                if type(target).__name__ != "Weapon" and type(target).__name__!= "Armor":
                    #only weapons and armor are equipable
                    print("Sorry, "+targetName+" cannot be equipped")
                    commandSuccess = False
                else:
                    player.equip(target)
            else:
                print("No such item in inventory")
                commandSuccess = False
        elif commandWords[0].lower() == "unequip":
            targetName = command[8:]
            target = player.getEquippedItemByName(targetName)
            if target != False:
                player.unequip(target)
            else:
                print("No such item equipped")
                commandSuccess = False
        elif commandWords[0].lower() == "me":
            player.displayMe()
        elif commandWords[0].lower() == "use":
            targetName = command[4:].lower()
            target = player.getItemByName(targetName)
            if target != False:
                #I made the functionality of most items go here, with the exception of the map because their so simple
                if targetName == "map":
                    print("The map is important, but now is not the time to read it.")
                    commandSuccess = False
                elif targetName == "health potion":
                    heal = min(player.maxMP-player.mana,10)
                    player.manaPoints += heal
                    target.consume()
                    print("You restore "+str(heal)+" mana points.")
                    if heal<10:
                        print("Hey if you didn't know, you can heal for up to 10 points with those things.")
                    print()
                    input("Press enter to continue...")
                    combatTimer+=5
                elif targetName == "mana potion":
                    heal = min(player.maxMP-player.mana,10)
                    player.manaPoints += heal
                    target.consume()
                    print("You restore "+str(heal)+" mana points.")
                    if heal<10:
                        print("Hey if you didn't know, you can heal for up to 10 points with those things.")
                    print()
                    input("Press enter to continue...")
                    combatTimer+=5
                elif targetName == "Invisibility potion":
                    combatTimer -= 100
                    target.consume()
                    print("You turn invisible. You have a chance to get some actions in without getting it.")
                    print()
                    input("Press enter to continue...")
                elif targetName == "spellbook":
                    options = []
                    for i in all_spells:
                        if spell_level[i] <= player.level and (i not in player.spellsC or i not in player.spellsNC):
                            options.append(i)
                    chosen = random.choice(options)
                    if chosen in combat_spells:
                        player.spellsC.append(chosen)
                    if chosen in noncombat_spells:
                        player.spellsNC.append(chosen)
                    combatTimer+=20
                else:
                    print("Sorry, "+target.name+" is not a usable item. Try equipping instead.")
                    commandSuccess = False
            else:
                target = player.getEquippedItemByName(targetName)
                if target != False:
                    #This error is here because a tester tried to use a dagger to initiate combat
                    print("You don't have to use that, it is already equipped.")
                else:
                    print("No such item.")
                commandSuccess = False
        elif commandWords[0].lower() == "spells":
            clear()
            #order of combat and noncombat switches depending on if you're in combat
            print("You know the following combat spells:")
            for i in player.spellsC:
                print(str(spell_mana[i])+"| "+i+": "+spell_desc[i])
            print()
            print("You know the following non-combat spells:")
            for i in player.spellsNC:
                print(str(spell_mana[i])+"| "+i+": "+spell_desc[i])
            print()
            input("Press enter to continue...")
        elif commandWords[0].lower() == "magic":
            mon = player.inCombat
            spellName = command[6:].lower()
            realSpell = False
            #this is to give a more specific error in case spellName isn't actually a spell
            for i in all_spells:
                if spellName == i.lower():
                    realSpell = True
                    spellName = i
            if realSpell == False:
                print("That is not a spell.")
                commandSuccess = False
            #the difference in the next three error messages are to spare the player from some confusion
            elif spellName not in player.spellsC:
                if spellName in player.spellsNC:
                    print("You can't cast that in combat.")
                    commandSuccess = False
                else:
                    print("You don't not know that spell.")
                    commandSuccess = False
            elif player.manaPoints < spell_mana[spellName]:
                print("You don't have the mana to cast that spell.")
                commandSuccess = False
            else:
                #this is so I don't do this 3 separate times
                if spellName in ["Fireball", "Flame", "Inferno"]:
                    flavor = "burn "
                elif spellName in ["Ice Shard", "Frost", "Ice Blast"]:
                    flavor = "chill "
                elif spellName in ["Lightning Bolt", "Zap", "Thunder Nova"]:
                    flavor = "shock "
                if spellName == "Cure":
                    confirm = None
                    #cure worns if the player is not actually getting any value out of it
                    if player.health == player.maxHealth:
                        print("You have full health, are you sure you want to use Cure?")
                        print("Enter y to confirm or n to deny")
                        while confirm != "y" or confirm !="n":
                            if confirm is not None:
                                print("Invalid input")
                            confirm = input()
                        if confirm == "n":
                            print("Okay then.")
                            commandSuccess = False
                    if confirm == None or confirm == 'y':
                        heal = min(random.randint(1,player.level*4),player.maxHealth-player.health)
                        player.health += heal
                        print("You heal for "+str(heal))
                        combatTimer+=10
                        player.manaPoints -= spell_mana["Cure"]
                elif spellName == "Ice Shard" or spellName == "Fireball" or spellName == "Lightning Bolt":
                    damage = 0
                    for i in range(0,3):
                        roll = random.randint(1,6)
                        damage += roll
                    player.manaPoints -= spell_mana["Ice Shard"]
                    print("You "+flavor+" the "+mon.name+" for "+str(damage)+" damage.")
                    mon.take_damage(damage)
                    combatTimer+=10
                elif spellName == "Zap" or spellName == "Frost" or spellName == "Flame":

                    print("Determine how long you want to use the spell for.")
                    print("Note that unit of time costs 1 mana")
                    print("Also note that the enemy striking will interupt your spell")
                    ammount = None
                    while type(ammount) != int or ammount > player.manaPoints or ammount < 0:
                        if type(ammount) != int and ammount != None:
                            print("Please put in a positive integer, or put 0 to cancel")
                        elif ammount < 0:
                            print("You can't use the spell for negative time. Positive integer or 0 please.")
                        elif ammount > player.manaPoints:
                            print("Slow down, you don't have that much mana, the most you can put is "+str(player.manaPoints))
                        ammount = input()
                        try:
                            ammount=int(ammount)
                        except:
                            pass
                    end = False
                    while not end:
                        damage = 0
                        mana_used = 0
                        #these are the spells that would be messed up by monsters attacking on 1
                        if combatTimer > mon.speed or ammount == 0 or mon.health<= damage:
                            end = True
                        else:
                            roll = random.randint(0,3)
                            print(roll)
                            damage += roll
                            ammount -= 1
                            combatTimer += 1
                            mana_used += 1
                    print("You spend "+str(mana_used)+"to "+flavor+" the"+mon.name+" for "+str(damage)+" damage.")
                    mon.take_damage(damage)
                    player.manaPoints -= mana_used
                elif spellName == "Blink":
                    print("Are you sure you want to blink? This will teleport you to a neighboring room and end combat")
                    print("Enter y to confirm or n to cancel")
                    print()
                    confirm = None
                    while confirm not in ["y","n"]:
                        if confirm != None:
                            print("Please put y to confirm or n to deny")
                            print()
                        confirm =  input()
                    if confirm == "n":
                        print("Okay then.")
                        commandSuccess = False
                    if confirm == "y":
                        clear()
                        print("Confirmed")
                        targetName = None
                        while targetName not in player.location.exitNames():
                            if targetName != None:
                                print("Invald direction")
                            print("You can move in the following directions")
                            for e in player.location.exitNames():
                                print(e)
                            print()
                            targetName = input()
                        #the following lines are to not break the monster's attack functionality
                        player.location.hasPlayer = []
                        mon.inCombat = False
                        player.inCombat = False
                        player.goDirection(targetName)
                        player.location.hasPlayer = [player]
                        player.manaPoints -= spell_mana["Blink"]
                elif spellName == "Teleport":
                    clear()
                    print("Are you sure you want to teleport? This will move you somewhere random and end combat.")
                    print("Type y to confirm or n to deny")
                    confirm = None
                    while confirm not in ['y', 'n']:
                        if confirm is not None:
                            print("y to confirm, n to deny")
                        print()
                        confirm = input()
                    if confirm == 'n':
                        print("Okay then.")
                    else:
                        new_room = player.location
                        while new_room == player.location:
                            new_room = random.choice(player.location.floor.rooms)
                        #same lines in blink, same purpose
                        mon.inCombat = False
                        player.inCombat = False
                        player.location.hasPlayer = []
                        player.location = new_room
                        player.location.hasPlayer.append(player)
                        player.manaPoints -= spell_mana["Teleport"]
                elif spellName == "Inferno" or spellName == "Iceblast" or spellName == "Thunder Nova":
                    damage = 0
                    for i in range(0,10):
                        roll = random.randint(1,10)
                        damage += roll
                    player.manaPoints -= spell_mana["Inferno"]
                    print("You "+flavor+"the "+mon.name+" for "+str(damage)+" damage.")
                    mon.take_damage(damage)
                    combatTimer+=15
                elif spellName == "Drain Touch":
                    damage = 0
                    for i in range(0,5):
                        damage += random.randint(1,6)
                    print("You drain "+str(damage)+" from the "+mon.name+".")
                    player.manaPoints -= spell_mana["Drain Touch"]
                    player.health = min(player.maxHealth, player.health+damage)
                    mon.take_damage(damage)
                    combatTimer+=10
                elif spellName == "Invisibility":
                    print("You go invisible, this should last about 100 units of time.")
                    player.manaPoints -= spell_mana["Invisibility"]
                    combatTimer -= 100
        elif commandWords[0].lower() == "inspect":
            targetName = command[8:].lower()
            target = player.getItemByName(targetName)
            #these are meant to be if and not elif, because they should all trigger if the intended target is a monster
            if target == False:
                target = player.getEquippedItemByName(targetName)
            if target == False:
                target = player.location.getItemByName(targetName)
            if target == False:
                target = player.location.getMonsterByName(targetName)
            if target != False:
                clear()
                c = type(target).__name__
                if c=="Monster":
                    print("This is a "+target.name+".")
                    print("It has "+str(target.health)+" health.")
                    print("It can hit for "+str(target.strength)+" damage ("+str(target.accuracy-player.evasion)+"% to hit).")
                    print("Your chance to hit it is "+str(player.accuracy-target.evasion)+"%.")
                    print("It has an attack rate of "+str(target.speed)+".")
                elif c=="Weapon":
                    print(target.desc)
                    print("This has an attack rate of "+str(target.speed)+".")
                    print("It weighs "+str(target.weight)+".")
                else:
                    print(target.desc)
                    print("It weights "+str(target.weight)+".")
                print()
                input("Press enter to continue...")
            else:
                print("No such item or monster")
        else:
            print("Not a valid command")
            commandSuccess = False
    while not commandSuccess and player.inCombat == False:
        commandSuccess = True
        command = input("What now? ")
        commandWords = command.split()
        if len(command)==0:
            #this stops the game from crashing if command is empty
            print("Please give a command.")
            commandSuccess = False
        elif commandWords[0].lower() == "go":   #cannot handle multi-word directions
            targetName = commandWords[1].lower()
            exitExists = False
            for x in player.location.exits:
                if targetName == x[0]:
                    exitExists = True
            if exitExists:
                player.location.hasPlayer = []
                player.goDirection(commandWords[1].lower())
                player.location.hasPlayer = [player]
                timePasses = True
            else:
                print("No such exit.")
                commandSuccess = False
        elif commandWords[0].lower() == "pickup":  #can handle multi-word objects
            targetName = command[7:]
            target = player.location.getItemByName(targetName)
            if target != False:
                if player.checkCarryWeight(target) != False: #checks if carryweight would go over with new item
                    player.pickup(target)
                else:
                    print("You're carring too much to pick that up.")
                    commandSuccess = False
            else:
                print("No such item.")
                commandSuccess = False
        elif commandWords[0].lower() == "drop":
            targetName = command[5:]
            target = player.getItemByName(targetName)
            if target == False: #checks equipped items if not in inventory
                target = player.getEquippedItemByName(targetName)
                if target != False:
                    player.unequip(target) #unequip to then drop in rest of command
            if target != False:
                player.drop(target)
            else:
                print("No such item.")
                print()
                commandSuccess = False
        elif commandWords[0].lower() == "inventory":
            player.showInventory()
        elif commandWords[0].lower() == "help":
            showHelp()
        elif commandWords[0].lower() == "quit":
            playing = False
        elif commandWords[0].lower() == "attack":
            targetName = command[7:]
            target = player.location.getMonsterByName(targetName)
            if target != False:
                player.attackMonster(target) #enters combat loop, see above
                combatTimer = 0
            else:
                print("No such monster.")
                commandSuccess = False
        elif commandWords[0].lower() == "equip":
            targetName = command[6:]
            target = player.getItemByName(targetName)
            if target == False: #allows player to equip from ground
            #it tired my figures to have to type two commands when bug fixing
            #that's why I did this
                target = player.location.getItemByName(targetName)
                if player.checkCarryWeight(target) != False and target != False:
                    player.pickup(target)
            if target != False:
                if type(target).__name__ != "Weapon" and type(target).__name__!= "Armor":
                    #only weapons and armor can be equipped
                    print("Sorry, "+targetName+" cannot be equipped")
                    commandSuccess = False
                else:
                    player.equip(target)
            else:
                print("No such item in inventory.")
                print()
                commandSuccess = False
        elif commandWords[0].lower() == "unequip":
            targetName = command[8:]
            target = player.getEquippedItemByName(targetName)
            if target != False:
                player.unequip(target)
            else:
                print("No such item equipped.")
                print()
                commandSuccess = False
        elif commandWords[0].lower() == "spells":
            clear()
            print("You know the following non-combat spells:")
            for i in player.spellsNC:
                print(str(spell_mana[i])+"| "+i+": "+spell_desc[i])
            print()
            print("You know the following combat spells:")
            for i in player.spellsC:
                print(str(spell_mana[i])+"| "+i+": "+spell_desc[i])
            print()
            input("Press enter to continue...")
        elif commandWords[0].lower() == "magic":
            #see combat version for notes on this spell
            #invisibility is the only spell that works differently in combat vs out of combat
            spellName = command[6:].lower()
            realSpell = False
            for i in all_spells:
                if spellName == i.lower():
                    realSpell = True
                    spellName = i
            if realSpell == False:
                print("That is not a spell.")
                commandSuccess = False
            elif spellName not in player.spellsNC:
                if spellName in player.spellsC:
                    print("You can't cast that out of combat.")
                    commandSuccess = False
                else:
                    print("You don't not know that spell.")
                    commandSuccess = False
            elif player.manaPoints < spell_mana[spellName]:
                print("You don't have the mana to cast that spell.")
                commandSuccess = False
            else:
                if spellName == "Cure":
                    confirm = None
                    if player.health == player.maxHealth:
                        print("You have full health, are you sure you want to use Cure?")
                        print("Enter y to confirm or n to deny")
                        while confirm != "y" or confirm !="n":
                            if confirm is not None:
                                print("Invalid input")
                            confirm = input()
                        if confirm == "n":
                            print("Okay then.")
                            commandSuccess = False
                    if confirm == None or confirm == 'y':
                        heal = max(random.randint(1,player.level*4),player.maxHealth-player.health)
                        player.health += heal
                        print("You heal for "+str(heal))
                        player.manaPoints -= spell_mana["Cure"]
                elif spellName == "Teleport":
                    clear()
                    print("Are you sure you want to teleport? This will move you somewhere random.")
                    print("Type y to confirm or n to deny")
                    confirm = None
                    while confirm not in ['y', 'n']:
                        if confirm is not None:
                            print("y to confirm, n to deny")
                        print()
                        confirm = input()
                    if confirm == 'n':
                        print("Okay then.")
                    else:
                        new_room = player.location
                        while new_room == player.location:
                            new_room = random.choice(player.location.floor.rooms)
                        player.location.hasPlayer = []
                        player.location = new_room
                        player.location.hasPlayer.append(player)
                        player.manaPoints -= spell_mana["Teleport"]
                elif spellName == "Invisibility":
                    print("You go invisible, this will only last until you take a time consuming action.")
                    player.invisible = True #goes away on first time passed
                    player.manaPoints -= spell_mana["Invisibility"]
        elif commandWords[0].lower() == "wait":
            timePasses = True
        elif commandWords[0].lower() == "me":
            player.displayMe()
        elif commandWords[0].lower() == "use":
            targetName = command[4:].lower()
            target = player.getItemByName(targetName)
            if target != False:
                if targetName == "map": #this sucked to make. please appreciate it
                    floor = player.location.floor
                    clear()
                    print("Do you want to see the full map?")
                    print("Enter y for the full map, or n to see the stairs coordinates.")
                    full = None
                    while full not in ['y', 'n']:
                        if full is not None:
                            print("Please enter y or n")
                        print()
                        full = input()
                    clear()
                    if full == 'y':
                        player.location.floor.makeMap(player.location)
                    else:
                        print("The exit for this floor is at ("+str(floor.finalX)+","+str(floor.finalY)+").")
                    print()
                    input("Press enter to continue...")
                elif targetName == "health potion":
                    #heals for 10 or up to max health, whichever is lower
                    heal = min(player.maxHealth-player.health,10)
                    player.health += heal
                    target.consume()
                    print("You heal "+str(heal)+" hit points.")
                    if heal<10:
                        #in case players don't inspect these potions, because they likely won't
                        print("Hey if you didn't know, you can heal for up to 10 points with those things.")
                    print()
                    input("Press enter to continue...")
                elif targetName == "mana potion":
                    #health potions but for mana
                    heal = min(player.maxMP-player.mana,10)
                    player.manaPoints += heal
                    target.consume()
                    print("You restore "+str(heal)+" mana points.")
                    if heal<10:
                        print("Hey if you didn't know, you can heal for up to 10 points with those things.")
                    print()
                    input("Press enter to continue...")
                elif targetName == "invisibility potion":
                    #works same as invisiblility spell, both in and out of combat
                    player.invisible = True
                    target.consume()
                    print("You turn invisible. You will remain so until you take a turn")
                    print()
                    input("Press enter to continue...")
                elif targetName == "spellbook":
                    #players learn a random spell they don't already know but are high enough level for
                    options = []
                    for i in all_spells:
                        if spell_level[i] <= player.level and (i not in player.spellsC and i not in player.spellsNC):
                            options.append(i)
                    if len(options) == 0: #this should never happen, but just in case
                        print("Unfortunately there are no spells you can lear right now.")
                        commandSuccess = False
                    else:
                        chosen = random.choice(options)
                        if chosen in combat_spells:
                            player.spellsC.append(chosen)
                        if chosen in noncombat_spells:
                            player.spellsNC.append(chosen)
                        target.consume()
                else:
                    #Error message because of tester action
                    print("Sorry, "+target.name+" is not a usable item. Try equipping instead.")
                    commandSuccess = False
            else:
                target = player.getEquippedItemByName(targetName)
                if target != False:
                    #This is because a tester tried to enter use dagger to attack
                    print("You don't have to use that, it is already equipped.")
                else:
                    print("No such item.")
                commandSuccess = False
        elif commandWords[0].lower() == "inspect":
            targetName = command[8:].lower()
            target = player.getItemByName(targetName)
            #these are supposed to be if not elif, it's supposed to go through all if it's a monster
            #otherwise the command wouldn't work on whatever gets skipped
            if target == False:
                target = player.getEquippedItemByName(targetName)
            if target == False:
                target = player.location.getItemByName(targetName)
            if target == False:
                target = player.location.getMonsterByName(targetName)
            if target != False:
                clear()
                c = type(target).__name__
                if c=="Monster":
                    print("This is a "+target.name+".")
                    print("It has "+str(target.health)+" health.")
                    print("It can hit for "+str(target.strength)+" damage ("+str(target.accuracy-player.evasion)+"% to hit).")
                    print("Your chance to hit it is "+str(player.accuracy-target.evasion)+"%.")
                    print("It has an attack rate of "+str(target.speed)+".")
                elif c=="Weapon":
                    print(target.desc)
                    print("This has an attack rate of "+str(target.speed)+".")
                    print("It weighs "+str(target.weight)+".")
                else:
                    print(target.desc)
                    print("It weights "+str(target.weight)+".")
                print()
                input("Press enter to continue...")
            else:
                print("No such item or monster")
        else:
            print("Not a valid command")
            commandSuccess = False
    if timePasses == True:
        #Here's the basic idea for regen: the player should be able to slowly regenerate health for free, with the rate increasing by level
        #If enough time has passed and the player has something to regenerate, then do, otherwise just let the value sit until they do
        #regen_timer reduced by player.rr instead of set to 0 so player can gain extra regen charging by leveling up
        if regen_timer < player.rr:
            regen_timer += 1
        if (player.health < player.maxHealth or player.manaPoints <player.maxMP) and regen_timer >= player.rr:
            regen_timer -= player.rr
            player.health = max(player.health+1, player.maxHealth)
            player.manaPoints = max(player.manaPoints+1, player.maxMP)
        player.invisible = False #invisiblility potion or spell used out of combat wears off after time passes
        updater.updateAll()
