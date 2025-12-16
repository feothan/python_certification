total_joltage = 0
file_path = "puzzle_input_3.txt"
K = 12

def max_joltage_k(bank: str, k: int) -> str:
    bank = bank.strip()
    drop = len(bank) - k
    stack = []

    for ch in bank:
        while drop > 0 and stack and stack[-1] < ch:
            stack.pop()
            drop -= 1
        stack.append(ch)

    if drop > 0:
        stack = stack[:-drop]

    return ''.join(stack[:k])

try:
    with open(file_path) as file:
        for line in file:
            best = max_joltage_k(line, K)   # 12-digit best as string
            total_joltage += int(best)      # convert to int for summing

except FileNotFoundError:
    print(f"The file '{file_path}' was not found.")
except Exception as e:
    print(f"Error: {e}")

print(total_joltage)
