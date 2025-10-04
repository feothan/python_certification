from collections import defaultdict, Counter
import csv
import re

# ---------- configuration / data ----------
CHROMATIC_SHARP = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
ENHARMONIC = {"Db":"C#", "Eb":"D#", "Gb":"F#", "Ab":"G#", "Bb":"A#"}
SHARP_TO_FLAT = {"C#":"Db","D#":"Eb","F#":"Gb","G#":"Ab","A#":"Bb"}
FLAT_TO_SHARP  = {v:k for k,v in SHARP_TO_FLAT.items()}
FLAT_TO_SHARP.update({"Cb":"B","E#":"F"})

CHORD_INTERVALS = {
    "maj": [0,4,7],
    "":    [0,4,7],
    "m":   [0,3,7],
    "min": [0,3,7],
    "dim": [0,3,6],
    "aug": [0,4,8],
    "7":   [0,4,7,10],
    "maj7":[0,4,7,11],
    "M7":  [0,4,7,11],
    "m7":  [0,3,7,10],
    "min7":[0,3,7,10],
    "mMaj7":[0,3,7,11],
    "dim7":[0,3,6,9],
    "m7b5":[0,3,6,10],
    "6":   [0,4,7,9],
    "m6":  [0,3,7,9],
    "9":   [0,4,7,10,14],
    "maj9":[0,4,7,11,14],
    "add9":[0,4,7,14],
    "m9":  [0,3,7,10,14],
    "11":  [0,4,7,10,14,17],
    "13":  [0,4,7,10,14,21],
    "sus2":[0,2,7],
    "sus4":[0,5,7],
    "sus": [0,5,7],
    "7sus4":[0,5,7,10],
}

_ROOT_RE = re.compile(r'^([A-Ga-g])([#b]?)(.*)$')

# ---------- helper utilities ----------
def get_notes_from_chord(chord_name: str):
    if not chord_name or not chord_name.strip():
        return []
    s = chord_name.strip()

    if '/' in s:
        main_part, bass_part = s.split('/', 1)
        bass_part = bass_part.strip()
    else:
        main_part, bass_part = s, None

    m = _ROOT_RE.match(main_part.strip())
    if not m:
        return []
    root_letter = m.group(1).upper()
    accidental = m.group(2) or ""
    suffix = (m.group(3) or "").strip()

    root_token = root_letter + accidental
    root_for_index = FLAT_TO_SHARP.get(root_token, root_token)
    if root_for_index not in CHROMATIC_SHARP:
        return []

    sfx = suffix.replace("MAJ", "maj").replace("M7", "maj7")
    sfx = sfx.replace("MIN", "m").replace("MIN7", "m7")
    sfx = sfx.replace("M", "maj") if sfx == "M" else sfx

    chosen = None
    for cand in [sfx, sfx.lower(), sfx.replace("min","m"), sfx.replace("m","min")]:
        if cand in CHORD_INTERVALS:
            chosen = cand
            break
    if chosen is None and (sfx == "" or sfx is None):
        chosen = ""
    if chosen is None:
        return []

    root_idx = CHROMATIC_SHARP.index(root_for_index)
    intervals = CHORD_INTERVALS[chosen]
    out_pitches = []
    for i in intervals:
        out_pitches.append(CHROMATIC_SHARP[(root_idx + i) % 12])

    if bass_part:
        mb = _ROOT_RE.match(bass_part)
        if mb:
            bass_root = mb.group(1).upper() + (mb.group(2) or "")
            bass_sharp = FLAT_TO_SHARP.get(bass_root, bass_root)
            if bass_sharp in CHROMATIC_SHARP:
                out_pitches.append(bass_sharp)
            else:
                out_pitches.append(bass_part)
        else:
            out_pitches.append(bass_part)

    return out_pitches

def _transpose_root_token(root_token, semitones):
    root = ENHARMONIC.get(root_token[0].upper() + (root_token[1] if len(root_token) > 1 else ""), root_token)
    if root not in CHROMATIC_SHARP:
        raise ValueError(f"Unknown root: {root_token}")
    idx = CHROMATIC_SHARP.index(root)
    return CHROMATIC_SHARP[(idx + semitones) % 12]

