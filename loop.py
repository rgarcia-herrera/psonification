import pprint
from time import sleep
import mido

class Loop:
    def __init__(self, roll, scale, instrument, name):
        self.roll = roll
        self.scale = scale
        self.instrument = instrument
        self.name = name

    def play(self, t):
        for i in range(0,len(self.roll[t])):
            if self.roll[t][i]:
                if not self.roll[t-1][i]:
                    # previous is 0, current is 1
                    self.instrument.send(mido.Message('note_on',
                                                      note=self.scale[i],
                                                      velocity=64))
            else:
                if self.roll[t-1][i]:
                    # previous is 1, current is 0
                    self.instrument.send(mido.Message('note_off',
                                                      note=self.scale[i]))

    def render(self, t):
        print(self.name, self.roll[t])


class Sequencer:
    loops = []
    bpm = 111
    delay = 60.0 / bpm

    def play(self):
        t = 0
        while True:
            for l in self.loops:
                l.play(t)
                l.render(t)
            # as time goes by
            t+=1
            if t == len(self.loops[0].roll):
                t = 0
            sleep(self.delay)
