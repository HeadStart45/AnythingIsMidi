import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

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
