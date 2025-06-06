# Set the stage.
from scripts.regsetup import description

game_over = False
location = "cistern"

# Initiate game data.
rooms = {
    "cistern": {
        'description': "The walls are dark with damp and you're having trouble keeping your balance in the rubble.",
        'contents': ['cat'],
        'exits': {
            'n': "tunnel",
            's': "clearing"
        }
    },
    "tunnel": {
        'description': "Unholy vinework crisscrosses the tunnel, the color of solitary rot.",
        'contents': ['bat'],
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
    "a baseball bat": {
        'description': "It's a Louisville Slugger.",
        'noun': 'bat',
        'location': "tunnel"
    },
    "a small cat": {
        'description': "It's a long-haired black cat named Harold Jr.",
        'noun': 'cat',
        'location': "cistern"
    },
    "the schmoozle": {
        'description': "It's a Louisville Slugger.",
        'noun': 'schmoozle',
        'location': 'inventory'
    }
}

inventory = []
verbs = ['look', 'examine', 'get', 'take', 'drop', 'eat', 'drink', 'open', 'close', 'burn', 'break', 'twist', 'throw', 'attack', 'use', 'say', 'in']

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

    # Compile a list of object tags in the game.
    objects_list = []
    for object in objects:
        objects_list.append(object[2])

    # Make a list of objects that are in the input.
    active_nouns = []
    for word in just_words:
        if word in objects_list:
            active_nouns.append(word)
    return active_verbs, active_nouns

# This is the game loop.
while game_over == False:
    print(f'Location: {location}')
    print(f'Description: {rooms[location]['description']}')

    # Show directions you can go.
    direction_names = ["north ", "south ", "east ", "west ", "up ", "down "]
    directions = ""
    for i in range(6):
        direction_letter = direction_names[i]
        if direction_letter in rooms[location]['exits']:
            directions += direction_names[rooms[location]['exits'].index(rooms[location]['exits'])]
    print(f'Directions: {directions}')

    # Show any objects that are in the room.
    objects_present = ""
    for each in range(len(objects)):
        if objects[each][3] == location:
            objects_present += str(objects[each][0]) + " "
    if objects_present:
        print(f'Objects: {objects_present}\n')
    else:
        print(f'Objects: none')

    # Ask for player input.
    player_move = input("What do you do? ")
    print()

    # Check for 'quit'
    if player_move == "quit":
        print("Thanks for playing! Goodbye.")
        game_over = True
        continue

    # Check for simple direction (n, s, e, w, u, d)
    if len(player_move) == 1 and player_move in room[location]['exits']:
        new_location = room[location]['exits'][player_move]

    # Check for inventory check (i, invent, inventory)
    inventory = ""
    if player_move == "i" or player_move == "invent" or player_move == "inventory":
        for each in range(len(objects)):
            if objects[each][3] == -1:
                inventory += str(objects[each][0]) + "\n"
        if inventory:
            print(f'You are carrying:\n{inventory}')
            continue
        else:
            print(f'You are carrying: nothing.\n')
            continue

    # Call the function to parse for verbs and nouns, check to make sure you get at least one of each.
    verb, noun = parse_text(player_move)
    if len(verb) < 1 or len(noun) < 1:
        print("I don't understand.\n")
        continue

    # # Handle the verb get/take
    # if verb[0] == "get" or verb[0] == "take":
    #     if noun[0] in objects[][2]:
    #         current_noun = objects[][2].index(noun[0])
    # print(current_noun)


    print(f'You can {verb[0]} the {noun[0]}.\n')



