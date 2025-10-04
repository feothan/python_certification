import numpy as np
import csv
import re

# ---------- configuration / data ----------
CHROMATIC_SHARP = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
ENHARMONIC = {"Db":"C#", "Eb":"D#", "Gb":"F#", "Ab":"G#", "Bb":"A#"}
# map sharps -> common flat equivalents
SHARP_TO_FLAT = {"C#":"Db","D#":"Eb","F#":"Gb","G#":"Ab","A#":"Bb"}
FLAT_TO_SHARP = {"Db":"C#","Eb":"D#","Gb":"F#","Ab":"G#","Bb":"A#","Cb":"B","E#":"F"}
# include some uncommon mappings

# Krumhansl-Schmuckler key profiles (major / minor)
KS_MAJOR = np.array([6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88])
KS_MINOR = np.array([6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17])
KS_KEYS = {}  # dictionary of key name -> profile vector

# Generate profiles for all 12 major and minor keys
CHROMATIC = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
for i, root in enumerate(CHROMATIC):
    KS_KEYS[root] = np.roll(KS_MAJOR, i)
    KS_KEYS[root + "m"] = np.roll(KS_MINOR, i)



key_signature_data = """
C:   C D E F G A B
G:   G A B C D E F#
D:   D E F# G A B C#
A:   A B C# D E F# G#
E:   E F# G# A B C# D#
B:   B C# D# E F# G# A#
F:  F# G# A# B C# D# E#
C:  C# D# E# F# G# A# B#

F:   F G A Bb C D E
Bb:  Bb C D Eb F G A
Eb:  Eb F G Ab Bb C D
Ab:  Ab Bb C Db Eb F G
Db:  Db Eb F Gb Ab Bb C
Gb:  Gb Ab Bb Cb Db Eb F
Cb:  Cb Db Eb Fb Gb Ab Bb

Am:   A B C D E F G
Em:   E F# G A B C D
Bm:   B C# D E F# G A
F#m:  F# G# A B C# D E
C#m:  C# D# E F# G# A B
G#m:  G# A# B C# D# E F#
D#m:  D# E# F# G# A# B C#
A#m:  A# B# C# D# E# F# G#

Dm:   D E F G A Bb C
Gm:   G A Bb C D Eb F
Cm:   C D Eb F G Ab Bb
Fm:   F G Ab Bb C Db Eb
Bbm:  Bb C Db Eb F Gb Ab
Ebm:  Eb F Gb Ab Bb Cb Db
Abm:  Ab Bb Cb Db Eb Fb Gb
"""

# Interval patterns (semitones from root)
CHORD_INTERVALS = {
    # triads
    "maj": [0,4,7],
    "":    [0,4,7],     # bare "C" -> major by default
    "m":   [0,3,7],
    "min": [0,3,7],
    "dim": [0,3,6],
    "aug": [0,4,8],
    # sevenths
    "7":   [0,4,7,10],
    "maj7":[0,4,7,11],
    "M7":  [0,4,7,11],
    "m7":  [0,3,7,10],
    "min7":[0,3,7,10],
    "mMaj7":[0,3,7,11],
    "dim7":[0,3,6,9],
    "m7b5":[0,3,6,10],  # half-diminished
    # sixths
    "6":   [0,4,7,9],
    "m6":  [0,3,7,9],
    # ninths / add
    "9":   [0,4,7,10,14],
    "maj9":[0,4,7,11,14],
    "add9":[0,4,7,14],
    "m9":  [0,3,7,10,14],
    # elevenths / thirteenths (simple approximations)
    "11":  [0,4,7,10,14,17],
    "13":  [0,4,7,10,14,21],
    # suspended
    "sus2":[0,2,7],
    "sus4":[0,5,7],
    "sus": [0,5,7],
    # extensions commonly combined with 7
    "7sus4":[0,5,7,10],
    # add more as you need...
}

# regex: root letter, optional accidental, remainder; optionally slash bass
_ROOT_RE = re.compile(r'^([A-Ga-g])([#b]?)(.*)$')

# ---------- helper utilities ----------
def _normalize_root_token(token: str) -> str:
    """Return canonical token (upper root letter + accidental if any)."""
    token = token.strip()
    if not token:
        return token
    letter = token[0].upper()
    acc = token[1] if len(token) > 1 else ""
    return letter + acc

def _prefer_flats_from_input(root_token: str, bass_token: str|None) -> bool:
    """If root or bass used a flat, prefer flats; if used a '#', prefer sharps; else default to sharps."""
    for t in (root_token, bass_token):
        if not t:
            continue
        if 'b' in t:
            return True
        if '#' in t:
            return False
    return False  # default: prefer sharps (False)

