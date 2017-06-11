import pprint
from time import sleep
import mido
import random

#
# timidity -iA -B2,8 -Os
# 
#mido.set_backend('mido.backends.portmidi')

output = mido.open_output(mido.get_output_names()[1])

#woodblock
output.send(mido.Message('program_change', program=1))

#output.send(mido.Message('program_change', program=80))


class Loop:
    loop = [
        [1, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 0, 0, 0],
        [1, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 0, 1, 1, 0, 1, 0],
        [1, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 1],
    ]

    # C3 = 48
    notas = range(100,109)

    def play(self, t):
        for i in range(0,len(self.loop[t])):
            if self.loop[t][i]:
                if not self.loop[t-1][i]:
                    output.send(mido.Message('note_on',
                                             note=self.notas[i],
                                             velocity=64))
            else:
                if self.loop[t-1][i]:
                    output.send(mido.Message('note_off',
                                             note=self.notas[i]))

    def render(self, t):
        print( self.loop[t])

    

bpm = 111
delay = 60.0 / bpm
l0 = Loop()
l1 = Loop()
l1.loop =  [
        [1, 0, 1, 0, 1, 0, 0, 1],
        [1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 0],
        [1, 0, 1, 1, 1, 0, 1, 0],
        [1, 1, 1, 0, 0, 0, 1, 0],
        [1, 0, 1, 0, 1, 1, 1, 1],
    ]
l1.notas = range(60,80)
t = 0
while True:
    l1.play(t)
    l0.play(t)
    l1.render(t)
    l0.render(t)
    # as time goes by
    t+=1
    if t == len(l0.loop):
        t = 0
    sleep(delay)
