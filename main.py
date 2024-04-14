from inputs import get_gamepad
import os
import rtmidi

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

KEY_EVENT = "Key"
AXIS_EVENT = "Absolute"

LEFT_STICK_X = "ABS_X"
LEFT_STICK_Y = "ABS_Y"
RIGHT_STICK_X = "ABS_RX"
RIGHT_STICK_Y = "ABS_RY"
LEFT_TRIGGER = "ABS_Z"
RIGHT_TRIGGER = "ABS_RZ"

BUTTON_SOUTH = "BTN_SOUTH"
BUTTON_WEST = "BTN_WEST"
BUTTON_EAST = "BTN_EAST"
BUTTON_NORTH = "BTN_NORTH"

LEFT_BUMPER = "BTN_TL"
RIGHT_BUMPER = "BTN_TR"

R_THREE = "BTN_THUMBR"
L_THREE = "BTN_THUMBL"


STATE_UP = 0
STATE_DOWN = 1
STATE_HELD = 2
STATE_BLANK = 3


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

class gamepadstate:
    def __init__(self) -> None:
        self.axisStates: dict[str, int] = {}
        self.buttonStates: dict[str, int] = {}
    def IngestAxisEvent(self, event) -> None:
        self.axisStates[event.code] = event.state
    def IngestButtonEvent(self, event) -> None:        
        self.buttonStates[event.code] = event.state
    def ClearButtonEvents(self) -> None:
        for key in self.buttonStates:
            if(self.buttonStates[key] == STATE_DOWN):
                self.buttonStates[key] = STATE_HELD
            elif(self.buttonStates[key] == STATE_UP):
                self.buttonStates[key] = STATE_BLANK
    def PollEvents(self) -> None:
        events = get_gamepad()
        for event in events:
            if event.ev_type == "Key":
                self.IngestButtonEvent(event)
            elif event.ev_type == "Absolute":
                self.IngestAxisEvent(event)
            else:
                self.ClearButtonEvents()
    def GetAxis(self, name: str) -> int:
        if(name in self.axisStates):
            return self.axisStates[name]
        else:
            return 0
    def GetButtonDown(self, name: str) -> bool:
        #print(f"Actual Button State: {self.buttonStates[name]}")
        if(name in self.buttonStates):  
            return self.buttonStates[name] == STATE_DOWN
        else:
            return False
    def GetButtonUp(self, name: str) -> bool:
        if(name in self.buttonStates):
            return self.buttonStates[name] == STATE_UP
        else:
            return False
    def GetButtonHeld(self, name: str) -> bool:
        if(name in self.buttonStates):
            return self.buttonStates[name] == STATE_HELD
        else:
            return False
        
        
        
    def GetVector(self, _left: bool) -> Vector2:
        if(_left):
            return Vector2(self.GetAxis(LEFT_STICK_X), self.GetAxis(LEFT_STICK_Y))
        else:
            return Vector2(self.GetAxis(LEFT_STICK_X), self.GetAxis(LEFT_STICK_Y))

if __name__ == "__main__":
    states = gamepadstate()
    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()

    if available_ports:
        midiout.open_port(1)
    else:
        print("No ports found")
    PAD_ONE = 40
    PAD_TWO = 38
    PAD_THREE = 37
    PAD_FOUR = 36

    pad_one_on = [0x90, 51, 112]
    pad_one_off = [0x80, 51, 0]

    def generateMidiMessage(on: bool, pad: int):
        if on:
            return [0x90, pad, 112]
        else:
            return [0x90, pad, 0]




    while 1:

        states.PollEvents()

        if states.GetButtonDown(name=BUTTON_SOUTH):
            print("Sending NoteOn event.")
            midiout.send_message(generateMidiMessage(True, PAD_ONE))
        if(states.GetButtonUp(name=BUTTON_SOUTH)):
            print("Sending NoteOff event.")
            midiout.send_message(generateMidiMessage(False, PAD_ONE))

        if states.GetButtonDown(name=BUTTON_WEST):
            print("Sending NoteOn event.")
            midiout.send_message(generateMidiMessage(True, PAD_TWO))
        if(states.GetButtonUp(name=BUTTON_WEST)):
            print("Sending NoteOff event.")
            midiout.send_message(generateMidiMessage(False, PAD_TWO))

        if states.GetButtonDown(name=BUTTON_EAST):
            print("Sending NoteOn event.")
            midiout.send_message(generateMidiMessage(True, PAD_THREE))
        if(states.GetButtonUp(name=BUTTON_EAST)):
            print("Sending NoteOff event.")
            midiout.send_message(generateMidiMessage(False, PAD_THREE))

        if states.GetButtonDown(name=BUTTON_NORTH):
            print("Sending NoteOn event.")
            midiout.send_message(generateMidiMessage(True, PAD_FOUR))
        if(states.GetButtonUp(name=BUTTON_NORTH)):
            print("Sending NoteOff event.")
            midiout.send_message(generateMidiMessage(False, PAD_FOUR))

        


        
            
        




            

