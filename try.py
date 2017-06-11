from loop import Loop, Sequencer
import mido
import random

#
# timidity -iA -B2,8 -Os
# 
#mido.set_backend('mido.backends.portmidi')

print(mido.get_output_names())

pianito = mido.open_output(mido.get_output_names()[1])
pianito.send(mido.Message('program_change', program=69))

sepa = mido.open_output(mido.get_output_names()[2])
sepa.send(mido.Message('program_change', program=115))

pong = mido.open_output(mido.get_output_names()[5])
pong.send(mido.Message('program_change', program=21))


l0 = Loop(roll=[[1, 0, 0, 0, 0, 0, 0, 1],
                [0, 1, 0, 0, 0, 1, 0, 0],
                [0, 0, 1, 0, 1, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0]],
          scale=range(70,79),
          instrument=sepa,
          name='sepa')

l1 = Loop(roll=[[1, 0, 0, 0],
                [1, 1, 1, 1],
                [1, 0, 0, 1],
                [1, 0, 1, 1],
                [0, 0, 1, 1],
                [1, 1, 1, 0],
                [1, 0, 1, 0]],
          scale=[41,52,55,70],
          instrument=pianito,
          name='pian')

l2 = Loop(roll=[[1, 0, 0, 0, 1, 0, 0, 1],
                [0, 1, 0, 0, 1, 1, 0, 0],
                [0, 0, 1, 0, 1, 1, 1, 0],
                [0, 0, 0, 1, 0, 1, 0, 1]],
          scale=range(60,69),
          instrument=pong,
          name='pong')

s = Sequencer()
s.loops = [l2, ]#l0, l1, l2]
s.play()
