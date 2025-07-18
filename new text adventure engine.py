import string
import re

is_first_time = True
game_over = False
location = "tunnel"
most_you_can_carry = 9 # Tiny objects take up no space, small take up 1, medium take up 2, large take up 3, huge items cannot be picked up.
amount_carried = 0

# Initiate game data.
rooms = {
    "cistern": {
        'description': "The walls are dark with damp and you're having trouble keeping your balance in the rubble.",
        'exits': {
            'n': "tunnel",
            's': "clearing"
        }
    },
    "tunnel": {
        'description': "Unholy vinework crisscrosses the tunnel, the color of solitary rot.",
        'exits': {
            's': "cistern"
        }
    },
    "clearing": {
        'description': "There's a tunnel's mouth leading away from this clearing, and a spot the size of an elephant where the grass is mashed down.",
        'exits': {
            'n': "cistern",
            'e': "dead end"
        }
    },
    "dead end": {
        'description': "There's no way out but back, and the squeeze was tight getting here. There's purple ooze on the wall.",
        'exits': {
            'w': "clearing"
        }
    },
    "on a cliff": {
        'description': "You're standing on a cliff, looking at a dilapidated building you suspect was a library.",
        'exits': {
            'e': "library",
            'w': "dead end"
        }
    },
    "library": {
        'description': "You are in a ruined library. The pictures are shredded, but the shelves look untouched, and emanate menace. A spiral staircase is in the center of the room.",
        'exits': {
            'w': "on a cliff",
            'u': "top floor"
        }
    },
    "top floor": {
        'description': "You are at the top of the spiral staircase. The library, here, is destroyed and open to the sky.",
        'exits': {
            'd': "library",
            'e': "meeting room"
        }
    },
    "meeting room": {
        'description': "This is where meetings were held in the library--fifty years ago, a hundred? You can't tell. There's a balcony to the east.",
        'exits': {
            'w': "top floor",
            'n': "balcony"
        }
    },
    "balcony": {
        'description': "You expect to see the expanse of the ruined city, but you see only very tall, very old trees. Could you have gotten turned around in the old library?",
        'exits': {
            's': "meeting room"
        }
    },
    "cozy cave": {
        'description': "This is a cozy little cave. It has all the amenities, but you feel like it would be a crime to touch anything.",
        'exits': {
            'e': "tunnel"
        }
    }
}

sizes = ['tiny', 'small', 'medium', 'large', 'huge']

objects = {
    'bat': {
        'display name': "a baseball bat",
        'description': "It's a Louisville Slugger.",
        'location': 'cozy cave',
        'size': 'medium',
        'special': ['flammable']
    },
    'cat': {
        'display name': "a small cat",
        'description': "It's a long-haired black cat named Harold Jr.",
        'location': 'cistern',
        'size': 'medium',
        'special': ['flammable', 'alive']
    },
    'schmoozle': {
        'display name': "the schmoozle",
        'description': "It's everything you expect it to be.",
        'location': 'clearing',
        'size': 'large',
        'special': ['edible', 'alive']
    },
    'rabbit': {
        'display name': "the rabbit",
        'description': "This is the rabbit of your dreams.",
        'location': 'meeting room',
        'size': 'medium',
        'special': ['edible', 'flammable', 'alive']
    },
    'lighter': {
        'display name': "a gold lighter",
        'description': "It has the initials 'QPN' on it.",
        'location': 'dead end',
        'size': 'small',
        'special': ['igniter']
    },
    'juicebox': {
        'display name': 'a juicebox',
        'description': "It's a raspberry juicebox.",
        'location': 'balcony',
        'size': 'small',
        'special': ['potable']
    },
    'box': {
        'display name': 'a cardboard box',
        'description': "It's a medium-sized box.",
        'location': 'library',
        'size': 'medium',
        'special': ['container'],
        'status': 'closed'
    },
    'paper': {
        'display name': 'a slip of paper',
        'description': "It's paper, with writing on it.",
        'location': 'on a cliff',
        'size': 'tiny',
        'special': ['flammable'],
    },
    'table': {
        'display name': 'a stone table',
        'description': "It would look harmless enough, if not for the blood stains.",
        'location': 'clearing',
        'size': 'huge',
        'special': ['shelf'],
    },
    'rock': {
        'display name': 'the big rock',
        'description': "It's a big rock against a stone wall.",
        'location': 'tunnel',
        'size': 'huge',
        'special': ['moveable'],
        'direction it reveals': 'w',
        'room it leads to': 'cozy cave'
    },
    'ladder': {
        'display name': 'a rope ladder',
        'description': "It's a dangling ladder in the crevice.",
        'location': 'dead end',
        'size': 'huge',
        'special': ['climbable'],
        'room it leads to': 'on a cliff'

    }
}

