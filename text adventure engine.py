# Set the stage.
from scripts.regsetup import description
from twisted.conch.scripts.tkconch import exitStatus

is_first_time = True
game_over = False
location = "cistern"

# Initiate game data.
rooms = {
    "cistern": {
        'description': "The walls are dark with damp and you're having trouble keeping your balance in the rubble.",
        'contents': ["a small cat", "the rabbit"],
        'exits': {
            'n': "tunnel",
            's': "clearing"
        }
    },
    "tunnel": {
        'description': "Unholy vinework crisscrosses the tunnel, the color of solitary rot.",
        'contents': ["a baseball bat"],
        'exits': {
            's': "cistern"
        }
    },
    "clearing": {
        'description': "There's a tunnel's mouth leading away from this clearing, and a spot the size of an elephant where the grass is mashed down.",
        'contents': [],
        'exits': {
            'n': "cistern",
            'e': "dead end"
        }
    },
    "dead end": {
        'description': "There's no way out but back, and the squeeze was tight getting here. There's purple ooze on the wall.",
        'contents': [],
        'exits': {
            'w': "clearing"
        }
    }

}

objects = {
    'bat': {
        'display name': "a baseball bat",
        'description': "It's a Louisville Slugger.",
        'location': "tunnel"
    },
    'cat': {
        'display name': "a small cat",
        'description': "It's a long-haired black cat named Harold Jr.",
        'location': "cistern"
    },
    'schmoozle': {
        'display name': "the schmoozle",
        'description': "It's everything you expect it to be.",
        'location': 'clearing'
    },
    'rabbit': {
        'display name': "the rabbit",
        'description': "This is the rabbit of your dreams.",
        'location': "cistern"
    },
    'lighter': {
        'display name': "a gold lighter",
        'description': "It has the initials 'QPN' on it.",
        'location': "dead end"
    }
}

# This is where puzzle logic and a lot of the fun goes. :)
def special_cases(verb, noun):
    if verb[0] == 'eat' and noun[0] == 'schmoozle':
        print("Once it makes eye contact with you, you're lost. You can't go through with it!\n")
        return True
    if verb[0] == 'burn' and noun[0] == 'bat' and 'lighter' in noun:
        print("It goes up in a lot of smoke!\n")
        objects[noun[0]]["display name"] = 'a crispy bat'
        objects[noun[0]]["description"] = "It's a shadow of its former self."
        return True
    if verb[0] in ['drop', 'place'] and noun[0] == 'cat':
        print("The poor cat, having escaped your grasp, runs as far away as it can get.\n")
        objects[noun[0]]["display name"] = 'a spooked cat'
        objects[noun[0]]["location"] = 'dead end'
        return True
    return False


edible_objects = ['schmoozle', 'rabbit']
flammable_objects = ['bat', 'cat']

verbs = ['look', 'examine', 'get', 'take', 'drop', 'place', 'eat', 'drink', 'open', 'close', 'burn', 'break', 'twist', 'throw', 'attack', 'use', 'say', 'in']

# Parse user input for verbs and nouns and return a list of each.
def parse_text(user_input):

    # Make lowercase.
    lowercase_move = player_move.lower()

    # Strip away punctuation.
    chars_to_remove = ["!", "?", ".", ",", ";"]
    stripped_move = "".join([char for char in lowercase_move if char not in chars_to_remove])

    # Turn the input into a list of words.
    just_words = stripped_move.split(" ")

    # Make a list of verbs that are in the input.
    active_verbs = []
    for word in just_words:
        if word in verbs:
            active_verbs.append(word)

    # Make a list of objects that are in the input.
    active_nouns = []
    for word in just_words:
        if word in objects:
            active_nouns.append(word)

    # Return verbs and nouns lists.
    return active_verbs, active_nouns

# This shows the player the room.
def look_at_the_room():
        print(f'Location: {location}')
        print(f'Description: {rooms[location]['description']}')

        # Show directions you can go; could have displayed the 'n', 's', etc., but this is prettier.
        exits = ""
        compass_points = ['north', 'south', 'east', 'west', 'up', 'down']
        for exit in rooms[location]['exits']:
            for each in compass_points:
                if exit == each[0]:
                    exits += each + " "

        # Check if there are no exits
        if not exits.strip():  # If exits is empty or only whitespace
            exits = "none"

        print(f'Exits: {exits}')

        # Show any objects that are in the room.
        contents = " - ".join(
            objects[item]["display name"] for item in objects if objects[item]["location"] == location
        )

        # Display the contents
        if contents:
            print(f"You see: {contents}")
        else:
            print("The room is empty.")

