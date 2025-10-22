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

def pick_three_options(candidates):
    if not candidates:
        return ["[no match]", "[no match]", "[no match]"]
    common_bin = [w for w in candidates if word_frequency(w, 'en') >= 0.001]
    medium_bin = [w for w in candidates if 0.002 <= word_frequency(w, 'en') < 0.001]
    rare_bin = [w for w in candidates if word_frequency(w, 'en') < 0.0002]
    if not common_bin: common_bin = candidates
    if not medium_bin: medium_bin = candidates
    if not rare_bin: rare_bin = candidates
    common = random.choice(common_bin)
    medium = random.choice(medium_bin)
    rare = random.choice(rare_bin)
    return [common, medium, rare]

# Generate all possible chunks up to max length for a stress pattern
def generate_chunks(pattern, max_len=3):
    """Return all contiguous slices of the pattern up to max_len syllables"""
    chunks = []
    for i in range(len(pattern)):
        for j in range(1, max_len+1):
            if i + j <= len(pattern):
                chunks.append(pattern[i:i+j])
    return chunks

def build_line_interactive(pattern, max_word_syllables=3):
    i = 0
    line = []
    while i < len(pattern):
        remaining = pattern[i:]
        # Try largest possible chunk first
        for size in range(min(max_word_syllables, len(remaining)), 0, -1):
            chunk = remaining[:size]
            candidates = find_words_by_stress(chunk)
            if candidates:
                options = pick_three_options(candidates)
                print(f"\nChunk '{chunk}' options (covers {size} syllable(s)):")
                print(f"1: {options[0]}  2: {options[1]}  3: {options[2]}")
                while True:
                    choice = input("Choose 1, 2, or 3: ").strip()
                    if choice in ['1','2','3']:
                        word = options[int(choice)-1]
                        line.append(word)
                        i += size
                        break
                    else:
                        print("Invalid choice. Enter 1, 2, or 3.")
                break
        else:
            # If no match, fallback to single syllable placeholder
            print(f"No match for syllable '{remaining[0]}', inserting placeholder.")
            line.append("[?]")
            i += 1
    return ' '.join(line)

if __name__ == "__main__":
    pattern_input = input("Enter stress pattern (/-/-/ style, / = stressed, - = unstressed): ").replace(' ','')
    print("\nLet's build your line!")
    final_line = build_line_interactive(pattern_input)
    print(f"\nYour generated line: {final_line}")
