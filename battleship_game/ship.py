from typing import List, Tuple, Set


class Ship:
    def __init__(self, name: str, position: List[Tuple[int, int]]):
        self.name = name  # Store name of the ship
        self.position = position  # Store its position
        self.size = len(self.position)  # Calculate the size of ship
        self.hits: Set[Tuple[int, int]] = set()  # Creates an empty set to track

    def add_hit(self, coord: Tuple[int, int]) -> None:
        if coord in self.position:
            self.hits.add(coord)

    def destroy(self) -> bool:
        return len(self.hits) == self.size
