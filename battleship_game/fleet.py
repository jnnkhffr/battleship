class ship:
    def __init__(self, size: int, name: str, postion: tuple):
        self.size = size
        self.name = name
        self.postion = postion


submarine = ship(1, 'sub', (1,1))
