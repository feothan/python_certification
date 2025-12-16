def is_double_sequence(s):
    n = len(s)
    if n % 2 != 0:
        return False  # Can’t split evenly in half
    half = n // 2
    return s[:half] == s[half:]  # First half equals second half

file_path = 'puzzle_input_2.txt'

with open(file_path, 'r') as file:
    id_ranges = file.readline().strip()

list_of_tuples = [tuple(map(int, s.split('-'))) for s in id_ranges.split(',')]

total = 0

for start, end in list_of_tuples:
    for id in range(start, end + 1):
        if is_double_sequence(str(id)):
            total += id

print(total)