def transpose_chords(tokens, semitones):
    out = []
    for tok in tokens:
        if tok == '|' or tok.strip() == '':
            out.append(tok)
            continue
        if '/' in tok:
            main, bass = tok.split('/', 1)
        else:
            main, bass = tok, None

        m = _ROOT_RE.match(main)
        if not m:
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
            mb = _ROOT_RE.match(bass)
            if mb:
                bass_root_token = mb.group(1) + (mb.group(2) or "")
                try:
                    new_bass = _transpose_root_token(bass_root_token, semitones)
                    bass_suffix = mb.group(3) or ""
                    new_bass = new_bass + bass_suffix
                except ValueError:
                    new_bass = bass
            else:
                new_bass = bass
            out.append(f"{new_main}/{new_bass}")
        else:
            out.append(new_main)

    return out

# ---------- Song object ----------
class Song:
    def __init__(self, year, title, artist, verse_chords, chorus_chords, bridge_chords, key_signature):
        self.year = int(year)
        self.title = title
        self.artist = artist
        self.verse_chords = verse_chords.split()
        self.chorus_chords = chorus_chords.split()
        self.bridge_chords = bridge_chords.split()
        self.key_signature = key_signature

    def __str__(self):
        return f"{self.year} {self.title} by {self.artist}, in {self.key_signature}"

    def transpose(self, increment):
        self.verse_chords = transpose_chords(self.verse_chords, increment)
        self.chorus_chords = transpose_chords(self.chorus_chords, increment)
        self.bridge_chords = transpose_chords(self.bridge_chords, increment)

    def to_roman(self, cap_accidentals: int = 2):
        """
        Convert chords in verse/chorus/bridge to Roman numerals relative to self.key_signature.
        Keeps diatonic base case as authoritative; flips case only when chord-quality detection
        confidently contradicts it. Appends seventh markers without duplication.
        Returns: {'verse': [...], 'chorus': [...], 'bridge': [...]}
        """

        # small helpers used only inside this method
        def norm(n):
            return FLAT_TO_SHARP.get(n, n)

        def pc_index(n):
            if not n:
                return None
            nn = norm(n).upper()
            return CHROMATIC_SHARP.index(nn) if nn in CHROMATIC_SHARP else None

        def detect_quality_and_seventh(main_chord):
            """Return (tri_quality, seventh_marker) where tri_quality in {'maj','min','dim','aug', None}."""
            notes = get_notes_from_chord(main_chord)
            if not notes:
                return None, ''
            root = notes[0]
            root_idx = pc_index(root)
            if root_idx is None:
                return None, ''
            pcs = []
            for n in notes:
                idx = pc_index(n)
                if idx is not None:
                    pcs.append((idx - root_idx) % 12)
            s = set(pcs)

            # triad detection
            if {4, 7}.issubset(s):
                tri = 'maj'
            elif {3, 7}.issubset(s):
                tri = 'min'
            elif {3, 6}.issubset(s):
                tri = 'dim'
            elif {4, 8}.issubset(s):
                tri = 'aug'
            else:
                tri = None

            # sevenths (best-effort)
            if {3, 6, 10}.issubset(s):
                return 'min', 'ø7'  # half-diminished
            if 11 in s:
                seventh = 'maj7'
            elif 10 in s:
                seventh = 'm7' if tri == 'min' else '7'
            else:
                seventh = ''

            return tri, seventh

        # --- parse key_signature from Song ---
        key_sig = getattr(self, "key_signature", None)
        if not key_sig:
            # no key specified: return chords unchanged
            return {
                'verse': list(self.verse_chords),
                'chorus': list(self.chorus_chords),
                'bridge': list(self.bridge_chords)
            }

        # normalize key label and detect minor/major
        ks = key_sig
        is_minor = ks.endswith('m') or ks.endswith('min')
        if ks.endswith('min'):
            key_root_label = ks[:-3]
        elif ks.endswith('m') and len(ks) > 1:
            key_root_label = ks[:-1]
        else:
            key_root_label = ks
        key_root_label = norm(key_root_label).upper()
        if key_root_label not in CHROMATIC_SHARP:
            return {
                'verse': list(self.verse_chords),
                'chorus': list(self.chorus_chords),
                'bridge': list(self.bridge_chords)
            }
        key_root_pc = CHROMATIC_SHARP.index(key_root_label)

        # diatonic intervals & base numerals (base_numerals is authoritative)
        if is_minor:
            scale_intervals = [0, 2, 3, 5, 7, 8, 10]  # natural minor
            base_numerals = ["i", "ii°", "III", "iv", "v", "VI", "VII"]
        else:
            scale_intervals = [0, 2, 4, 5, 7, 9, 11]  # major
            base_numerals = ["I", "ii", "iii", "IV", "V", "vi", "vii°"]

        degree_pcs = [(key_root_pc + i) % 12 for i in scale_intervals]

        # Compose numeral using the diatonic base as source-of-truth, flip case only if tri_quality confidently contradicts
        def compose_numeral_fixed(deg_idx, tri_quality, seventh_marker, alteration):
            base = base_numerals[deg_idx]

            # Flip case only when tri_quality clearly contradicts the diatonic base:
            if tri_quality == 'maj' and base.islower():
                base = base.upper()
            elif tri_quality == 'min' and base.isupper():
                base = base.lower()

            # dim / aug handling
            if tri_quality == 'dim':
                if not base.endswith('°'):
                    base = base.rstrip('°') + '°'
            if tri_quality == 'aug':
                base = (base.rstrip('°') if base.endswith('°') else base).upper() + '+'

            # format accidental suffix
            alt = alteration
            if alt > 6:
                alt = 6
            if alt < -6:
                alt = -6
            acc = ''
            if alt > 0:
                acc = '#' * min(alt, cap_accidentals)
            elif alt < 0:
                acc = 'b' * min(-alt, cap_accidentals)

            numeral = f"{base}{acc}"

            # Normalize seventh appending:
            if seventh_marker:
                if seventh_marker == 'ø7':
                    numeral = f"{numeral}ø7"
                elif seventh_marker == 'm7':
                    # if numeral is lowercase (minor), append '7' for readability (ii7 means ii m7)
                    if any(ch.islower() for ch in numeral if ch.isalpha()):
                        numeral = f"{numeral}7"
                    else:
                        numeral = f"{numeral}m7"
                else:
                    numeral = f"{numeral}{seventh_marker}"

            return numeral

        # convert single chord -> roman (no '?' results)
        def chord_to_roman_single(chord_token):
            s = chord_token.strip()
            if not s:
                return ""
            # drop inversion part for degree calc
            main = s.split('/', 1)[0].strip()
            m = _ROOT_RE.match(main)
            if not m:
                return "(?)"
            root_tok = (m.group(1).upper() + (m.group(2) or ""))
            root_norm = norm(root_tok)
            root_pc = pc_index(root_norm)
            if root_pc is None:
                return "(?)"

            tri, seventh = detect_quality_and_seventh(main)

            # pick diatonic degree with minimal signed distance
            best_deg = None
            best_delta = None
            for deg_idx, deg_pc in enumerate(degree_pcs):
                delta = (root_pc - deg_pc) % 12
                if delta > 6:
                    delta -= 12
                if best_deg is None or abs(delta) < abs(best_delta):
                    best_deg = deg_idx
                    best_delta = delta

            return compose_numeral_fixed(best_deg, tri, seventh, best_delta)

        # map across sections
        return {
            'verse': [chord_to_roman_single(ch) for ch in self.verse_chords],
            'chorus': [chord_to_roman_single(ch) for ch in self.chorus_chords],
            'bridge': [chord_to_roman_single(ch) for ch in self.bridge_chords],
        }


