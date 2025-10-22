import nltk
from nltk.corpus import cmudict
from wordfreq import word_frequency
import random

# Ensure CMU dictionary is downloaded
nltk.download('cmudict')

cmu = cmudict.dict()


def get_stress(word):
    pronunciations = cmu.get(word.lower())
    if not pronunciations:
        return None
    pron = pronunciations[0]
    stress = ''.join(['/' if '1' in s else '-' for s in pron if s[-1].isdigit()])
    return stress


def find_words_by_stress(pattern):
    matches = []
    for word in cmu.keys():
        s = get_stress(word)
        if s == pattern:
            matches.append(word)
    return matches


# Pick three options using frequency thresholds
def pick_three_options(candidates):
    if not candidates:
        return ["[no match]", "[no match]", "[no match]"]

    # Separate into bins using frequency thresholds
    common_bin = [w for w in candidates if word_frequency(w, 'en') >= 0.0001]
    medium_bin = [w for w in candidates if 0.002 <= word_frequency(w, 'en') < 0.0001]
    rare_bin = [w for w in candidates if word_frequency(w, 'en') < 0.0002]

    # If a bin is empty, fallback to available words
    if not common_bin: common_bin = candidates
    if not medium_bin: medium_bin = candidates
    if not rare_bin: rare_bin = candidates

    # Pick one randomly from each bin
    common = random.choice(common_bin)
    medium = random.choice(medium_bin)
    rare = random.choice(rare_bin)

    return [common, medium, rare]


def split_pattern(pattern):
    chunks = []
    i = 0
    while i < len(pattern):
        if i + 2 <= len(pattern):
            chunks.append(pattern[i:i + 2])
            i += 2
        else:
            chunks.append(pattern[i])
            i += 1
    return chunks


def build_line_interactive(pattern):
    chunks = split_pattern(pattern)
    line = []
    for idx, chunk in enumerate(chunks):
        candidates = find_words_by_stress(chunk)
        options = pick_three_options(candidates)
        print(f"\nChunk {idx + 1} (pattern '{chunk}') options:")
        print(f"1: {options[0]}  2: {options[1]}  3: {options[2]}")
        while True:
            choice = input("Choose 1, 2, or 3: ").strip()
            if choice in ['1', '2', '3']:
                line.append(options[int(choice) - 1])
                break
            else:
                print("Invalid choice. Enter 1, 2, or 3.")
    return ' '.join(line)


if __name__ == "__main__":
    pattern_input = input("Enter stress pattern (/-/-/ style, / = stressed, - = unstressed): ").replace(' ', '')
    print("\nLet's build your line!")
    final_line = build_line_interactive(pattern_input)
    print(f"\nYour generated line: {final_line}")
