from constants import DEVICE_TYPE, DEVICE_TO_KEYMAP

class KeyActionDirectory:
    def __init__(self) -> None:
        self.actionDict: dict[str, int] = {}
    def AddPlayNoteAction(self, key, note) -> None:
        self.actionDict[key] = note
    def GetAction(self, key) -> int:
        return self.actionDict[key]
    def AddDefaultActions(self, deviceType):
        for xc in DEVICE_TO_KEYMAP[deviceType]:
            if(xc not in self.actionDict):
                self.AddPlayNoteAction(xc, 60)

