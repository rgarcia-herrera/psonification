from loop import Loop, Sequencer, scale2ints
import mido
import random
import mingus.core.scales as scales

#
# timidity -iA -B2,8 -Os
#
#mido.set_backend('mido.backends.portmidi')

print(mido.get_output_names())

pianito = mido.open_output(mido.get_output_names()[1])
pianito.send(mido.Message('program_change', program=48))

sepa = mido.open_output(mido.get_output_names()[2])
sepa.send(mido.Message('program_change', program=45))

cM = scale2ints(scales.Major, 'C', span=4, octave=2)
am = scale2ints(scales.NaturalMinor, 'A', span=4, octave=3)

l0 = Loop(roll=[[1, 0, 0, 0, 0, 0, 0, 1],
                [0, 1, 0, 0, 0, 1, 0, 0],
                [0, 0, 1, 0, 1, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0]],
          scale=am,
          instrument=sepa,
          name='sepa')

l1 = Loop(roll=[[1, 0, 0, 0],
                [1, 1, 1, 1],
                [1, 0, 0, 1],
                [1, 0, 1, 0],
                [0, 0, 1, 1],
                [1, 1, 0, 1],
                [1, 0, 1, 0]],
          scale=cM,
          instrument=pianito,
          name='pian')


s = Sequencer(loops = [l0, l1],
              bpm=120)


while True:
    if random.choice([True, False, False]):
        l1.roll = [[random.choice([1,0,0]) for n in range(4)] for m in range(random.randint(2,6))]
        l0.roll = [[random.choice([1,0,0]) for n in range(8)] for m in range(random.randint(3,7))]
    if random.choice([True, False]):
        scale1 = scale2ints(scales.NaturalMinor, random.choice(['A','D','E']), span=3, octave=random.randint(2,4))
        scale2 = scale2ints(scales.NaturalMinor, random.choice(['D','E','B']), span=3, octave=random.randint(2,5))
        l1.scale = scale1
        l0.scale = scale2
    else:
        l1.scale = [n+2 for n in l0.scale]
        l0.scale = [n+2 for n in l0.scale]
        
    s.play()    
