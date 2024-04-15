import rtmidi
from inputController import gamepadstate as gs
from constants import MIDI_PAD, GAMEPAD_KEY, GAMEPAD_ABSOLUTE
import KeyPatchDirectory as kpd

class MidiController:
    def __init__(self) -> None:
        self.midiout = rtmidi.MidiOut()
        self.available_ports = self.midiout.get_ports()
        
        self.port = 0

    def Setup(self) -> None:
        if self.available_ports:
            self.midiout.open_port(self.port)
        else:
            print("No ports found")
    def SetPort(self, portIndex: int) -> None:
        self.port = portIndex
    def RefreshPorts(self) -> None:
        self.midiout.delete()
        self.midiout = rtmidi.MidiOut()
        self.available_ports = self.midiout.get_ports()


    def generateMidiMessage(self, on: bool, pad: int):
        if on:
            return [0x90, pad, 112]
        else:
            return [0x80, pad, 0]
    def StartPlayNote(self, note: int) -> None:
        self.midiout.send_message(self.generateMidiMessage(True, note))
    def StopPlayNote(self, note: int) -> None:
        self.midiout.send_message(self.generateMidiMessage(False, note))


#called as a thread from the gui main loop, runs once the pad is activated
def ControllerLoop(window, midi, inDirectory: kpd.KeyActionDirectory) -> None:


    #midi.Setup
    
    states = gs.gamepadstate()
    directory: kpd.KeyActionDirectory = inDirectory

    while 1:
        #poll the gamepad for input
        states.PollEvents()

        for key in GAMEPAD_KEY:
            if(states.GetButtonDown(key)):
                midi.StartPlayNote(directory.GetAction(key))
            if(states.GetButtonUp(key)):
                midi.StopPlayNote(directory.GetAction(key))
