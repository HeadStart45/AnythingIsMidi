import rtmidi
from inputController import gamepadstate as gs
from constants import DEVICE_TO_KEYMAP, DEVICE_TYPE
import KeyActionDirectory as kad

class MidiController:
    def __init__(self) -> None:
        self.midiout = rtmidi.MidiOut()
        self.available_ports = self.midiout.get_ports()
        self.key_action_directory = kad.KeyActionDirectory()
        self.activeInputType: DEVICE_TYPE = DEVICE_TYPE.NONE
        self.port = 0

    def Setup(self) -> None:
        if self.available_ports:
            self.midiout.open_port(self.port)
        else:
            print("No ports found")
    def SetPort(self, portIndex: int) -> None:
        self.port = portIndex
    def SetActiveInput(self, inputType):
        self.activeInputType = inputType
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
    def ControllerLoop(self, window) -> None:   
        self.Setup
        states = gs.gamepadstate()
        while 1:
            #poll the gamepad for input
            states.PollEvents()

            for key in DEVICE_TO_KEYMAP[self.activeInputType]:
                if(states.GetButtonDown(key)):
                    self.StartPlayNote(self.key_action_directory.GetAction(key))
                if(states.GetButtonUp(key)):
                    self.StopPlayNote(self.key_action_directory.GetAction(key))

