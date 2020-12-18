import pretty_midi
import random

class Measure:
    def __init__(self, pitch):
        self.beats = [False, False, False, False, False, False, False, False]
        self.pitchName = pitch
        self.pitch = pretty_midi.note_name_to_number(pitch)
        self.changeChance = 64 - 1
        #self.currentForm = self
        self.place = 0
        self.lengthOfNote = .25 #1 eigth note at 120bpm

        self.pm = pretty_midi.PrettyMIDI()
        self.cello_program = pretty_midi.instrument_name_to_program('Cello')
        self.cello = pretty_midi.Instrument(program=self.cello_program)

        self.create()
        return

    def create(self):
        self.createFirstForm()

        #try each beat until all are playing
        done = False
        while not done:
            self.decideIfBeatShouldBeAdded()
            self.createMeasure()
            done = True
            for each in range(0, 7):
                if self.beats[each] == False:
                    done = False

        #try each beat until all are silent
        done = False
        while not done:
            self.decideIfBeatShouldBeRemoved()
            self.createMeasure()
            done = True
            for each in range(0, 7):
                if self.beats[each] == True:
                    done = False

        self.createFile()
        return

    def createFirstForm(self):
        self.beats[random.randint(0, 7)] = True
        self.createMeasure()
        return

    def decideIfBeatShouldBeAdded(self):
        for each in range(0, 7):
            if self.beats[each] == False:
                if random.randint(0, self.changeChance) == 0:
                   self.beats[each] = True
        return

    def decideIfBeatShouldBeRemoved(self):
        for each in range(0, 7):
            if self.beats[each] == True:
                if random.randint(0, self.changeChance) == 0:
                   self.beats[each] = False
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

#each line build up then tear down

#ts = pretty_midi.TimeSignature(4, 4, 0)
#measure = Measure('C#4')
#measure = Measure('A4')
#measure = Measure('E5')
#measure = Measure('A5')
#measure = Measure('F#3')
#measure = Measure('D3')
measure = Measure('B2')
#measure = Measure('G#2')
print('done')