import pretty_midi
import random

class Measure:
    def __init__(self, pitch):
        self.beats = [False, False, False, False, False, False, False, False]
        self.pitchName = pitch
        self.pitch = pretty_midi.note_name_to_number(pitch)
        #self.changeChance = 16 - 1
        self.changeChanceMin = 0
        self.changeChanceMax = 100
        self.place = 0
        self.length = 280
        self.lengthOfNote = .25 #1 eigth note at 120bpm

        self.pm = pretty_midi.PrettyMIDI()
        self.cello_program = pretty_midi.instrument_name_to_program('Cello')
        self.cello = pretty_midi.Instrument(program=self.cello_program)

        self.create()
        return

    def create(self):
        self.createFirstMeasure()

        while self.place < self.length:
            self.decideIfBeatShouldChange()
            self.createMeasure()

        self.createFile()
        return

    def createFirstMeasure(self):
        self.beats[random.randint(0, 7)] = True
        self.createMeasure()
        return

    def decideIfBeatShouldChange(self):
        for each in range(0, 7):
            if random.randint(0, self.changeChance) == 0:
                self.invertBeat(each)
        return

    def invertBeat(self, i):
        if self.beats[i] == True:
            self.beats[i] = False
        elif self.beats[i] == False:
            self.beats[i] = True
        return

    def createMeasure(self):
        for each in range(0, 7):
            self.place = self.place + self.lengthOfNote
            if self.beats[each] == True:
                note = pretty_midi.Note(velocity=100,
                                        pitch=self.pitch,
                                        start=self.place,
                                        end=self.place + self.lengthOfNote)
                self.cello.notes.append(note)
        return

    def createFile(self):
        self.pm.instruments.append(self.cello)
        self.pm.write(self.pitchName + ' output.mid')
        return

#near constant change for each line

measure = Measure('C#4')
measure = Measure('A4')
measure = Measure('E5')
measure = Measure('A5')
measure = Measure('F#3')
measure = Measure('C#3')
measure = Measure('A2')
measure = Measure('E2')
print('done')
