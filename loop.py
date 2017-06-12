import pprint
from time import sleep
import mido
from mingus.containers import Note


class Loop:
    def __init__(self, roll, scale, instrument, name):
        self.roll = roll
        self.scale = scale
        self.instrument = instrument
        self.name = name

    def play(self, t):
        tt = t % len(self.roll)
        for i in range(0,len(self.roll[tt])):
            if self.roll[tt][i]:
                if not self.roll[tt-1][i]:
                    # previous is 0, current is 1
                    self.instrument.send(mido.Message('note_on',
                                                      note=self.scale[i],
                                                      velocity=64))
            else:
                if self.roll[tt-1][i]:
                    # previous is 1, current is 0
                    self.instrument.send(mido.Message('note_off',
                                                      note=self.scale[i]))

    def mute(self):
        for i in range(0,len(self.roll[0])):
            self.instrument.send(mido.Message('note_off',
                                              note=self.scale[i]))
        
    def render(self, t):
        tt = t % len(self.roll)        
        print(self.name, self.roll[tt])


class Sequencer:

    def __init__(self, loops=[], bpm=30):
        self.loops = loops
        bpm = bpm
        self.delay = 60.0 / bpm

        # find longest loop
        self.longest = max([len(l.roll) for l in self.loops])

    def play(self):
        for t in range(self.longest):
            for l in self.loops:
                l.play(t)
                l.render(t)
            # as time goes by
            sleep(self.delay)

        for l in self.loops:
            l.mute()



def scale2ints(minguscale, key='C', span=2, octave=3):
    scale = minguscale(key, span)
    notas = []
    for o in range(octave, octave+span):
        for n in range(7):
            notas.append(int(Note(scale.ascending()[n], o)))
    notas.append(int(Note(scale.tonic, octave+span)))
    return notas
