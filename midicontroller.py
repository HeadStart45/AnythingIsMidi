import rtmidi
from inputController import gamepadstate
from constants import DEVICE_TO_KEYMAP, DEVICE_TYPE, OCTAVE_MODE, ACTION_TYPE
import KeyActionDirectory as kad
import utility



class MidiController:
    def __init__(self) -> None:
        self.midiout = rtmidi.MidiOut()
        self.available_ports = self.midiout.get_ports()
        self.key_action_directory = kad.KeyActionDirectory()
        self.activeInputType: DEVICE_TYPE = DEVICE_TYPE.NONE
        self.port = -1
        self.states = gamepadstate()
        self.SUPPORTED_DEVICES = [DEVICE_TYPE.GAMEPAD]
        self.loop = False
        self.programOctave = 3
    def Setup(self) -> None:
        if self.available_ports:
            self.midiout.open_port(self.port)
        else:
            print("No ports found")
    def Deactivate(self) -> None:
        self.midiout.close_port()
    def SetPort(self, portIndex: int) -> None:
        self.port = portIndex
    def SetActiveInput(self, inputType):
        self.activeInputType = inputType
    def RefreshPorts(self) -> None:
        self.midiout.delete()
        self.midiout = rtmidi.MidiOut()
        self.available_ports = self.midiout.get_ports()
    def IsDeviceSupported(self,device) -> bool:
        return device in self.SUPPORTED_DEVICES
    def GetAvailablePorts(self):
        ports = []
        for port in self.available_ports:
            if(port != "Microsoft GS Wavetable Synth 0"):
                ports.append(port)
        if len(ports) == 0:
            ports.append("NONE")
        return ports
    def generateMidiMessage(self, on: bool, pad: int):
        if on:
            return [0x90, pad, 112]
        else:
            return [0x80, pad, 0]
    def StartPlayNote(self, note: int) -> None:
        self.midiout.send_message(self.generateMidiMessage(True, note))
    def StopPlayNote(self, note: int) -> None:
        self.midiout.send_message(self.generateMidiMessage(False, note))

    def HasPort(self) -> bool:
        return self.port != -1 # -1 is the default should only be sit to this if there are no ports available
    def AddPlayNoteAction(self,key, note, octave, octave_mode):
        if(octave_mode == OCTAVE_MODE.EXPLICIT.name):
            noteAsNumber: int = utility.note_to_number(note, octave=int(octave))
            self.key_action_directory.AddPlayNoteAction(key, noteAsNumber)
        else:
            noteAsNumber: int = utility.note_to_number(note, octave=self.programOctave)
            self.key_action_directory.AddPlayNoteAction(key, noteAsNumber)
    #MAIN Input loop
    def ControllerLoop(self) -> None:   
        self.Setup()
        while(self.midiout.is_port_open()):
            #poll the gamepad for input
            self.states.PollEvents()
            #print("loop")
            for key in DEVICE_TO_KEYMAP[self.activeInputType]:
                if(self.key_action_directory.GetAction(key).action_type == ACTION_TYPE.PLAY_NOTE):
                    if(self.states.GetButtonDown(key)):
                        self.StartPlayNote(self.key_action_directory.GetAction(key).note)
                        #print("Playing Note")
                    if(self.states.GetButtonUp(key)):
                        self.StopPlayNote(self.key_action_directory.GetAction(key).note)
                        #print("Stop Playing Note")