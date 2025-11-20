import random

writing_seeds = [
    "A doorway where sound dies.",
    "Someone knitting a memory back together.",
    "A shadow that hesitates.",
    "A familiar voice coming from a place it shouldn’t.",
    "I don’t think this place likes us.",
    "Who taught you to speak like that?",
    "Write 4 sentences. The last one must land like a revelation.",
    "Write one paragraph in which the weather expresses a secret.",
    "Write a scene where two characters are wrong about each other.",
    "Devotion under pressure.",
    "Fear translated into a physical object.",
    "A hope so small it fits under a fingernail."
]

music_seeds = [
    "Play a bass groove built only from chromatic approach notes.",
    "Sing one ascending pattern on ‘oo,’ then invert it descending.",
    "Loop a 2-bar riff; shift its rhythm by one beat every pass.",
    "Play something that sounds like a locked door.",
    "Find the interval that feels like regret and improvise a melody around it.",
    "Use only the A and D strings.",
    "One chord per bar, but never repeat the same inversion twice.",
    "Write a 10-second motif that could be a Mandibles intro.",
    "Create a bassline that implies a chord the guitar never plays."
]

coding_seeds = [
    "Write a function that returns the first repeated element in a list.",
    "Generate a random sequence of steps (N, S, E, W) and calculate final coordinates.",
    "Write a function that prettifies a list of filenames.",
    "Write a 5-line CLI that echoes input with a timestamp.",
    "Draw a waveform in ASCII from random data.",
    "Simulate a firefly blinking pattern in the terminal.",
    "Make a function that moves a sprite toward a target by 1 unit per call.",
    "Generate a simple tilemap in nested lists."
]

print("writing:", writing_seeds[random.randint(0, len(writing_seeds) - 1)])
print("music:", music_seeds[random.randint(0, len(music_seeds) - 1)])
print("coding:", coding_seeds[random.randint(0, len(coding_seeds) - 1)])