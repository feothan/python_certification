import sys
import textwrap

def print_with_wrap(text):
    wrapped_text = textwrap.fill(text, 40)
    print(wrapped_text)
    return


def get_answer(prompt):
    while True:
        print_with_wrap(prompt)
        response = input()
        first_letter = response[:1].lower()
        if first_letter == "y":
            return True
        elif first_letter == "n":
            return False
        else:
            print("Please answer with yes or no (y/n).")

def story_ends(ending):
    print_with_wrap(ending)
    print("\nThe End")
    sys.exit() #End program.

def intro():
    return get_answer(
        "Hello, adventurer! It's the big day. Do you dare to get out of bed? (y/n) "
    )

def part_A():
    return get_answer(
        "You get out of bed, brush your teeth, and schlep to the kitchen. Seated at the table, you see yourself, wearing a ballerina outfit. Your other you says, 'I found this at the back of our closet. You don\'t mind, do you?' Do you mind? (y/n) "
    )

def part_B():
    story_ends(
        "You really think that you are making this decision for yourself. You truly do. But the EveryBellyBeast is weaving its song through your open window. When you succumb sleep, you also succumb to her jaws."
    )

def part_C():
    story_ends(
        "'Oh, silly,' you say, 'how could I mind me? And you look fabulous!' You are very happy together."
    )

def part_D():
    return get_answer(
        "'How could I be okay with you? I'm the real me!' you shout. Your mom appears in the doorway and looks directly at the other you and says, 'Good morning, Dear. Who's your little friend?' You're not sure who you are anymore. And you realize you're shrinking. You could grab the edge of the table to steady yourself. Do you? (y/n) "
    )

def part_E():
    return get_answer(
        "You're shrinking much faster than you anticipated. You manage to grab the edge of the table, but in seconds you're so small that letting go would mean certain death. Do you ask the other you for help? (y/n) "
    )

def part_F():
    story_ends(
        "'I don't think it's intelligent, Darling,' your mother says to OtherYou. They decide to put you in the snake cage and see what happens. Nothing good happens."
    )

def part_G():
    story_ends(
        "Other you is kind, and moves you safely to the table, where you seem to have settled into a height that will allow you to wear Barbie clothes. Your mother thinks you're adorable. OtherYou thinks you're adorable. You live to a ripe old age in the Barbie Dreamhouse."
    )

def part_H():
    story_ends(
        "You get... oh-so-very small. All of the shapes of the world disappear into what look like cosmos. You have a new world to explore!"
    )

def main():
    gets_out_of_bed = intro()
    if not gets_out_of_bed:
        part_B() #First ending.
    is_okay_with_doppelganger = part_A()
    if not is_okay_with_doppelganger:
        part_C() #Second ending.
    grabs_the_edge = part_D()
    if not grabs_the_edge:
        part_H()
    asks_for_help = part_E()
    if not asks_for_help:
        part_F() #Third ending.
    part_G() #Fourth ending.

main()