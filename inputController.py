from inputs import get_gamepad, devices
from constants import GAMEPAD_KEYMAP, KEY_STATE, EVENT_TYPE, DEVICE_TYPE
from utility import Vector2

def GetDeviceList():
    return devices.all_devices

def DetectDeviceType(device):
    if(device in devices.gamepads):
        return DEVICE_TYPE.GAMEPAD
    elif(device in devices.mice):
        return DEVICE_TYPE.MOUSE
    elif(device in devices.keyboards):
        return DEVICE_TYPE.KEYBOARD
    elif(device in devices.other_devices):
        return DEVICE_TYPE.OTHER
    else:
        return DEVICE_TYPE.NONE


#Monitors the input state of the gamepad. Poll events will wait until input is detected 
#so should be threaded if not wanting to block execution
class gamepadstate:
    def __init__(self) -> None:
        self.axisStates: dict[str, int] = {}
        self.buttonStates: dict[str, int] = {}
    def IngestAxisEvent(self, event) -> None:
        self.axisStates[event.code] = event.state
    def IngestButtonEvent(self, event) -> None:
        self.buttonStates[event.code] = KEY_STATE(event.state)
    def ClearButtonEvents(self) -> None:
        for key in self.buttonStates:
            if(self.buttonStates[key] == KEY_STATE.STATE_DOWN):
                self.buttonStates[key] = KEY_STATE.STATE_HELD
            elif(self.buttonStates[key] == KEY_STATE.STATE_UP):
                self.buttonStates[key] = KEY_STATE.STATE_BLANK
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
            if(self.buttonStates[name] == KEY_STATE.STATE_DOWN) :
                print("this should evaluate to true")
            return self.buttonStates[name] == KEY_STATE.STATE_DOWN
        else:
            return False
    def GetButtonUp(self, name: str) -> bool:
        if(name in self.buttonStates):
            return self.buttonStates[name] == KEY_STATE.STATE_UP
        else:
            return False
    def GetButtonHeld(self, name: str) -> bool:
        if(name in self.buttonStates):
            return self.buttonStates[name] == KEY_STATE.STATE_HELD
        else:
            return False
        
    def GetStickVector(self, _left: bool) -> Vector2:
        if(_left):
            return Vector2(self.GetAxis(GAMEPAD_KEYMAP.LEFT_STICK_X), self.GetAxis(GAMEPAD_KEYMAP.LEFT_STICK_Y))
        else:
            return Vector2(self.GetAxis(GAMEPAD_KEYMAP.LEFT_STICK_X), self.GetAxis(GAMEPAD_KEYMAP.LEFT_STICK_Y))
