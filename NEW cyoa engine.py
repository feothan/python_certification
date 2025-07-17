import subprocess
game_title_page = "\n\nWelcome to\nBusScape!\n"
game_not_over = True
page = 1
clear_screen_after_each_page = False

story_pages = {
    1: {
        'description': "You're on the bus. Your stop's ahead.",
        'choices': {
            "Pull the chord.": 2,
            "Look at your phone.": 3
        }
    },
    2: {
        'description': "The bus driver opens the doors, but there's a dude wearing a rabbit mascot outfit in your way!",
        'choices': {
            "Push the rabbit dude out of the way.": 4,
            "Ask him (or her) politely to step aside.": 5,
            "Try to climb out the window.": 7
        }
    },
    3: {
        'description': "The bus driver gets distracted by the very funny video on your phone and crashes the bus. You die.",
        'choices': None
    },
    4: {
        'description': "Rabbit dude is a super-tough dudette, and she wipes the floor with you.",
        'choices': None
    },
    5: {
        'description': "In rabbit language, your polite words sound very angry.",
        'choices': {
            "More.": 6
        }
    },
    6: {
        'description': "The rabbit folds you up into a tiny cube and puts you in her purse.",
        'choices': None
    },
    7: {
        'description': "You climb out the window to freedom. And terrible traffic injury.",
        'choices': None
    }
}

print(game_title_page)
while game_not_over:
    if clear_screen_after_each_page:
        subprocess.run("cls" if subprocess.os.name == "nt" else "clear", shell=True)

    print(story_pages[page]['description'])

    choices = story_pages[page]['choices']
    if not choices:
        print("\nTHE END")
        game_not_over = False
        break

    print("Choices:")
    for num, choice in enumerate(choices):
        print(f"{num + 1}: {choice}")

    while True:
        try:
            decision = int(input("\nWhat do you do? "))
            if 0 < decision <= len(choices):
                page = story_pages[page]['choices'][(list(choices)[decision - 1])]
                break  # break out of input loop, not game loop
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")