# ---------- CSV loading ----------
with open('songs.csv', mode='r', newline='') as file:
    song_list = csv.reader(file)
    song_book = []
    for column in song_list:
        new_song = Song(column[0], column[1], column[2], column[3], column[4], column[5], column[6])
        song_book.append(new_song)

# ---------- Example iteration ----------
for song in song_book:
    print(song)
    print(f"verse {song.verse_chords}, chorus {song.chorus_chords}, bridge {song.bridge_chords}")
    print(song.to_roman())
    print()

# ---------- Helper: parse a roman token produced by Song.to_roman ----------
_ROMAN_RE = re.compile(r'(?P<base>[IViv]+°?\.?|\w+)(?P<acc>[#b]{0,2})(?P<sev>ø7|maj7|m7|7|)?')

# ---------- Roman parse helper (unchanged interface) ----------
_ROMAN_RE = re.compile(r'(?P<base>[IViv]+°?|\w+)(?P<acc>[#b]{0,2})(?P<sev>ø7|maj7|m7|7|)?')

def parse_roman_token(tok: str):
    if not tok:
        return None, 0, ''
    m = _ROMAN_RE.match(tok)
    if not m:
        # fallback: peel off known sevenths and trailing accidentals
        sev = ''
        for s in ('ø7','maj7','m7','7'):
            if tok.endswith(s):
                sev = s
                tok = tok[:-len(s)]
                break
        acc = 0
        while tok.endswith('#'):
            acc += 1
            tok = tok[:-1]
        while tok.endswith('b'):
            acc -= 1
            tok = tok[:-1]
        base = tok
        return base, acc, sev
    base = m.group('base')
    acc = m.group('acc') or ''
    sev = m.group('sev') or ''
    alteration = acc.count('#') - acc.count('b')
    return base, alteration, sev

