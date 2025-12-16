def is_duplicate_sequence(id):
    length = len(id)
    for divisor in range(2, 9):
        if length % divisor != 0:
            continue  # Can't split evenly, try next divisor
        fraction = length // divisor
        parts = [id[i*fraction:(i+1)*fraction] for i in range(divisor)]
        if len(set(parts)) == 1:
            return True
    return False

file_path = 'puzzle_input_2.txt'

with open(file_path, 'r') as file:
    id_ranges = file.readline().strip()

list_of_tuples = [tuple(map(int, s.split('-'))) for s in id_ranges.split(',')]

total = 0

for start, end in list_of_tuples:
    for id in range(start, end + 1):
        if is_duplicate_sequence(str(id)):
            total += id

print(total)
