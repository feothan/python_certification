# Set the stage.
game_over = False
location = 1

# Initiate game data.
rooms = [["dummy room", "This is where the description would go, in real life... followed by nsewud directions.", [0, 0, 0, 0, 0, 0]],
["cistern", "The walls are dark with damp and you're having trouble keeping your balance in the rubble.", [2, 3, 0, 0, 0, 0]],
["tunnel", "Unholy vinework crisscrosses the tunnel, the color of solitary rot.", [0, 1, 0, 0, 0, 0, 0]],
["clearing", "There's a tunnel's mouth leading away from this clearing, and a spot the size of an elephant where the grass is mashed down.", [1, 0, 4, 0, 0, 0, 0]],
["dead end", "There's no way out but back, and the squeeze was tight getting here. There's purple ooze on the wall.", [0, 0, 0, 3, 0, 0]]]

objects = [["a baseball bat", "It's a Louisville Slugger.", "bat", 2],
           ["a small cat", "It's a long-haired black cat named Harold Jr.", "cat", 1],
           ["the schmoozle", "It's everything you expect it to be.", "schmoozle", -1]]

verbs = ["look", "examine", "get", "take", "drop", "eat", "drink", "open", "close", "burn", "break", "twist", "throw", "attack", "use", "say", "in"]

# Parse user input for verbs and nouns and return a list of each.
def parse_text(user_input):

    # Make lowercase.
    lowercase_move = player_move.lower()

    # Strip away punctuation.
    chars_to_remove = ["!", "?", ".", ",", ";"]
    stripped_move = "".join([char for char in lowercase_move if char not in chars_to_remove])

    # Turn the input into a list of words.
    just_words = stripped_move.split(" ")

    # Make a list of verbs (by number) that are in the input.
    active_verbs = []
    for word in just_words:
        if word in verbs:
            active_verbs.append(word)

    # Compile a list of object tags in the game.
    objects_list = []
    for object in objects:
        objects_list.append(object[2])

    # Make a list of objects (by number) that are in the input.
    active_nouns = []
    for word in just_words:
        if word in objects_list:
            active_nouns.append(word)
    return active_verbs, active_nouns

# This is the game loop.
while game_over == False:
    print(f'Location: {rooms[location][0]}')
    print(f'Description: {rooms[location][1]}')

    # Show directions you can go.
    direction_names = ["north ", "south ", "east ", "west ", "up ", "down "]
    directions = ""
    for i in range(6):
        direction_number = rooms[location][2][i]
        if direction_number:
            direction_name = direction_names[i]
            directions += direction_name
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
    direction_letters = ["n", "s", "e", "w", "u", "d"]
    if len(player_move) == 1 and player_move in direction_letters:
        which_direction = direction_letters.index(player_move)
        new_location = rooms[location][2][which_direction]
        location = new_location
        continue

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

    # Handle the verb get/take
    if verb[0] == "get" or verb[0] == "take":
        if noun[0] in objects[][2]:
            current_noun = objects[][2].index(noun[0])
    print(current_noun)


    print(f'You can {verb[0]} the {noun[0]}.\n')


