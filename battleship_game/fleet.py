class ship:
    def __init__(self, size: int, type: str, postion: tuple, orientation: str):
        self.size = size
        self.type = type
        self.postion = postion
        self.orientation = orientation


submarine = ship(1, 'sub', (1,1))
