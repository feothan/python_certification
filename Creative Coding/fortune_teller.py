import random

class FortuneTeller:

    def __init__(self, fortunes):
        self.fortunes = fortunes
        self.history_list = []

    def tell_fortune(self):
        fortune_index = random.randint(0,len(self.fortunes)-1)
        fortune = self.fortunes[fortune_index]
        self.history_list.append(fortune_index)
        return fortune

    def get_Counts(self):
        times_each_used = {}
        for fortune_index in self.history_list:
            if fortune_index in times_each_used:
                times_each_used[fortune_index] += 1
            else:
                times_each_used[fortune_index] = 1
        return dict(sorted(times_each_used.items()))

def main():
    fortunes = [
        "Seek help from professionals trained in mental health care.",
        "Your finances will be a key to your financial future.",
        "Only listen to fortune cookie, disregard all other fortune telling units.",
        "You are not illiterate.",
        "You will be hungry again in one hour.",
        "life difficult.",
        "You do not have to worry about your future.",
        "A person is never too old to leNo problem leaves you where you found it.arn.",
        "If you think nobody cares if you are alive, try missing a couple of car payments.",
        "Dogs have owners, cats have staff."
    ]
    presto = FortuneTeller(fortunes)
    for i in range(1000000):
        fortune = presto.tell_fortune()
        print(fortune)
    print(presto.get_Counts())

main()