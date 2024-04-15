import rtmidi
from inputController import gamepadstate
from constants import DEVICE_TO_KEYMAP, DEVICE_TYPE
import KeyActionDirectory as kad



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
    def ControllerLoop(self) -> None:   
        self.Setup()
        while(self.midiout.is_port_open()):
            #poll the gamepad for input
            self.states.PollEvents()
            print("loop")
            for key in DEVICE_TO_KEYMAP[self.activeInputType]:
                if(self.states.GetButtonDown(key)):
                    self.StartPlayNote(self.key_action_directory.GetAction(key))
                    print("Playing Note")
                if(self.states.GetButtonUp(key)):
                    self.StopPlayNote(self.key_action_directory.GetAction(key))
                    print("Stop Playing Note")
    def HasPort(self) -> bool:
        return self.port != -1 # -1 is the default should only be sit to this if there are no ports available
