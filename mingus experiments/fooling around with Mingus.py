import mingus.core.notes as notes
from mingus.containers import Note

print(notes.is_valid_note("Cb"))
my_note = Note("A", 4)  # A in the 4th octave
print(my_note)

from mingus.core import chords
c_major_triad = chords.from_shorthand("Cb")
print(c_major_triad)

from mingus.core import scales
# Semitones for major scale: W-W-H-W-W-W-H
major_semitones = [2, 2, 1, 2, 2, 2, 1]
c_major_scale = scales.Diatonic("C", major_semitones)
print(c_major_scale.ascending())

from mingus.core import scales
db_ionian = scales.Aeolian("C")
print(db_ionian.ascending())