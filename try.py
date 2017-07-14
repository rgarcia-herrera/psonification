import lupe
import mido
import mingus.core.scales as scales
from pony.orm import db_session, commit

#
# timidity -iA -B2,8 -Os
#

print(mido.get_output_names())

muted = mido.open_output(mido.get_output_names()[1])
muted.send(mido.Message('program_change', program=0))

cM = lupe.scale2ints(scales.Major, 'C', span=4, octave=4)
am = lupe.scale2ints(scales.NaturalMinor, 'A', span=3, octave=5)

lupe.db.bind('sqlite', ':memory:', create_db=True)
lupe.db.generate_mapping(create_tables=True)

with db_session:
    l = lupe.Loop(roll=[[0,  114,  0, 0],
                        [0,   55,  0, 0],
                        [99,  66,  0, 0], ],
                  mask=[[0, 1, 0, 0],
                        [0, 1, 0, 0],
                        [0, 1, 0, 0], ],
                  scale=am)
    commit()

    l.instrument = muted

    s = lupe.Sequencer(loops=[l, ],
                       bpm=222)

    while True:
        s.play()