def _sharp_or_flat(sp_name: str, prefer_flats: bool) -> str:
    """Given a sharp-based name like 'C#', return either 'C#' or 'Db' depending on preference."""
    sp_name = sp_name.upper()
    if prefer_flats and sp_name in SHARP_TO_FLAT:
        return SHARP_TO_FLAT[sp_name]
    return sp_name

# ---------- main function ----------
def get_notes_from_chord(chord_name: str):
    """
    Parse a chord symbol and return a list of pitch names (strings).
    - Includes explicit slash bass as the last element of the returned list.
    - Attempts to prefer flats in output if input used flats; otherwise prefers sharps.
    - Returns [] on invalid/unsupported input.
    """
    if not chord_name or not chord_name.strip():
        return []
    s = chord_name.strip()

    # split off slash-bass if present (keep it for output)
    if '/' in s:
        main_part, bass_part = s.split('/', 1)
        bass_part = bass_part.strip()
    else:
        main_part, bass_part = s, None

    # parse root + suffix from main_part
    m = _ROOT_RE.match(main_part.strip())
    if not m:
        return []
    root_letter = m.group(1).upper()
    accidental = m.group(2) or ""
    suffix = (m.group(3) or "").strip()  # e.g. "m7", "maj7", "sus4", "add9"

    root_token = root_letter + accidental
    root_norm = _normalize_root_token(root_token)
    # canonicalize flats to sharps for indexing
    root_for_index = FLAT_TO_SHARP.get(root_norm, root_norm)
    if root_for_index not in CHROMATIC_SHARP:
        return []

    # determine preference for output spelling
    prefer_flats = _prefer_flats_from_input(root_token, bass_part)

    # normalize suffix tokens (common aliases)
    sfx = suffix
    sfx = sfx.replace("MAJ", "maj").replace("M7", "maj7")  # case-insensitive helpers
    sfx = sfx.replace("MIN", "m")
    sfx = sfx.replace("MIN7", "m7")
    sfx = sfx.replace("M", "maj") if sfx == "M" else sfx  # rare
    # make lower for consistent matching, but keep keys in CHORD_INTERVALS
    sfx_key_candidates = [sfx, sfx.lower(), sfx.replace("min","m"), sfx.replace("m","min")]

    # find the best matching chord interval pattern
    chosen = None
    for cand in sfx_key_candidates:
        if cand in CHORD_INTERVALS:
            chosen = cand
            break
    # also allow uppercase keys in table (like "M7" if present)
    if chosen is None:
        for cand in sfx_key_candidates:
            if cand.upper() in CHORD_INTERVALS:
                chosen = cand.upper()
                break

    # if the suffix is empty, treat as major triad
    if chosen is None and (sfx == "" or sfx is None):
        chosen = ""  # maps to CHORD_INTERVALS[""] => major triad

    if chosen is None:
        # unsupported chord type for now
        return []

    # compute notes from intervals
    root_idx = CHROMATIC_SHARP.index(root_for_index)
    intervals = CHORD_INTERVALS[chosen]
    out_pitches = []
    for i in intervals:
        nm = CHROMATIC_SHARP[(root_idx + i) % 12]
        out_pitches.append(_sharp_or_flat(nm, prefer_flats))

    # include explicit bass (transformed to preferred spelling)
    if bass_part:
        mb = _ROOT_RE.match(bass_part)
        if mb:
            bass_root = mb.group(1).upper() + (mb.group(2) or "")
            # canonicalize bass to sharp for lookup, then convert back
            bass_sharp = FLAT_TO_SHARP.get(bass_root, bass_root)
            if bass_sharp in CHROMATIC_SHARP:
                bass_out = _sharp_or_flat(bass_sharp, prefer_flats)
                out_pitches.append(bass_out)
            else:
                # if bass couldn't be parsed, append raw text
                out_pitches.append(bass_part)
        else:
            out_pitches.append(bass_part)

    return out_pitches

_root_re = re.compile(r'^([A-Ga-g])([#b]?)(.*)$')  # root letter, optional accidental, rest

def _normalize_root(r):
    r = r[0].upper() + (r[1] if len(r) > 1 else "")
    return ENHARMONIC.get(r, r)

def _transpose_root_token(root_token, semitones):
    """root_token like 'C' or 'Bb' -> transposed root in sharps (C#, etc.)"""
    root = _normalize_root(root_token)
    if root not in CHROMATIC_SHARP:
        raise ValueError(f"Unknown root: {root_token}")
    idx = CHROMATIC_SHARP.index(root)
    return CHROMATIC_SHARP[(idx + semitones) % 12]

