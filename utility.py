import os
from constants import NOTES, OCTAVES, NOTES_IN_OCTAVE

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class Vector2:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    def setX(self, x: int):
        self.x = x
    def setY(self, y: int):
        self.y = y

errors = {
    'program': 'Bad input, please refer this spec-\n'
               'http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/program_change.htm',
    'notes': 'Bad input, please refer this spec-\n'
             'http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/midi_note_numbers_for_octaves.htm'
}


def number_to_note(number: int) -> tuple:
    octave = number // NOTES_IN_OCTAVE
    assert octave in OCTAVES, errors['notes']
    assert 0 <= number <= 127, errors['notes']
    note = NOTES[number % NOTES_IN_OCTAVE]

    return note, octave


def note_to_number(note: str, octave: int) -> int:
    assert note in NOTES, errors['notes']
    assert octave in OCTAVES, errors['notes']

    note = NOTES.index(note)
    note += (NOTES_IN_OCTAVE * octave)

    assert 0 <= note <= 127, errors['notes']

    return note
#Helper class for generating key names for pysimplegui elements dynamically
#Key name is the name of the input on the keymap
class PSGKeyGenerator:
    def __init__(self) -> None:
        #constant keys
        self.PortCombo = '-PORTCOMBO-'
        self.DeviceCombo = '-DEVICECOMBO-'
        
        self.GamePadFrame = '-GAMEPADFRAME-'
        self.MouseFrame = '-MOUSEFRAME-'
        self.NotSupportedFrame = '-NOTSUPPORTED-'

        self.ActivateButton = 'Activate'
        self.DeactivateButton = 'Deactivate'
        self.QuitButton = 'Quit'
    
    def OctaveMode(self, keyName: str)->str:
        return f"-{keyName}OCTAVEMODE-"
    def Octave(self, keyName: str)->str:
        return f"-{keyName}OCTAVE-"
    def ActionType(self, keyName: str)->str:
        return f"-{keyName}ACTIONTYPE-"
    def Note(self, keyName: str)->str:
        return f"-{keyName}NOTE-"
    

