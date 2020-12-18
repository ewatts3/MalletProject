import pretty_midi
import random

class Pitch:
    def __init__(self, pitchName):
        self.pitch = pretty_midi.note_name_to_number(pitchName) #+ 12
        self.beats = [False, False, False, False, False, False, False, False]
        return

    def changeOneBeatForFirstMeasure(self):
        self.beats[random.randint(0, 7)] = True
        return

    def decideIfBeatShouldChange(self, indexOfBeat, changeChance):
        if random.randint(0, changeChance) == 0:
                self.invertBeat(indexOfBeat)
        return

    def invertBeat(self, i):
        if self.beats[i] == True:
            self.beats[i] = False
        elif self.beats[i] == False:
            self.beats[i] = True
        return

    def getPitch(self):
        return self.pitch

    def getBeats(self):
        return self.beats

    def setBeats(self, newBeats):
        self.beats = newBeats
        return

class changeChanceObject:
    def __init__(self, range):
        self.range = range
        self.currentChance = random.randint(self.range[0], self.range[1])
        self.isIncreasing = True
        return

    def getCurrentChance(self):
        if self.currentChance == self.range[1]:
            self.isIncreasing = False
        elif self.currentChance == self.range[0]:
            self.isIncreasing = True

        if self.isIncreasing is True:
            self.currentChance = self.currentChance + 1
        else:
            self.currentChance = self.currentChance - 1

        return self.currentChance

class Composition:
    def __init__(self, noteNames):
        pm = pretty_midi.PrettyMIDI()
        noteSet = self.getNoteSet(noteNames)
        #changeChance = 16 - 1
        changeChanceRange = [0, 9]
        changeChance = changeChanceObject(changeChanceRange)
        place = 0
        lengthOfPiece = 120
        lengthOfNote = .25 #1 eigth note at 120bpm
        
        instrument = self.create(pm, noteSet,changeChance, place, lengthOfPiece, lengthOfNote)
        self.createFile(pm, instrument)
        return

    def getNoteSet(self, noteNames):
        noteSet = []
        for i in range(0, len(noteNames)):
            pitch = Pitch(noteNames[i])
            noteSet.append(pitch)
        return noteSet

    def create(self, pm, noteSet, changeChance, place, lengthOfPiece, lengthOfNote):
        cello_program = pretty_midi.instrument_name_to_program('Cello')
        instrument = pretty_midi.Instrument(program=cello_program)

        for i in range(0, len(noteSet)):
            self.createFirstMeasure(noteSet)
        place = self.createMeasure(noteSet, place, lengthOfNote, instrument)

        while place < lengthOfPiece:
            self.decideIfBeatsShouldChange(noteSet, self.getChangeChance(changeChance))
            place = self.createMeasure(noteSet, place, lengthOfNote, instrument)

        return instrument

    def getChangeChance(self, changeChanceObject):
        changeChance = changeChanceObject.getCurrentChance()
        print(changeChance)
        return changeChance

    def createFirstMeasure(self, noteSet):
        for i in range(0, len(noteSet)):
            noteSet[i].changeOneBeatForFirstMeasure()
        return

    def decideIfBeatsShouldChange(self, noteSet, changeChance):
        for i in range(0, len(noteSet)):
            noteSet[i].decideIfBeatShouldChange(i, changeChance)
        return

    def createMeasure(self, noteSet, place, lengthOfNote, instrument):
        startingPlace = place
        for i in range(0, len(noteSet)):
            currentPlace = startingPlace
            currentBeats = noteSet[i].getBeats()
            currentPitch = noteSet[i].getPitch()
            for j in range(0, len(currentBeats)):
                if currentBeats[j] == True:
                    note = pretty_midi.Note(velocity=100,
                                        pitch=currentPitch,
                                        start=currentPlace,
                                        end=currentPlace + lengthOfNote)
                    instrument.notes.append(note)
                currentPlace = currentPlace + lengthOfNote
        return currentPlace

    def createFile(self, pm, instrument):
        pm.instruments.append(instrument)
        pm.write('output.mid')
        return

#"swelling" change for each line

noteNames = ['E2', 'A2', 'C#3', 'F#3', 'C#4', 'A4', 'E5', 'A5']
Composition(noteNames)