def transpose_chords(tokens, semitones):
    out = []
    for tok in tokens:
        # leave purely structural markers (like '|') alone
        if tok == '|' or tok.strip() == '':
            out.append(tok)
            continue

        # If token contains a '/', treat left of '/' as main chord, right as explicit bass
        if '/' in tok:
            main, bass = tok.split('/', 1)
        else:
            main, bass = tok, None

        # extract root from main using regex
        m = _root_re.match(main)
        if not m:
            # unknown token — leave as-is
            out.append(tok)
            continue

        root_token = m.group(1) + (m.group(2) or "")
        suffix = m.group(3) or ""

        try:
            new_root = _transpose_root_token(root_token, semitones)
        except ValueError:
            out.append(tok)
            continue

        new_main = new_root + suffix

        if bass:
            # parse and transpose bass similarly (accept e.g. 'G#', 'Bb', etc.)
            mb = _root_re.match(bass)
            if mb:
                bass_root_token = mb.group(1) + (mb.group(2) or "")
                try:
                    new_bass = _transpose_root_token(bass_root_token, semitones)
                    # if bass had an extra suffix (unlikely), keep it
                    bass_suffix = mb.group(3) or ""
                    new_bass = new_bass + bass_suffix
                except ValueError:
                    # leave original bass if we can't parse it
                    new_bass = bass
            else:
                new_bass = bass
            out.append(f"{new_main}/{new_bass}")
        else:
            out.append(new_main)

    return out

def chord_to_pitch_classes(chord):
    """Return pitch classes (0=C ... 11=B) for a chord name."""
    notes = get_notes_from_chord(chord)
    pcs = []
    for n in notes:
        if n in CHROMATIC:
            pcs.append(CHROMATIC.index(n))
        elif n in FLAT_TO_SHARP and FLAT_TO_SHARP[n] in CHROMATIC:
            pcs.append(CHROMATIC.index(FLAT_TO_SHARP[n]))
    return pcs

def section_profile(chords):
    """Build pitch-class histogram for a list of chords."""
    pc_counts = np.zeros(12)
    for chord in chords:
        pcs = chord_to_pitch_classes(chord)
        for pc in pcs:
            pc_counts[pc] += 1
    # normalize to proportions
    if pc_counts.sum() > 0:
        pc_counts /= pc_counts.sum()
    return pc_counts

def krumhansl_schmuckler_correlation(profile, key_profile):
    """Compute correlation between a section's profile and a key profile."""
    return np.corrcoef(profile, key_profile)[0,1]

def section_starts_with_root(section, key):
    """Returns 1 if the first chord of section matches the key root, else 0."""
    if not section:
        return 0
    key_root = key[0].upper()
    first_chord_root = _ROOT_RE.match(section[0])
    if not first_chord_root:
        return 0
    chord_root = first_chord_root.group(1).upper() + (first_chord_root.group(2) or "")
    # consider major/minor equivalence
    if chord_root == key_root:
        return 1
    return 0


class Song: #create the song object
    def __init__(self, year, title, artist, verse_chords, chorus_chords, bridge_chords):
        self.year = int(year)
        self.title = title
        self.artist = artist
        self.verse_chords = verse_chords.split()
        self.chorus_chords = chorus_chords.split()
        self.bridge_chords = bridge_chords.split()

    def __str__(self):
        song = f"{self.year} {self.title} by {self.artist}"
        return song

    def transpose(self, increment):
        self.verse_chords = transpose_chords(self.verse_chords, increment)
        self.chorus_chords = transpose_chords(self.chorus_chords, increment)
        self.bridge_chords = transpose_chords(self.bridge_chords, increment)

    def key_signature(self):
        all_sections = [self.verse_chords, self.chorus_chords, self.bridge_chords]
        cumulative_scores = {key: 0.0 for key in KS_KEYS}

        for section in all_sections:
            if not section:
                continue
            profile = section_profile(section)
            for key in KS_KEYS:
                corr = krumhansl_schmuckler_correlation(profile, KS_KEYS[key])
                weight = 1 + 0.5 * section_starts_with_root(section, key)  # boost if section starts on root
                cumulative_scores[key] += corr * weight

        # return the best guess key
        best_key = max(cumulative_scores, key=cumulative_scores.get)
        return best_key


with open('songs.csv', mode='r', newline='') as file: #load data from songs.csv spreadsheet
    song_list = csv.reader(file)
    song_book = []  #load the song book with song objects
    for entry in song_list:
        new_song = Song(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5])
        song_book.append(new_song)

# for song in song_book:
#     print(f"{song.title} was a hit of {song.year}, by {song.artist}!")
#     print(f"The first chord in the {len(song.verse_chords)}-change verse is {song.verse_chords[0]}.")
#     print(f"The first chord in the {len(song.chorus_chords)}-change chorus is {song.chorus_chords[0]}.")
#     print(f"The first chord in the {len(song.bridge_chords)}-change bridge is {song.bridge_chords[0]}.")
#     print()

for song in song_book:
    print(song)
    print (f"best guess at key: {song.key_signature()}")
    print()

    # song.transpose(2)
    # print(f"v {song.verse_chords} c {song.chorus_chords} b {song.bridge_chords}")
