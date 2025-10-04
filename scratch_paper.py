def get_roman_numeral(chord_root, chord_quality, key_root, key_type="major"):
    """
    Converts a chord's root and quality to its Roman numeral representation within a specified key.
    """
    chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    # Determine the scale of the specified key
    if key_type == "major":
        key_scale_intervals = [0, 2, 4, 5, 7, 9, 11]  # Major scale intervals
    elif key_type == "minor":
        key_scale_intervals = [0, 2, 3, 5, 7, 8,
                               10]  # Natural minor scale intervals (can be adjusted for harmonic/melodic)
    else:
        raise ValueError("Unsupported key type. Use 'major' or 'minor'.")

    key_root_index = chromatic_scale.index(key_root.upper())
    key_scale = [chromatic_scale[(key_root_index + interval) % 12] for interval in key_scale_intervals]

    # Find the degree of the chord root within the key scale
    try:
        degree = key_scale.index(chord_root.upper()) + 1
    except ValueError:
        return f"Chromatic chord: {chord_root}{chord_quality}"  # Handle non-diatonic chords

    # Determine the Roman numeral based on degree and quality
    roman_numerals = ["I", "II", "III", "IV", "V", "VI", "VII"]

    # Adjust for major/minor/diminished quality
    if chord_quality == "major":
        return roman_numerals[degree - 1]
    elif chord_quality == "minor":
        return roman_numerals[degree - 1].lower()
    elif chord_quality == "diminished":
        return roman_numerals[degree - 1].lower() + "°"
    else:
        return f"{chord_root}{chord_quality} (Unknown quality)"


def chords_to_roman_numerals(chord_list, key_root, key_type="major"):
    """
    Converts a list of chords to a list of Roman numeral representations.
    Chords are expected in a format like "C major", "G minor", "B diminished".
    """
    roman_numerals_list = []
    for chord_str in chord_list:
        parts = chord_str.split(" ")
        chord_root = parts[0]
        chord_quality = " ".join(parts[1:])  # Handle multi-word qualities like "major 7"
        roman_numerals_list.append(get_roman_numeral(chord_root, chord_quality, key_root, key_type))
    return roman_numerals_list


# Example usage
chords = ["C major", "G major", "A minor", "F major", "B diminished"]
key = "C"
key_type = "major"

roman_numerals = chords_to_roman_numerals(chords, key, key_type)
print(f"Chords in {key} {key_type}: {roman_numerals}")

chords_minor_key = ["Am minor", "Dm minor", "E major", "G major"]
key_minor = "A"
key_type_minor = "minor"

roman_numerals_minor = chords_to_roman_numerals(chords_minor_key, key_minor, key_type_minor)
print(f"Chords in {key_minor} {key_type_minor}: {roman_numerals_minor}")