import string
import re

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
    },
    'juicebox': {
        'display name': 'a juicebox',
        'description': "It's a raspberry juicebox.",
        'location': "inventory"
    }
}

# This is where puzzle logic and a lot of the fun goes. :)
# Game authors, please note that the parser will simplify input so it matches the cases below.
def special_case(action, direct_object, preposition, indirect_object):
    components = [var for var in [action, direct_object, preposition, indirect_object] if var is not None]
    player_input = " ".join(components)
    print(player_input)
    if player_input == 'eat schmoozle':
        print("Once it makes eye contact with you, you're lost. You can't go through with it!\n")
        return True
    if player_input == 'burn bat with lighter':
        print("It goes up in a lot of smoke!\n")
        objects[direct_object]['display name'] = 'a crispy bat'
        objects[direct_object]['description'] = "It's a shadow of its former self."
        return True
    if player_input == 'drop cat':
        print("The poor cat, having escaped your grasp, runs as far away as it can get.\n")
        objects[direct_object]['display name'] = 'a spooked cat'
        objects[direct_object]['location'] = 'dead end'
        return True
    return False


edible_objects = ['schmoozle', 'rabbit']
drinkable_objects = ['juicebox']
flammable_objects = ['bat', 'cat']

verb_list = ['take', 'drop', 'examine', 'open', 'close', 'read', 'go', 'climb', 'attack', 'eat', 'drink', 'throw', 'put', 'activate', 'deactivate', 'move', 'burn']
synonyms = {'get': 'take', 'grab': 'take', 'pick up': 'take', 'in': 'inside', 'into': 'inside', 'look at': 'examine', 'kill': 'attack', 'turn on': 'activate', 'turn off': 'deactivate'}
preposition_list = ["at", "from", "under", "on", "to", "with", "inside", "behind", "through"]

def replace_synonyms(text):
    # Sort keys by length (desc) to handle longer phrases first
    sorted_keys = sorted(synonyms.keys(), key=len, reverse=True)

    # Create a regex pattern to match all the synonym keys as full words/phrases
    pattern = r'\b(?:' + '|'.join(re.escape(key) for key in sorted_keys) + r')\b'

    def replacer(match):
        matched_phrase = match.group(0)
        return synonyms[matched_phrase]

    # Replace using the regex pattern
    result = re.sub(pattern, replacer, text)

    return result

# Parse user input for an action, a direct object, a preposition, and an indirect object
# and return the information as a dictionary.
def parse_input(player_input):
    # Convert the input to lowercase
    lowercase_input = player_input.lower()

    # Call function to replace synonyms
    modified_input = replace_synonyms(lowercase_input)

    # Remove punctuation from user input
    cleaned_input = "".join(char for char in modified_input if char not in string.punctuation)

    # Turn input into tokens
    tokens = cleaned_input.split()

    # initiate variables for parts of speech
    action = None
    direct_object = None
    preposition = None
    indirect_object = None

    # Identify parts of speech in player input.
    # Make first verb and noun into action and direct object.
    # Make last preposition and last noun into preposition and indirect object.
    for token in tokens:
        if token in verb_list:
            action = token
        elif token in objects:
            if not direct_object:
                direct_object = token
            else:
                indirect_object = token
        elif token in preposition_list:
            preposition = token

    return action, direct_object, preposition, indirect_object

# This shows the player the room.
def look_at_the_room():
        print(f'Location: {location}')
        print(f'Description: {rooms[location]['description']}')

        # Show directions you can go; could have displayed the 'n', 's', etc., but this is prettier.
        exits = ""
        compass_points = ['north', 'south', 'east', 'west', 'up', 'down']
        for each_exit in rooms[location]['exits']:
            for each in compass_points:
                if each_exit == each[0]:
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
while not game_over:

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

    # Check for failed directional attempts.
    if player_move in ['n', 's', 'e', 'w', 'u', 'd']:
        print("That direction isn't an option.\n")
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

    # Check for blank player_moves and weird attempts at direction.
    if player_move == "" or len(player_move) < 3:
        print("?\n")
        continue

    # Call the function to parse for verbs and nouns, check to make sure you get at least one of each and handle cases.
    action, direct_object, preposition, indirect_object = parse_input(player_move)
    if direct_object and not action:
        if objects[direct_object]['location'] in ['inventory', 'location']:
            print(f"What do you want me to do to {objects[direct_object]['display name']}?\n")
            continue
        else:
            print(f"What do you want me to do?\n")
            continue
    if action and not direct_object:
        print(f"What do you want me to {action}?\n")
        continue

    # Handle the verb look/examine
    if action == 'examine':
        object_location = objects[direct_object]['location']
        if object_location in [location, 'inventory']:
            if special_case(action, direct_object, preposition, indirect_object):
                continue
            else:
                print(objects[direct_object]['description'], "\n")
                continue
        else:
            print("I don't see that here.\n")
            continue

    # Handle the verb get/take
    if action == 'take':
        object_location = objects[direct_object]['location']
        if object_location == 'inventory':
            print("You are already carrying that.\n")
            continue
        elif object_location == location:
            if special_case(action, direct_object, preposition, indirect_object):
                continue
            else:
                objects[direct_object]['location'] = 'inventory'
                print("Okay.\n")
                continue
        else:
            print("I don't see that here.\n")
            continue

    # Handle the verb drop/place
    if action in ['drop', 'place']:
        object_location = objects[direct_object]['location']
        if object_location == "inventory":
            if special_case(action, direct_object, preposition, indirect_object):
                continue
            else:
                objects[direct_object]['location'] = location
                print("You drop it.\n")
                continue
        elif object_location == location:
            print("You're not holding it.\n")
            continue
        else:
            print("I don't see that here.")
            continue

    # Handle the verb eat
    if action == 'eat':
        object_location = objects[direct_object]['location']
        if object_location == "inventory":
            if direct_object in edible_objects:
                if special_case(action, direct_object, preposition, indirect_object):
                    continue
                else:
                    print("You eat it.\n")
                    objects[direct_object]['location'] = None
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

    # Handle the verb drink
    if action == 'drink':
        object_location = objects[direct_object]['location']
        if object_location == 'inventory':
            if direct_object in drinkable_objects:
                if special_case(action, direct_object, preposition, indirect_object):
                    continue
                else:
                    print("You drink it, and throw away the container.\n")
                    objects[direct_object]['location'] = None
                continue
            else:
                print("You can't drink that.\n")
                continue
        elif object_location == location:
            print("I should probably pick it up first.\n")
            continue
        else:
            print("That's not here.\n")
        continue

    # Handle the verb open


    # Handle the verb close

    # Handle the verb burn
    if action == 'burn': # Is it the right verb?
        object_location = objects[direct_object]['location'] # Is the noun either here...
        if object_location == 'inventory': # Or in the inventory?
            if direct_object in flammable_objects: # Is the noun on the list of objects you can burn?
                if indirect_object == 'lighter': # Does the player mention the lighter?
                    if objects['lighter']['location'] == 'inventory': # Are you holding the lighter?
                        if special_case(action, direct_object, preposition, indirect_object):
                            continue
                        else:
                            print("You burn it.\n")
                            objects[direct_object]['location'] = None
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