# ---------- Improved roman -> chord renderer (fixes m7 duplication) ----------
def roman_to_chord(roman_token: str, target_key: str, cap_accidentals: int = 2):
    """
    Convert roman token (e.g. 'ii', 'V7', 'III#', 'ivbmaj7', 'iiø7') into a chord in target_key.
    Returns string like 'C', 'Dm', 'G7', 'F#maj7', 'A#m7b5', etc.
    """
    # normalize target key
    tk = target_key.strip()
    is_minor = tk.endswith('m') or tk.endswith('min')
    if tk.endswith('min'):
        key_root_label = tk[:-3]
    elif tk.endswith('m') and len(tk) > 1:
        key_root_label = tk[:-1]
    else:
        key_root_label = tk
    key_root_label = FLAT_TO_SHARP.get(key_root_label, key_root_label).upper()
    if key_root_label not in CHROMATIC_SHARP:
        raise ValueError(f"Unknown target key: {target_key}")
    key_root_pc = CHROMATIC_SHARP.index(key_root_label)

    # diatonic intervals
    if is_minor:
        scale_intervals = [0,2,3,5,7,8,10]
        base_numerals = ["i","ii°","III","iv","v","VI","VII"]
    else:
        scale_intervals = [0,2,4,5,7,9,11]
        base_numerals = ["I","ii","iii","IV","V","vi","vii°"]
    degree_pcs = [(key_root_pc + i) % 12 for i in scale_intervals]

    base, alteration, seventh = parse_roman_token(roman_token)
    if base is None:
        return f"({roman_token})"

    # map numeral string to index (I->0 .. VII->6)
    roman_map = {"I":0,"II":1,"III":2,"IV":3,"V":4,"VI":5,"VII":6}
    base_letters = re.sub(r'[°+]', '', base).upper()
    deg_idx = roman_map.get(base_letters)
    if deg_idx is None:
        # fallback
        return f"({roman_token})"

    # compute final pitch class
    deg_pc = degree_pcs[deg_idx]
    final_pc = (deg_pc + alteration) % 12
    root_name = CHROMATIC_SHARP[final_pc]

    # determine triad quality preference from base and natural mapping
    # natural base case for this degree in current mode:
    natural_base = base_numerals[deg_idx]
    # decide tri_quality: 'maj' or 'min' or 'dim' or 'aug'
    tri_quality = None
    if '°' in base or '°' in natural_base:
        tri_quality = 'dim'
    else:
        # use case of provided base to guess quality: lowercase => minor, uppercase => major
        if base.islower():
            tri_quality = 'min'
        elif base.isupper():
            tri_quality = 'maj'
        else:
            # fallback to natural base
            tri_quality = 'min' if natural_base.islower() else 'maj'

    # build chord name carefully to avoid duplicates like 'Gmm7'
    chord = root_name
    if tri_quality == 'min':
        chord += 'm'
    elif tri_quality == 'dim':
        chord += 'dim'
    elif tri_quality == 'aug':
        chord += 'aug'
    # append seventh properly:
    if seventh:
        if seventh == 'ø7':
            # half-diminished: represent as m7b5 on the minor triad root
            # ensure root uses 'm' form
            chord = root_name + 'm7b5'
        elif seventh == 'm7':
            # if tri is minor, append '7' to 'm' (e.g. 'Gm7'), else append 'm7'
            if tri_quality == 'min':
                if not chord.endswith('m'):
                    chord += 'm'
                chord += '7'
            else:
                chord += 'm7'
        else:
            # '7' or 'maj7' appended as-is
            chord += seventh

    return chord

