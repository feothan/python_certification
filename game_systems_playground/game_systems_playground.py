class Player:
    def __init__(self, name, gender, race, fighting_class):
        self.name = name
        self.gender = gender
        self.race = race
        self.fighting_class = fighting_class
    def __str__(self):
        descrip = f"{self.name}\ngender: {self.gender}\nrace: {self.race}\nfighting_class: {self.fighting_class}"
        return descrip

class Triple:
    def __init__(self, item1, value1, item2, value2, item3, value3):
        values = [abs(value1), abs(value2), abs(value3)]
        total = sum(values)

        if total == 0:
            rounded = [0, 0, 0]
        else:
            scaled = [v * 100 / total for v in values]
            integers = [int(v) for v in scaled]
            decimals = [v - int(v) for v in scaled]

            remainder = 100 - sum(integers)

            # Apply remainder to the largest decimals, preserving order
            for _ in range(remainder):
                idx = decimals.index(max(decimals))
                integers[idx] += 1
                decimals[idx] = 0  # ensures no double-selection

            rounded = integers

        self.labels = (item1, item2, item3)
        self.values = rounded

    def __str__(self):
        return ", ".join(f"{label}({value})" for label, value in zip(self.labels, self.values))

fighting_class = Triple("warrior", 9, "mage", 11, "cleric", 13)
gender = Triple("male", 5, "female", 4, "threemale", 1)
race = Triple("dwarf", 1, "orc", 1, "elf", 2)
jeff = Player("Jeff", gender, race, fighting_class)
print (jeff)
