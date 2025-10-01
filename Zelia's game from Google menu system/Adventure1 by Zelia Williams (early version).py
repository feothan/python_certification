import subprocess
game_title_page = "\n\nWelcome to\nAdventure 1\nby Zelia Williams\n"
game_not_over = True
page = 1
clear_screen_after_each_page = False

story = {
    "Adventure1": {
        'cave': 2
        'swamp': 3
        }
    },
    2: {
        'text': "you see two paths",
        'right': 3
        'left': 0
        }
    },
    3: {
        'description': "you head down a rocky underground path",
        'choices': {
            1: {'choice': "more", 'go_to_page': 4},
    },
    4: {
        'description': "Rabbit dude is a super-tough dudette, and she wipes the floor with you.",
        'choices': None
    },
    5: {
        'description': "In rabbit language, your polite words sound very angry.",
        'choices': {
            1: {'choice': "More.", 'go_to_page': 6}
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
    for num, choice_info in choices.items():
        print(f"{num}: {choice_info['choice']}")

    while True:
        try:
            decision = int(input("\nWhat do you do? "))
            if decision in choices:
                page = choices[decision]['go_to_page']
                print('\n')
                break  # break out of input loop, not game loop
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")