from loop import Loop, Sequencer, scale2ints
import mido
import random
import mingus.core.scales as scales

#
# timidity -iA -B2,8 -Os
#
#mido.set_backend('mido.backends.portmidi')

print(mido.get_output_names())

muted = mido.open_output(mido.get_output_names()[1])
muted.send(mido.Message('program_change', program=45))

glocken = mido.open_output(mido.get_output_names()[2])
glocken.send(mido.Message('program_change', program=47))

cM = scale2ints(scales.Major, 'C', span=4, octave=2)
am = scale2ints(scales.NaturalMinor, 'A', span=4, octave=3)

l0 = Loop(roll=[[1, 0, 0, 0, 0, 0, 0, 1]],
          mask=[[1, 0, 0, 0, 0, 0, 0, 1]],
          scale=[1,2],
          instrument=glocken,
          name='glocken')

l1 = Loop(roll=[[1, 0, 0, 0],
                [1, 0, 1, 0]],
          mask=[[1, 0, 0, 0],
                [1, 0, 1, 0]],
          scale=[33,44,55],
          instrument=muted,
          name='muted')

s = Sequencer(loops = [l0, l1, ],
              bpm=322)

while True:
    if random.choice([True, False, False]):
        l0.roll = [[random.choice([1,1,0]) for n in range(3)] for m in range(random.randint(3,6))]
        l0.mask = l0.roll
        l1.roll = [[random.choice([1,0,0]) for n in range(7)] for m in range(random.randint(5,7))]
        l1.mask = l1.roll
    if random.choice([True, False]):

        l0.scale = scale2ints(random.choice([scales.Phrygian,
                                             scales.NaturalMinor]),
                              random.choice(['A', 'D', 'E']),
                              span=5,
                              octave=random.randint(3,6))

        l1.scale = scale2ints(random.choice([scales.Ionian,
                                             scales.Dorian,
                                             scales.Phrygian,
                                             scales.Major]),
                              random.choice(['E','A','B', 'Bb']),
                              span=5,
                              octave=random.randint(3,6))
    else:
        delta=random.choice([-2, 2])
        delta1=random.choice([-2, 2])        
        l1.scale = [n+delta for n in l0.scale]
        l0.scale = [n+delta1+delta for n in l0.scale]
        
    s.play()    
