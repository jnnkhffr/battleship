from battleship_game.config import SUB_SIZE, FRIG_SIZE, DEST_SIZE, ACC_SIZE


class ship:
    def __init__(self, size: int, position: tuple, orientation: str):
        self.size = size
        self.position = position
        self.orientation = orientation

# All ships in different classes

class submarine(ship):
    def __init__(self, size: int, position: tuple, orientation: str):
        super().__init__(size, position, orientation)
        self.size = SUB_SIZE

class frigate(ship):
    def __init__(self, size: int, position: tuple, orientation: str):
        super().__init__(size, position, orientation)
        self.size = FRIG_SIZE

class destroyer(ship):
    def __init__(self, size: int, position: tuple, orientation: str):
        super().__init__(size, position, orientation)
        self.size = DEST_SIZE
class aircraft_carrier(ship):
    def __init__(self, size: int, position: tuple, orientation: str):
        super().__init__(size, position, orientation)
        self.size = ACC_SIZE
