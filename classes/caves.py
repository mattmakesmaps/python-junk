from random import choice, shuffle
import pdb

class Cave(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.here = []
        self.tunnels = []

    def tunnel_to(self, cave):
        """ Create a two-way tunnel """
        self.tunnels.append(cave)
        cave.tunnels.append(self)

    def __repr__(self):
        return "<Cave " + self.name + ">"

cave_names = [
        "Arched Cavern",
        "Saggy Satchel",
        "Nordic Network",
        "Dangerous Dungeon"
        ]

def create_caves():
    shuffle(cave_names)
    caves = [Cave(cave_names[0], "fake desc")]
    for name in cave_names[1:]:
        pdb.set_trace()
        new_cave = Cave(name, name)
        eligable_caves = [cave for cave in caves if len(cave.tunnels) < 3]
        new_cave.tunnel_to(choice(eligable_caves))
        caves.append(new_cave)
    return caves

if __name__ == "__main__":
    for cave in create_caves():
        print cave.name, "=>", cave.tunnels
