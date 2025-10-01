import json

# Load the file
try:
    with open('bookmarks.json', 'r') as file:
        story = json.load(file)
    print("(Zelia's extracted shortcut data successfully loaded!)\n")
    print("To play, enter the number next to the choice you'd like to make and press enter.\nWhen there are no available choices, just press enter.\n")
except FileNotFoundError:
    print("Error: 'bookmarks.json' not found. Please ensure the file exists.")
    exit()
except json.JSONDecodeError:
    print("Error: Could not decode JSON. Please check the file's format.")
    exit()

# Extract root title
root_title = next(iter(story))
current_node = story[root_title]
print(root_title)

# Main loop
while True:
    # Handle {"final message": {}} as an ending
    if isinstance(current_node, dict) and len(current_node) == 1:
        only_key = next(iter(current_node))
        if current_node[only_key] == {}:
            print(f"\n{only_key}")
            print("\nThe End\n")
            break

    # Handle string or non-dict value
    if not isinstance(current_node, dict):
        print(f"\n{current_node}")
        print("\nThe End\n")
        break

    current_choices = list(current_node)
    print()

    if len(current_choices) == 1:
        # Only one choice — show it without a number, accept anything
        only_choice = current_choices[0]
        print(only_choice)
        input("? ")
        current_node = current_node[only_choice]
    else:
        # Multiple choices — show numbered list and require valid selection
        for i, choice in enumerate(current_choices, 1):
            print(f"{i}. {choice}")

        while True:
            player_input = input("? ").strip()
            if player_input.isdigit():
                selected_index = int(player_input)
                if 1 <= selected_index <= len(current_choices):
                    chosen_key = current_choices[selected_index - 1]
                    current_node = current_node[chosen_key]
                    break
            print("Please enter a valid number.")
