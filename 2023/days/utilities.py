"""Generic helpers"""

import itertools


def list_1d_to_2d(data, columns):
    return [data[i : i + columns] for i in range(0, len(data), columns)]


def pairwise_without_overlap(iterable):
    a = iter(iterable)
    return zip(a, a)


class Coordinate:
    """Represent a single point within a 2D space."""

    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"<Coordinate x: {self.x}, y:{self.y}>"

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y)

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __lt__(self, other) -> bool:
        return (self.x, self.y) < (other.x, other.y)

    def neighbours(self):
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for delta in deltas:
            yield Coordinate(self.x + delta[0], self.y + delta[1])


class Matrix:
    """Represent a 2D matrix.

    Improvements:
    * _data as a 2d list to avoid index calculation?
    * factory functions to create the matrix (from string, from custom type)
    """

    def __init__(self, data):
        if isinstance(data[0], str):
            self._data = [list(x) for x in data]
        self._data = list(itertools.chain.from_iterable(data))
        self.rows = len(data)
        self.columns = len(data[0])

    def __iter__(self):
        return iter(self._data)

    def __repr__(self) -> str:
        return f"<Matrix rows: {self.rows}, columns: {self.columns}>"

    def __str__(self) -> str:
        return "\n".join(
            " ".join(map(str, row)) for row in list_1d_to_2d(self._data, self.columns)
        )

    # def all_coordinates(self):
    #     for r, line in enumerate(self._data):
    #         for c, _ in enumerate(line):
    #             yield Coordinate(r, c)

    def set(self, coordinate, value):
        index = coordinate.x * self.columns + coordinate.y
        self._data[index] = value

    def get(self, coordinate):
        index = coordinate.x * self.columns + coordinate.y
        return self._data[index]

    def find(self, needle) -> Coordinate:
        index = self._data.index(needle)
        x = index // self.columns
        y = index % self.columns
        return Coordinate(x, y)

    def find_all(self, needle) -> list[Coordinate]:
        indices = [i for i, x in enumerate(self._data) if x == needle]
        return [Coordinate(i // self.columns, i % self.columns) for i in indices]
