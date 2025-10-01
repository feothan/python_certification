class Treasure:
    def __init__(self, name, points):
        self.name = name
        self.points = points

class Room:
    def __init__(self, name, treasure_list, dir_dictionary):
        self.name = name
        self.treasure_list = treasure_list
        self.dir_dictionary = dir_dictionary

    def transfer_treasure(self, player):
        player.treasure_list += self.treasure_list
        self.treasure_list = []

    def add_dir(self, dir, room):
        if dir in ['north', 'south', 'east', 'west', 'up', 'down']:
            self.dir_dictionary[dir] = room

class Player:
    def __init__(self, name, treasure_list, location):
        self.name = name
        self.treasure_list = treasure_list
        self.location = location

    def points(self):
        total = 0
        for treasure in self.treasure_list:
            total += treasure.points
        return total

    def choose_dir(self):
        directions_comma = ", ".join(self.location.dir_dictionary)

        waiting = True
        while waiting:
            options = ["north", "south", "east", "west", "up", "down"]
            short_options = ['n', 's', 'e', 'w', 'u', 'd']
            choice = input(f"Choose a direction ({directions_comma}): ")

            if len(choice) == 1 and choice in short_options:
                choice = options[short_options.index(choice)]

            if choice in options and choice in self.location.dir_dictionary:
                self.location = self.location.dir_dictionary[choice]
                waiting = False
            else:
                print("No room in that direction; enter another direction.")

class Game:
    def __init__(self, player, exit_room, win_points):
        self.player = player
        self.exit_room = exit_room
        self.win_points = win_points
        self.still_playing = True

    def run(self):
        while self.still_playing:
            room = self.player.location
            if len(room.treasure_list) > 0:
                treasure_descriptions = []
                for treasure in room.treasure_list:
                    treasure_descriptions.append(f"{treasure.name} ({treasure.points})")
                treasure_comma = ", ".join(treasure_descriptions)
                print(f"{room.name}\nYou see: {treasure_comma}")
                print("You put everything in your backpack.")
                self.player.location.transfer_treasure(self.player)
            else:
                print(f"{self.player.location.name}\nYou see: no treasure")

            print(f"You have {self.player.points()} points")

            if self.player.location == self.exit_room:
                if self.win_points > self.player.points():
                    print("The door beckons you but you need 700 points to open it!")
                else:
                    print("You open the door and reach a beautiful room of life-sized dolls\nand treasure. You live happily ever after with your riches.")
                    print(f"Congratulations {self.player.name} on winning the game!")
                    self.still_playing = False
                    break

            self.player.choose_dir()

            print()


treasure1 = Treasure('Flower', 5)
treasure2 = Treasure('Gold Statue', 50)
treasure3 = Treasure('Intricately Carved Ivory Elephants', 100)
treasure4 = Treasure('Human Skull', 40)
treasure5 = Treasure('Broken Teacup', 5)
treasure6 = Treasure('Old Tome', 20)
treasure7 = Treasure('Fancy Painting', 30)
treasure8 = Treasure('Bookworm', 5)
treasure9 = Treasure('Tiger Skin Rug', 56)
treasure10 = Treasure('Biscuits', 10)
treasure11 = Treasure('Fancy Teapot', 20)
treasure12 = Treasure('Bug', 1)
treasure13 = Treasure('Katana', 38)
treasure14 = Treasure('A Small Unicorn Figurine', 20)
treasure15 = Treasure('Tons of Old Dolls', 50)
treasure16 = Treasure('Camera and Rolls of Film', 50)
treasure17 = Treasure('A Beautifully Carved Statue', 100)
treasure18 = Treasure('Jewelry', 100)

room1 = Room('Grassy Clearing', [], {})
room2 = Room('Dead End', [treasure1], {})
room3 = Room('Entrance to an Abandoned House', [], {})
room4 = Room('House Entryway', [treasure2], {})
room5 = Room('Living Room', [treasure3], {})
room6 = Room('Small Closet', [treasure4], {})
room7 = Room('Dining Room', [treasure5], {})
room8 = Room('Library Room', [treasure6, treasure7, treasure8], {})
room9 = Room('Furnished Room', [treasure9], {})
room10 = Room('Small Room with an Odd-Looking Door', [], {})
room12 = Room('Kitchen', [treasure10, treasure11], {})
room13 = Room('Pantry', [treasure12], {})
room14 = Room('Decorated Room with Stair Going Up', [], {})
room15 = Room('Small Room', [treasure13], {})
room16 = Room('Hallway with Fancy Red Carpets', [], {})
room17 = Room('Bathroom', [treasure14], {})
room18 = Room("Child's Bedroom", [treasure15], {})
room19 = Room("Adjoining Child's Bedroom", [treasure16], {})
room20 = Room('Queen Bedroom with Ladder up to Third Floor', [treasure17], {})
room21 = Room('One Big Room Full of Human Skeletons Adorned with Jewelry', [treasure18], {})

room1.dir_dictionary = {'south': room2, 'east': room3}
room2.dir_dictionary = {'north': room1}
room3.dir_dictionary = {'west': room1, 'east': room4}
room4.dir_dictionary = {'west': room3, 'north': room12, 'east': room7, 'south': room5}
room5.dir_dictionary = {'north': room4, 'east': room6}
room6.dir_dictionary = {'west': room5}
room7.dir_dictionary = {'west': room4, 'north': room14, 'east': room8}
room8.dir_dictionary = {'west': room7, 'down': room9}
room9.dir_dictionary = {'up': room8, 'east': room10}
room10.dir_dictionary = {'west': room9}
room12.dir_dictionary = {'south': room4, 'north': room13}
room13.dir_dictionary = {'south': room12}
room14.dir_dictionary = {'south': room7, 'east': room15, 'up': room16}
room15.dir_dictionary = {'west': room14}
room16.dir_dictionary = {'west': room20, 'north': room18, 'east': room17, 'down': room14}
room17.dir_dictionary = {'west': room16}
room18.dir_dictionary = {'south': room16, 'east': room19}
room19.dir_dictionary = {'west': room18, 'south': room16}
room20.dir_dictionary = {'east': room16, 'up': room21}
room21.dir_dictionary = {'down': room20}

name = input("What's your name again?: ")
print(f"Oh, hi {name}. Let's play the game!\n")
player = Player(name, [], room1)
game1 = Game(player, room10, 700)
game1.run()