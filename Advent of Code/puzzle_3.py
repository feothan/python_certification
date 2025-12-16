total_joltage = 0
file_path = "puzzle_input_3.txt"

try:
    with open(file_path) as file:
        for line in file:
            batteries = list(line.strip())
            sorted_batteries = sorted(batteries)
            if batteries.index(sorted_batteries[-1]) < len(batteries)-1 :
                tens_digit = sorted_batteries[-1]
            else:
                tens_digit = sorted_batteries[-2]
            remaining_batteries = batteries[int(batteries.index(tens_digit) + 1):]
            sorted_remaining_batteries = sorted(remaining_batteries)
            ones_digit = sorted_remaining_batteries[-1]
            joltage = int(tens_digit + ones_digit)
            total_joltage += joltage

except FileNotFoundError:
    print(f"The file '{file_path}' was not found.")
except Exception as e:
    print(f"Error: {e}")

print(total_joltage)