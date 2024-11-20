"""Generic helpers"""


class Coordinate:
    """Represent a single point within a 2D space."""

    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"<Coordinate x: {self.x}, y:{self.y}>"

    def neighbours(self):
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for delta in deltas:
            yield Coordinate(self.x + delta[0], self.y + delta[1])


class Grid:
    """Represent a 2D grid."""

    def __init__(self, data):
        if isinstance(data[0], str):
            self._data = [list(x) for x in data]
        else:
            self._data = data

    def __repr__(self) -> str:
        return f"<Grid rows: {len(self._data)}, columns: {len(self._data[0])}>"

    def __str__(self) -> str:
        return "\n".join("".join(map(str, row)) for row in self._data)

    def all_coordinates(self):
        for r, line in enumerate(self._data):
            for c, _ in enumerate(line):
                yield Coordinate(r, c)

    def set(self, coordinate, value):
        self._data[coordinate.x][coordinate.y] = value

    def get(self, coordinate):
        return self._data[coordinate.x][coordinate.y]