verbs = {
    'take': {
        'conditions': ['must be in room'],
        'actions': ['moves direct object to inventory'],
        'prepositions': ['on', 'inside', 'with'],
    },
    'drop': {
        'conditions': ['must be in inventory'],
        'actions': ['moves direct object to room'],
        'prepositions': ['on', 'inside', 'with'],
    },
    'examine': {
        'conditions': ['must be in room or inventory'],
        'actions': ['examine object'],
        'prepositions': ['with']
    },
    'open': {
        'conditions': ['must be in room or inventory'],
        'actions': ['change status of direct object to open'],
        'prepositions': ['with']
    },
    'close': {
        'conditions': ['must be in room or inventory'],
        'actions': ['changes status of direct object to closed'],
        'prepositions': ['with']
    },
    'read': {
        'conditions': ['must be in room or inventory'],
        'actions': [],
        'prepositions': ['with']
    },
    'enter': {
        'conditions': ['must be in room', 'must be a door', 'must be open'],
        'actions': ['move player to specified room'],
        'prepositions': []
    },
    'climb': {
        'conditions': ['must be in room', 'must be climbable'],
        'actions': ['move player to specified room'],
        'prepositions': ['with']
    },
    'attack': {
        'conditions': ['must be in room', 'must be alive'],
        'actions': ['begin fight sequence'],
        'prepositions': ['with']
    },
    'eat': {
        'conditions': ['must be edible'],
        'actions': ['destroy direct object', 'enhance player'],
        'prepositions': ['with']
    },
    'drink': {
        'conditions': ['must be potable'],
        'actions': ['destroy direct object', 'enhance player'],
        'prepositions': ['with']
    },
    'throw': {
        'conditions': [],
        'actions': ['moves direct object to room'],
        'prepositions': ['at']
    },
    'activate': {
        'conditions': ['must be in room or inventory'],
        'actions': ['change status of direct object to on'],
        'prepositions': ['with']
    },
    'deactivate': {
        'conditions': ['must be in room or inventory'],
        'actions': ['change status of direct object to off'],
        'prepositions': ['with']
    },
    'burn': {
        'conditions': ['must be flammable'],
        'actions': ['change object'],
        'prepositions': ['with']
    },
    'push': {
        'conditions': ['must be in room', 'must be moveable'],
        'actions': ['reveal direction via moveable'],
        'prepositions': ['with']
    },
    'put': {
        'conditions': ['must be in inventory'],
        'actions': ['place in container or on shelf'],
        'prepositions': ['in', 'on', 'inside']
    }
}

# This is where puzzle logic and a lot of the fun goes. :)
# Game authors, please note that the parser will simplify input so it matches the cases below.

# But first, we put the action, direct object, preposition, and indirect object into one neat package.
def special_case(action, direct_object, preposition, indirect_object):
    components = [var for var in [action, direct_object, preposition, indirect_object] if var is not None]
    player_input = " ".join(components)
    # print(player_input) -- This line lets you check for the distilled form, when you want that!

    if player_input == 'eat schmoozle':
        print("Once it makes eye contact with you, you're lost. You can't go through with it!\n")
        return True
    if player_input == 'burn bat with lighter':
        print("It goes up in a lot of smoke!\n")
        objects[direct_object]['display name'] = 'a crispy bat'
        objects[direct_object]['weight'] = 1
        objects[direct_object]['description'] = "It's a shadow of its former self."
        return True
    if player_input == 'drop cat':
        print("The poor cat, having escaped your grasp, runs as far away as it can get.\n")
        objects[direct_object]['display name'] = 'a spooked cat'
        objects[direct_object]['location'] = 'dead end'
        return True
    return False