# This is the game loop.
while game_over == False:

    # Display room info if the game has just started.
    if is_first_time:
        look_at_the_room()
        is_first_time = False

    # Ask for player input.
    player_move = input("What do you do? ")
    print()

    # Check for 'quit'
    if player_move in ['quit', 'goodbye']:
        print("Thanks for playing! Goodbye.")
        game_over = True
        continue

    # Check for simple direction (n, s, e, w, u, d)
    if len(player_move) == 1 and player_move in rooms[location]['exits']:
        location = rooms[location]['exits'][player_move]
        is_first_time = True
        continue

    # Check for inventory check (i, invent, inventory)
    if player_move in ["i", "invent", "inventory"]:
        display_inventory = " - ".join(
            objects[item]["display name"] for item in objects if objects[item]["location"] == "inventory"
        )
        if display_inventory:
            print(f'You are carrying:\n{display_inventory}\n')
        else:
            print("You're not carrying anything.\n")
        continue

    # Check for 'look' request
    if player_move in ["look", "l"]:
        look_at_the_room()
        is_first_time = False
        continue

    # Check for failed directional attempts.
    if player_move in ['n', 's', 'e', 'w', 'u', 'd']:
        print("That direction isn't an option.\n")
        continue

    # Check for blank player_moves and weird attempts at direction.
    if player_move == "" or len(player_move) < 3:
        print("?\n")
        continue

    # Call the function to parse for verbs and nouns, check to make sure you get at least one of each and handle cases.
    verb, noun = parse_text(player_move)
    if len(verb) == 0 and len(noun) > 0:
        if objects[noun[0]]["location"] == "inventory" or objects[noun[0]]["location"] == location:
            print(f"What do you want me to do to {objects[noun[0]]["display name"]}?\n")
            continue
        else:
            print(f"What do you want me to do?\n")
            continue
    if len(noun) == 0 and len(verb) > 0:
        print(f"What do you want me to {verb[0]}?\n")
        continue

    # Handle the verb look/examine
    if verb[0] in ['look', 'examine']:
        object_location = objects[noun[0]]['location']
        if object_location == location or object_location == "inventory":
            if special_cases(verb, noun) == True:
                continue
            else:
                print(objects[noun[0]]["description"], "\n")
                continue
        else:
            print("I don't see that here.\n")
            continue

    # Handle the verb get/take
    if verb[0] in ['get', 'take']:
        object_location = objects[noun[0]]['location']
        if object_location == "inventory":
            print("You are already carrying that.\n")
            continue
        elif object_location == location:
            if special_cases(verb, noun) == True:
                continue
            else:
                objects[noun[0]]['location'] = "inventory"
                print("Okay.\n")
                continue
        else:
            print("I don't see that here.\n")
            continue

    # Handle the verb drop/place
    if verb[0] in ['drop', 'place']:
        object_location = objects[noun[0]]['location']
        if object_location == "inventory":
            if special_cases(verb, noun) == True:
                continue
            else:
                objects[noun[0]]['location'] = location
                print("You drop it.\n")
                continue
        elif object_location == location:
            print("You're not holding it.\n")
            continue
        else:
            print("I don't see that here.")
            continue

    # Handle the verb eat
    if verb[0] == 'eat':
        object_location = objects[noun[0]]['location']
        if object_location == "inventory":
            if noun[0] in edible_objects:
                if special_cases(verb, noun) == True:
                    continue
                else:
                    print("You eat it.\n")
                    objects[noun[0]]['location'] = "oblivion"
                continue
            else:
                print("That's not edible.\n")
                continue
        elif object_location == location:
            print("I should probably pick it up first.\n")
            continue
        else:
            print("That's not here.\n")
        continue

    # Handle the verb burn
    if verb[0] == 'burn': # Is it the right verb?
        object_location = objects[noun[0]]['location'] # Is the noun either here...
        if object_location == "inventory": # Or in the inventory?
            if noun[0] in flammable_objects: # Is the noun on the list of objects you can burn?
                if "lighter" in noun: # Does the player mention the lighter?
                    if objects["lighter"]["location"] == "inventory": # Are you holding the lighter?
                        if special_cases(verb, noun) == True:
                            continue
                        else:
                            print("You burn it.\n")
                            objects[noun[0]]['location'] = "oblivion"
                            continue
                    else:
                        print("That might work, but you don't have one of those.\n")
                else:
                    print("Burn it with what?\n")
                    continue
            else:
                print("That's not flammable.\n")
                continue
        elif object_location == location:
            print("I should probably pick it up first.\n")
            continue
        else:
            print("That's not here.\n")
        continue



