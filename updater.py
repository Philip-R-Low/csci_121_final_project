updates = []

def updateAll():
    print("updating")
    for u in updates:
        u.update()

def register(thing):
    updates.append(thing)

def deregister(thing):
    updates.remove(thing)