# Each occurence of a synonym is switched out of the raw input text in favor of described verbs.
synonyms = {
    'get': 'take',
    'grab': 'take',
    'pick up': 'take',
    'place': 'drop',
    'move': 'push',
    'go': 'enter',
    'in': 'inside',
    'into': 'inside',
    'on top of': 'on',
    'look at': 'examine',
    'kill': 'attack',
    'turn on': 'activate',
    'turn off': 'deactivate'}

# These words will be dropped into the "preposition" slot when detected.
preposition_list = ['on', 'inside', 'with', 'at']

def can_carry(object_id): # Function receives an object name & immediately creates a subdictionary of its stats.
    object_in_question = objects[object_id]
    size = object_in_question.get('size', "") # Gets size
    what_it_weighs = sizes.index(size)

    if amount_carried + what_it_weighs > most_you_can_carry:
        return False

    return True

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
        if token in verbs:
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
            print("The room is empty.\n")

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

    # Process standard responses to verb-direct_object/verb-direct_object-preposition-noun combos.
    if action in verbs:
        verb_data = verbs[action]
        object_location = objects[direct_object]['location']

        # Check basic presence conditions
        conditions = verb_data.get('conditions', [])
        actions = verb_data.get('actions', [])

        # Generate fail responses for when specific conditions are not met.
        failed = False
        for condition in conditions:
            if condition == 'must be in room':
                if objects[direct_object]['location'] == 'inventory':
                    print("You're already holding that.\n")
                    failed = True
                    break
                elif not objects[direct_object]['location'] == location:
                    print("I don't see that here.\n")
                    failed = True
                    break

            elif condition == 'must be in inventory' and not (
                    objects[direct_object]['location'] == 'inventory'
            ):
                print("I'm not carrying that.\n")
                failed = True
                break

            elif condition == 'must be in room or inventory':
                if objects[direct_object]['location'] != 'inventory' and objects[direct_object]['location'] != location:
                    print("I don't that here.\n")
                    failed = True
                    break

            elif condition == 'must be edible' and 'edible' not in objects[direct_object].get('special', []):
                print("That's not edible.\n")
                failed = True
                break
            elif condition == 'must be potable' and 'potable' not in objects[direct_object].get('special', []):
                print("You can't drink that.\n")
                failed = True
                break
            elif condition == 'must be flammable' and 'flammable' not in objects[direct_object].get('special', []):
                print("That's not flammable.\n")
                failed = True
                break
            elif condition == 'must be climbable' and 'climbable' not in objects[direct_object].get('special', []):
                print("You can't climb that.\n")
                failed = True
                break
            elif condition == 'must be alive' and 'alive' not in objects[direct_object].get('special', []):
                print("That wouldn't work.\n")
                failed = True
                break
            elif condition == 'must be a door' and 'door' not in objects[direct_object].get('special', []):
                print("That's not something you can enter.\n")
                failed = True
                break
            elif condition == 'must be open' and objects[direct_object].get('status') != 'open':
                print("It's not open.\n")
                failed = True
                break
            elif condition == 'must be moveable' and 'moveable' not in objects[direct_object].get('special', []):
                print("You can't move that.\n")
                failed = True
                break
            elif action == 'burn':
                if not indirect_object:
                    print("Burn it with what?\n")
                    failed = True
                    break
                if indirect_object not in objects:
                    print("I don't know what that is.\n")
                    failed = True
                    break
                if objects[indirect_object]['location'] != 'inventory':
                    print("You're not holding that.\n")
                    failed = True
                    break
                if 'igniter' not in objects[indirect_object].get('special', []):
                    print("That won't help you start a fire.\n")
                    failed = True
                    break

        if failed:
            continue

        # Special case override... see function immediately after room, object, and verb data.
        if special_case(action, direct_object, preposition, indirect_object):
            continue

        # If the conditions are met, execute the associated standard actions!
        for act in actions:
            if act == 'moves direct object to inventory':
                if object_location == location:
                    size = objects[direct_object].get('size', "")
                    what_it_weighs = sizes.index(size)
                    if size != 'huge':
                        if can_carry(direct_object):
                            objects[direct_object]['location'] = 'inventory'
                            amount_carried += what_it_weighs
                            print(amount_carried, "\n")
                            print("Okay.\n")
                        else:
                            print("I'm carrying too much.\n")
                    else:
                        print("That's too heavy!\n")

            elif act == 'moves direct object to room':
                if object_location == 'inventory':
                    objects[direct_object]['location'] = location
                    size = objects[direct_object].get('size', "")
                    what_it_weighs = sizes.index(size)
                    amount_carried -= what_it_weighs
                    print(amount_carried, "\n")
                    print("You drop it.\n")
                elif object_location == location:
                    print("You're not holding it.\n")
                else:
                    print("I don't see that here.\n")

            elif act == 'destroy direct object':
                objects[direct_object]['location'] = None
                print(f"You {action} it.\n")
            elif act == 'enhance player':
                print("Player enhanced!\n")
            elif act == 'change status of direct object to on':
                objects[direct_object]['status'] = 'on'
                print("Activated.\n")
            elif act == 'change status of direct object to off':
                objects[direct_object]['status'] = 'off'
                print("Deactivated.\n")
            elif act == 'reveal direction via moveable':
                obj = objects[direct_object]
                if (
                        'direction it reveals' in obj
                        and 'room it leads to' in obj
                        and 'moveable' in obj.get('special', [])
                ):
                    direction = obj['direction it reveals']
                    destination = obj['room it leads to']

                    if direction in rooms[location]['exits']:
                        print("You've already revealed the passageway.\n")
                        continue

                    rooms[location]['exits'][direction] = destination

                    dir_full = {
                        'n': 'north', 's': 'south', 'e': 'east',
                        'w': 'west', 'u': 'up', 'd': 'down'
                    }.get(direction, direction)

                    print(f"You push the {obj['display name']}, revealing a passageway to the {dir_full}.\n")
                else:
                    print("You push it, but nothing happens.\n")
            elif act == 'change status of direct object to open':
                objects[direct_object]['status'] = 'open'
                if action == 'push':
                    print(f"You push the {objects[direct_object]['display name']}, revealing a way forward.\n")
                else:
                    print("Opened.\n")
            elif act == 'change status of direct object to closed':
                objects[direct_object]['status'] = 'closed'
                print("Closed.\n")
            elif act == 'move player to specified room':
                if 'room it leads to' in objects[direct_object]:
                    location = objects[direct_object]['room it leads to']
                    is_first_time = True
                    break
                else:
                    print("You can't go there.\n")
            elif act == 'begin fight sequence':
                print(f"You attack the {objects[direct_object]['display name']}.\n")
            elif act == 'change object':
                objects[direct_object]['location'] = None
                print("You change it.\n")
            elif act == 'examine object':
                print(objects[direct_object].get('description', "You see nothing special.") + "\n")
            elif action in ['open', 'close'] and 'openable' not in objects[direct_object].get('special', []):
                print(f"You can't {action} that.\n")
                failed = True
                break
            elif act == 'place in container or on shelf':
                if not indirect_object:
                    print("Where do you want to put it?\n")
                    break

                container = objects[indirect_object]
                item = objects[direct_object]

                # Check if open (if openable), container/shelf, same location
                if container.get('location') != location:
                    print("That isn't here.\n")
                    break
                if 'container' in container.get('special', []) and container.get('status') != 'open':
                    print("It's closed.\n")
                    break
                if 'container' not in container.get('special', []) and 'shelf' not in container.get('special', []):
                    print("You can't put things there.\n")
                    break

                # Check volume constraint
                used = sum(objects[i]['volume'] for i in container.get('contents', []))
                if used + item['volume'] > container['capacity']:
                    print("There's no room.\n")
                    break

                # Move item into container
                container.setdefault('contents', []).append(direct_object)
                item['location'] = indirect_object
                pounds_carried -= item.get('weight', 0)
                volume_carried -= item.get('volume', 0)
                print(f"You place the {item['display name']} {preposition} the {container['display name']}.\n")

                # Success: stop further action execution
                break

        continue