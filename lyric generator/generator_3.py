import nltk
from nltk.corpus import cmudict, wordnet
from wordfreq import word_frequency
import random

# Ensure required NLTK data is downloaded
nltk.download('cmudict')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

cmu = cmudict.dict()


def get_stress(word):
    pronunciations = cmu.get(word.lower())
    if not pronunciations:
        return None
    pron = pronunciations[0]
    stress = ''.join(['/' if '1' in s else '-' for s in pron if s[-1].isdigit()])
    return stress


def word_matches_pos(word, pos_tag):
    """Simple mapping using WordNet POS"""
    wn_pos_map = {'N': wordnet.NOUN, 'V': wordnet.VERB, 'J': wordnet.ADJ, 'R': wordnet.ADV, 'D': None}
    wn_pos = wn_pos_map.get(pos_tag)
    if wn_pos is None:
        return True  # Determiners and unknown POS accepted
    return bool(wordnet.synsets(word, pos=wn_pos))


def find_words_by_stress_and_pos(pattern, pos_tag):
    matches = []
    for word in cmu.keys():
        s = get_stress(word)
        if s == pattern and word_matches_pos(word, pos_tag):
            matches.append(word)
    return matches


def pick_three_options(candidates):
    if not candidates:
        return ["[no match]"] * 3
    random.shuffle(candidates)
    weights = [max(word_frequency(w, 'en'), 0.0001) for w in candidates]
    if len(candidates) >= 3:
        sample = random.choices(candidates, weights=weights, k=5)
        unique_words = []
        for w in sample:
            if w not in unique_words:
                unique_words.append(w)
            if len(unique_words) == 3:
                break
        while len(unique_words) < 3:
            unique_words.append(random.choices(candidates, weights=weights)[0])
        return unique_words
    else:
        return random.choices(candidates, weights=weights, k=3)


def build_line_interactive_with_pos(pattern, template, max_word_syllables=3):
    i = 0
    line = []
    pos_idx = 0
    while i < len(pattern):
        remaining = pattern[i:]
        pos_tag = template[pos_idx % len(template)]  # loop template
        for size in range(min(max_word_syllables, len(remaining)), 0, -1):
            chunk = remaining[:size]
            candidates = find_words_by_stress_and_pos(chunk, pos_tag)
            if candidates:
                options = pick_three_options(candidates)
                print(f"\nChunk '{chunk}' (POS {pos_tag}, covers {size} syllable(s)) options:")
                print(f"1: {options[0]}  2: {options[1]}  3: {options[2]}")
                while True:
                    choice = input("Choose 1, 2, or 3: ").strip()
                    if choice in ['1', '2', '3']:
                        word = options[int(choice) - 1]
                        line.append(word)
                        i += size
                        pos_idx += 1
                        break
                    else:
                        print("Invalid choice. Enter 1, 2, or 3.")
                break
        else:
            # fallback if no match
            line.append("[?]")
            i += 1
            pos_idx += 1
    return ' '.join(line)


if __name__ == "__main__":
    pattern_input = input("Enter stress pattern (/-/-/ style): ").replace(' ', '')
    print("\nChoose a grammatical template:")
    print("1: Determiner + Adjective + Noun + Verb (D J N V)")
    print("2: Noun + Verb + Adverb (N V R)")
    choice = input("Template 1 or 2? ").strip()
    template = ['D', 'J', 'N', 'V'] if choice == '1' else ['N', 'V', 'R']

    print("\nLet's build your grammatically-aware line!")
    final_line = build_line_interactive_with_pos(pattern_input, template)
    print(f"\nYour generated line: {final_line}")
