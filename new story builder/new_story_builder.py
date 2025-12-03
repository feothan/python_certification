import random

wants = [
    "to be forgiven ('Tell me I’m not the worst thing I’ve ever done.')",
    "to be chosen ('Pick me over the world, just once.')",
    "to be understood ('See the reason under the wreckage.')"
    "to be trusted ('Let me matter enough to be believed.')",
    "to be needed ('I want a place in your life that isn’t replaceable.')",
    "to be seen as good ('Please don’t see the monster I fear I am.')",
    "to regain what was lost ('Give me back the moment where everything went wrong.')"
]
fears = [
    "to be exposed ('If you know the truth, you’ll look at me differently.')",
    "to be left again ('You already hurt me once. I can’t survive a second time.')",
    "to be responsible ('If I act, I might break everything.')",
    "to be powerless ('I can’t bear being the one who can’t help.')",
    "to be the villain ('What if every awful thing they said about me was right?')",
    "to be forgotten ('If you stop caring, I might stop existing.')",
    "to be wrong about the past ('If I admit the truth, my entire identity collapses.')"
]

still_looking = True
while still_looking:
    random_want = wants[random.randint(0, len(wants) - 1)]
    random_fear = fears[random.randint(0, len(fears) - 1)]
    print (f"One character just wants {random_want}\nand the other is afraid {random_fear}.")
    right_one = input ("Does this work for you? ")
    if right_one in ["y", "yes"]:
        still_looking = False

