class KeyActionDirectory:
    def __init__(self) -> None:
        self.actionDict: dict[str, int] = {}
    def AddPlayNoteAction(self, key, note) -> None:
        self.actionDict[key] = note
    def GetAction(self, key) -> int:
        return self.actionDict[key]

