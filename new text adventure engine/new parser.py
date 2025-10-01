import string

synonyms = {'get': 'take', 'grab': 'take', 'pick up': 'take', 'into': 'inside', 'look at': 'examine', 'kill': 'attack', 'turn on': 'activate', 'turn off': 'deactivate'}
verb_list = ['take', 'drop', 'examine', 'open', 'close', 'read', 'go', 'climb', 'attack', 'eat', 'drink', 'throw', 'put', 'activate', 'deactivate', 'move']
noun_list = ["bowl", "shelf", "oyster", "wheelbarrow", "lamp", "sword", "rug", "leaflet", 'door', 'window', 'book', 'gold', 'jewels', 'knife', 'newspaper', 'magazine', 'rock', 'case']
preposition_list = ["at", "from", "under", "on", "to", "with", "inside", "behind", "through"]

def parse_input(player_input):
    # Convert the input to lowercase
    lowercase_input = player_input.lower()

    # Switch out all synonyms with standard language
    modified_input = lowercase_input
    for key in sorted(synonyms.keys(), key=len, reverse=True):
        modified_input = modified_input.replace(key, synonyms[key])
    # for key in synonyms:
    #     modified_input = modified_input.replace(key, synonyms[key])



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
        elif token in noun_list:
            if not direct_object:
                direct_object = token
            else:
                indirect_object = token
        elif token in preposition_list:
            preposition = token

    return {
        "action": action,
        "direct object": direct_object,
        "preposition": preposition,
        "indirect object": indirect_object
    }

print(parse_input(input("What would you like to do next? ")))