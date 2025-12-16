file_path = "puzzle_input_1.txt"

dial = 50
times_we_reach_zero = 0

try:
    with open(file_path) as file:
        for line in file:
            instruction = line.strip()
            left_or_right = instruction[0]
            distance = int(instruction[1:])

            # Convert L/R to -1/+1
            direction = 1 if left_or_right == 'R' else -1

            # Check each step along the way
            for step in range(1, distance + 1):
                dial = (dial + direction) % 100  # move one step
                if dial == 0:
                    times_we_reach_zero += 1

except FileNotFoundError:
    print(f"The file '{file_path}' was not found.")
except Exception as e:
    print(f"Error: {e}")

print(f"We reach zero {times_we_reach_zero} times!")
