from enum import Enum
class GAMEPAD_KEY(str, Enum):
    BUTTON_SOUTH = "BTN_SOUTH"
    BUTTON_WEST = "BTN_WEST"
    BUTTON_EAST = "BTN_EAST"
    BUTTON_NORTH = "BTN_NORTH"

    LEFT_BUMPER = "BTN_TL"
    RIGHT_BUMPER = "BTN_TR"

    R_THREE = "BTN_THUMBR"
    L_THREE = "BTN_THUMBL"

class GAMEPAD_ABSOLUTE(str, Enum):
    LEFT_STICK_X = "ABS_X"
    LEFT_STICK_Y = "ABS_Y"

    RIGHT_STICK_X = "ABS_RX"
    RIGHT_STICK_Y = "ABS_RY"

    LEFT_TRIGGER = "ABS_Z"
    
    RIGHT_TRIGGER = "ABS_RZ"

class MOUSE_KEY(str, Enum):
    LEFT_BUTTON = "BTN_LEFT"
    RIGHT_BUTTON = "BTN_RIGHT"
    MIDDLE_BUTTON = "BTN_MIDDLE"
    SIDE_BUTTON = "BTN_SIDE"

class KEY_STATE(Enum):
    STATE_UP = 0
    STATE_DOWN = 1
    STATE_HELD = 2
    STATE_BLANK = 3

class EVENT_TYPE(Enum):
    KEY_EVENT = "Key"
    AXIS_EVENT = "Absolute"

class MIDI_PAD(Enum):
    PAD_ONE = 40
    PAD_TWO = 38
    PAD_THREE = 37
    PAD_FOUR = 36

class DEVICE_TYPE(Enum):
    NONE = 0
    GAMEPAD = 1,
    KEYBOARD = 2,
    MOUSE = 3,
    OTHER = 4,


