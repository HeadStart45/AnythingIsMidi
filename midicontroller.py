import rtmidi
import gamepadstate as gs
from constants import MIDI_PAD, GAMEPAD_KEY, GAMEPAD_ABSOLUTE
import KeyPatchDirectory as kpd

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
        midiout.open_port(1)
else:
    print("No ports found")

def generateMidiMessage(on: bool, pad: int):
    if on:
        return [0x90, pad, 112]
    else:
        return [0x80, pad, 0]

def StartPlayNote(note: int) -> None:
    midiout.send_message(generateMidiMessage(True, note))

def StopPlayNote(note: int) -> None:
    midiout.send_message(generateMidiMessage(False, note))

#called as a thread from the gui main loop, runs once the pad is activated
def ControllerLoop(window, inDirectory: kpd.KeyActionDirectory) -> None:
    states = gs.gamepadstate()
    directory: kpd.KeyActionDirectory = inDirectory

    while 1:
        #poll the gamepad for input
        states.PollEvents()

        for key in GAMEPAD_KEY:
            if(states.GetButtonDown(key)):
                StartPlayNote(directory.GetAction(key))
            if(states.GetButtonUp(key)):
                StopPlayNote(directory.GetAction(key))
