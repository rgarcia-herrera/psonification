from time import sleep
import mido
from mingus.containers import Note


class Loop:
    def __init__(self, roll, mask, scale, instrument=None):
        self.roll = roll
        self.mask = mask
        self.scale = scale
        self.instrument = instrument
        self.current = [False for i in range(0, len(self.roll[0]))]

    def on(self, i, velocity=64):
        self.instrument.send(
            mido.Message('note_on',
                         note=self.scale[i],
                         velocity=velocity))
        self.current[i] = True

    def off(self, i):
        self.instrument.send(mido.Message('note_off',
                                          note=self.scale[i]))
        self.current[i] = False

    def play(self, t):
        t = t % len(self.roll)
        for i in range(0, len(self.roll[t])):
            now = self.roll[t][i]

            if not self.current[i] and now > 0:  # from silence to on
                self.on(i, velocity=now)
            elif self.current[i] and now == 0:   # from playing to off
                self.off(i)
            elif self.current[i] and now > 0:    # playing, maybe staccato
                if self.mask[t][i] == 1:  # interrupt sound if mask is 1
                    self.off(i)
                    self.on(i, velocity=now)
                else:
                    pass  # if mask == 0 keep note_on from previous t

    def mute(self):
        for i in range(0, len(self.roll[0])):
            self.instrument.send(mido.Message('note_off',
                                              note=self.scale[i]))

    def render(self, t):
        tt = t % len(self.roll)
        print self.instrument.name, self.roll[tt]


class Sequencer:

    def __init__(self, loops=[], bpm=30):
        self.loops = loops
        self.set_bpm(bpm)

        # find longest loop
        self.longest = max([len(l.roll) for l in self.loops])

    def set_bpm(self, bpm):
        self.delay = 60.0 / bpm

    def play(self):
        for t in range(self.longest):
            for l in self.loops:
                l.play(t)
                l.render(t)
            sleep(self.delay)


def scale2ints(minguscale, key='C', span=2, octave=3):
    scale = minguscale(key, span)
    notas = []
    for o in range(octave, octave+span):
        for n in range(7):
            notas.append(int(Note(scale.ascending()[n], o)))
    notas.append(int(Note(scale.tonic, octave+span)))
    return notas