# ---------- NEW: corpus-driven, last-token transition model and interactive builder ----------
def build_progression_from_corpus_v2(song_book):
    """
    Revised interactive progression builder.
    - Uses Song.to_roman() outputs from the corpus.
    - For each section (verse/chorus/bridge) builds last-token -> Counter(next-token).
    - Interactively lets user pick: at start, offers most frequent section-starters;
      thereafter offers top-next choices after the *last chosen token* aggregated across corpus.
    - Allows ending a section at any time.
    - Renders final progression into a user-chosen target key.
    """
    # 1) gather per-section roman sequences
    section_seqs = {'verse': [], 'chorus': [], 'bridge': []}
    for song in song_book:
        try:
            romans = song.to_roman()
        except Exception:
            continue
        for sec in ('verse','chorus','bridge'):
            seq = romans.get(sec, [])
            cleaned = [t.strip() for t in seq if t and t.strip()]
            if cleaned:
                section_seqs[sec].append(cleaned)

    # 2) build last-token -> Counter(next) models and start counters
    transition = {sec: defaultdict(Counter) for sec in ('verse','chorus','bridge')}
    starts = {sec: Counter() for sec in ('verse','chorus','bridge')}
    for sec in ('verse','chorus','bridge'):
        for seq in section_seqs[sec]:
            if seq:
                starts[sec][seq[0]] += 1
            for i, tok in enumerate(seq):
                if i+1 < len(seq):
                    nxt = seq[i+1]
                    transition[sec][tok][nxt] += 1
                else:
                    # mark termination possibility explicitly (optional)
                    transition[sec][tok]['__END__'] += 0

    # 3) interactive construction
    built = {}
    print("\n--- Interactive progression builder (v2) ---")
    print("Choose numbers (1-5), or 'e' to end the section.\n")
    for sec in ('verse','chorus','bridge'):
        print(f"\nBuilding {sec} progression. Corpus examples: {len(section_seqs[sec])}")
        prog = []
        last = None
        while True:
            if last is None:
                # show top starts
                counter = starts[sec]
                if not counter:
                    print("No start data for this section; ending.")
                    break
                common = counter.most_common(5)
            else:
                counter = transition[sec].get(last, Counter())
                if not counter:
                    # fallback to overall starts if no continuation known
                    counter = starts[sec]
                common = [(k,v) for k,v in counter.most_common(5) if k != '__END__']
                if not common:
                    # nothing to suggest
                    print("No known continuation from that token; you can end or pick a start token.")
                    # offer to pick a start token or end
                    counter = starts[sec]
                    common = counter.most_common(5)
            # display
            print("\nNext options:")
            total = sum(v for k,v in counter.items() if k != '__END__')
            for i,(tok,cnt) in enumerate(common, start=1):
                pct = (cnt/total*100) if total>0 else 0.0
                print(f"  {i}. {tok}   ({cnt} occurrences, {pct:.1f}%)")
            print("  e. end this section")
            choice = input("Choose option (1-5 or e): ").strip().lower()
            if choice in ('e','end'):
                break
            if choice.isdigit():
                idx = int(choice)-1
                if 0 <= idx < len(common):
                    chosen = common[idx][0]
                    prog.append(chosen)
                    last = chosen
                    continue
            print("Invalid choice; try again.")
        built[sec] = prog
        print(f"{sec.capitalize()} progression built: {prog}")

    # 4) render to target key
    print("\nBuilt all sections.")
    target_key = input("Enter target key to render final progression (e.g. C, Am, F#): ").strip()
    try:
        _ = roman_to_chord('I', target_key)
    except Exception as e:
        print(f"Warning: target key '{target_key}' may be invalid ({e}); continuing.")

    rendered = {}
    for sec in ('verse','chorus','bridge'):
        rendered[sec] = [ roman_to_chord(tok, target_key) for tok in built.get(sec, []) ]

    # 5) show results
    print("\nFinal progressions:")
    for sec in ('verse','chorus','bridge'):
        print(f"\n{sec.upper()}:")
        print("  Roman: ", '  '.join(built.get(sec, [])))
        print("  Chords:", '  '.join(rendered.get(sec, [])))
    return built, rendered

built, rendered = build_progression_from_corpus_v2(song_book)