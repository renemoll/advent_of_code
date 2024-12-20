"""Generic helpers"""

import itertools
import re
import typing


def clamp(n: float, smallest: float, largest: float) -> float:
    return max(smallest, min(n, largest))


def diff(xs: list) -> list:
    return [b - a for a, b in itertools.pairwise(xs)]


def is_even(n: int) -> bool:
    return n % 2 == 0


def list_1d_to_2d(data, columns):
    return [data[i : i + columns] for i in range(0, len(data), columns)]


def pairwise_without_overlap(iterable):
    a = iter(iterable)
    return zip(a, a)


def parse_ints(text: str) -> list[int]:
    return list(map(int, re.findall(r"-?\d+", text)))


def take_n(data: list, n: int) -> typing.Generator[list, None, None]:
    for i in range(0, len(data), n):
        yield data[i : i + n]


def transpose_2d_list(l):
    return list(map(list, zip(*l)))


class Coordinate:
    """Represent a single point within a 2D space."""

    x: int
    y: int

    def __init__(self, x, y) -> "Coordinate":
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"<Coordinate x: {self.x}, y:{self.y}>"

    def __add__(self, other: "Coordinate") -> "Coordinate":
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Coordinate") -> "Coordinate":
        return Coordinate(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, int):
            return Coordinate(self.x * other, self.y * other)
        raise TypeError

    def __rmul__(self, other):
        if isinstance(other, int):
            return Coordinate(self.x * other, self.y * other)
        raise TypeError

    def __eq__(self, other: "Coordinate") -> bool:
        try:
            return self.x == other.x and self.y == other.y
        except AttributeError:
            return self.x == other[0] and self.y == other[1]

    def __lt__(self, other: "Coordinate") -> bool:
        return (self.x, self.y) < (other.x, other.y)

    def neighbours(self) -> typing.Generator["Coordinate", None, None]:
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for delta in deltas:
            yield Coordinate(self.x + delta[0], self.y + delta[1])


class Grid:
    """Represent a 2D grid.

    Improvements:
    * _data as a 2d list to avoid index calculation?
    * factory functions to create the matrix (from string, from custom type)
    """

    def __init__(self, data):
        if isinstance(data[0], str):
            self._data = [list(x) for x in data]
        self._data = list(itertools.chain.from_iterable(data))
        self._stride = len(data[0])

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

    def set(self, coordinate: Coordinate, value) -> None:
        index = coordinate.x + self._stride * coordinate.y
        self._data[index] = value

    def get(self, coordinate: Coordinate):
        index = coordinate.x + self._stride * coordinate.y
        return self._data[index]

    def find(self, needle) -> Coordinate:
        index = self._data.index(needle)
        x = index % self._stride
        y = index // self._stride
        return Coordinate(x, y)

    def find_all(self, needle) -> typing.Generator["Coordinate", None, None]:
        indices = [i for i, x in enumerate(self._data) if x == needle]
        for i in indices:
            yield Coordinate(i % self._stride, i // self._stride)

    def neighbours(
        self, coordinate: Coordinate, include_diagonals=True
    ) -> typing.Generator[Coordinate, None, None]:
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        if include_diagonals:
            deltas += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for delta in deltas:
            x = coordinate.x + delta[0]
            y = coordinate.y + delta[1]
            if 0 <= x < self.rows and 0 <= y < self.columns:
                yield Coordinate(x, y)
            else:
                continue

    # def all_coordinates(self) -> typing.Generator[Coordinate, None, None]:
    #     for r in range(self.rows):
    #         for c in range(self.columns):
    #             yield Coordinate(r, c)


class SparseGrid:
    """A spare grid representation, only storing specific values and their coordinates."""

    def __init__(self, data, predicate=lambda x: True):
        """TODO: datatype of self._data"""
        self._data = {}
        for r, row in enumerate(data):
            for c, ch in enumerate(row):
                if predicate(ch):
                    self._data[Coordinate(c, r)] = ch
        self.rows = len(data)
        self.columns = len(data[0])

    def __iter__(self):
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def pop_front(self):
        c = list(self._data)[0]
        v = self._data.pop(c)
        return (c, v)

    def keys(self):
        return set(self._data.keys())

    def values(self):
        return self._data.values()

    def find(self, needle) -> Coordinate:
        for c, v in self._data.items():
            if v == needle:
                return c
        raise IndexError

    def find_all(self, needle) -> typing.Generator["Coordinate", None, None]:
        for c, value in self._data.items():
            if value == needle:
                yield c

    def front(self):
        c = list(self._data)[0]
        v = self._data[c]
        return (c, v)

    def get(self, coordinate: Coordinate):
        return self._data[coordinate]

    def neighbours(
        self, coordinate: Coordinate, include_diagonals=True
    ) -> typing.Generator[Coordinate, None, None]:
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        if include_diagonals:
            deltas += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for delta in deltas:
            x = coordinate.x + delta[0]
            y = coordinate.y + delta[1]
            c = Coordinate(x, y)
            if 0 <= x < self.rows and 0 <= y < self.columns and c in self.keys():
                yield c
            else:
                continue

    def remove(self, coordinate: Coordinate):
        if coordinate in self.keys():
            self._data.pop(coordinate)
