from constants import DEVICE_TYPE, DEVICE_TO_KEYMAP, ACTION_TYPE
from utility import note_to_number
class Action:
    def __init__(self, actionType) -> None:
        self.action_type: ACTION_TYPE = actionType

class PlayNoteAction(Action):
    def __init__(self, note: int) -> None:
        super().__init__(ACTION_TYPE.PLAY_NOTE)
        self.note: int = note


class KeyActionDirectory:
    def __init__(self) -> None:
        self.action_dict: dict[str, Action] = {}
    def AddPlayNoteAction(self, key, note) -> None:
        self.action_dict[key] = PlayNoteAction(note=note)
        #print("adding Play Note Action")
    def GetAction(self, key) -> int:
        return self.action_dict[key]
    def AddDefaultActions(self, deviceType):
        for xc in DEVICE_TO_KEYMAP[deviceType]:
            if(xc not in self.action_dict):
                self.AddPlayNoteAction(xc, note_to_number('C', 3))

