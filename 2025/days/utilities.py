"""Generic helpers"""

import itertools
import typing


def list_1d_to_2d(data, columns):
    return [data[i : i + columns] for i in range(0, len(data), columns)]


class Coordinate:
    """Represent a single point within a 2D space."""

    x: int
    y: int

    def __init__(self, x, y) -> "Coordinate":
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        return (self.x << 16) ^ self.y

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

    @staticmethod
    def distance(p1: Coordinate, p2: Coordinate) -> int:
        """L1 (Manhattan) distance"""
        return abs(p1.x - p2.x) + abs(p1.y - p2.y)

    def transform(self, func) -> "Grid":
        data = [func(x) for x in self._data]
        return Grid(list_1d_to_2d(data, self.columns))


class SparseGrid:
    """A spare grid representation, only storing specific values and their coordinates."""

    def __init__(self, data=None, predicate=lambda x: True):
        """TODO: datatype of self._data"""
        self._data = {}

        if not data is None:
            self._stride = len(data[0])
            self.rows = len(data)
            self.columns = len(data[0])

            for r, row in enumerate(data):
                for c, ch in enumerate(row):
                    if predicate(ch):
                        index = c + self._stride * r
                        self._data[index] = ch

    def __iter__(self):
        return iter(self.keys())

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, index: int):
        return self._data[index]

    def __setitem__(self, index: int, value):
        self._data[index] = value

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def find(self, needle) -> int:
        for idx, v in self._data.items():
            if v == needle:
                return idx
        raise IndexError

    def find_all(self, needle) -> typing.Generator[int, None, None]:
        for idx, value in self._data.items():
            if value == needle:
                yield idx

    def get(self, index: int):
        return self._data[index]

    def set(self, index: int, value):
        self._data[index] = value

    def neighbours(
        self, index: int, include_diagonals=True
    ) -> typing.Generator[int, None, None]:
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        if include_diagonals:
            deltas += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        cx = index % self._stride
        cy = index // self._stride

        for delta in deltas:
            x = cx + delta[0]
            y = cy + delta[1]
            idx = x + self._stride * y
            if 0 <= x < self.rows and 0 <= y < self.columns and idx in self._data:
                yield idx
            else:
                continue

    def remove(self, index: int):
        if index in self._data:
            self._data.pop(index)


# class SparseGrid:
#     """A spare grid representation, only storing specific values and their coordinates."""

#     def __init__(self, data=None, predicate=lambda x: True):
#         """TODO: datatype of self._data"""
#         self._data = {}

#         if not data is None:
#             self._stride = len(data[0])
#             self.rows = len(data)
#             self.columns = len(data[0])

#             for r, row in enumerate(data):
#                 for c, ch in enumerate(row):
#                     if predicate(ch):
#                         index = c + self._stride * r
#                         self._data[index] = ch

#     def __iter__(self):
#         return iter(self.keys())

#     def __len__(self) -> int:
#         return len(self._data)

#     def __getitem__(self, coordinate: Coordinate):
#         index = coordinate.x + self._stride * coordinate.y
#         return self._data[index]

#     def __setitem__(self, coordinate: Coordinate, value):
#         index = coordinate.x + self._stride * coordinate.y
#         self._data[index] = value

#     def keys(self):
#         return [
#             Coordinate(idx % self._stride, idx // self._stride) for idx in self._data
#         ]

#     def values(self):
#         return self._data.values()

#     def find(self, needle) -> Coordinate:
#         for idx, v in self._data.items():
#             if v == needle:
#                 return Coordinate(idx % self._stride, idx // self._stride)
#         raise IndexError

#     def find_all(self, needle) -> typing.Generator["Coordinate", None, None]:
#         for idx, value in self._data.items():
#             if value == needle:
#                 yield Coordinate(idx % self._stride, idx // self._stride)

#     def get(self, coordinate: Coordinate):
#         return self._data[coordinate]

#     def set(self, coordinate: Coordinate, value):
#         self._data[coordinate] = value

#     def neighbours(
#         self, coordinate: Coordinate, include_diagonals=True
#     ) -> typing.Generator[Coordinate, None, None]:
#         deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
#         if include_diagonals:
#             deltas += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

#         for delta in deltas:
#             x = coordinate.x + delta[0]
#             y = coordinate.y + delta[1]
#             idx = x + self._stride * y
#             if 0 <= x < self.rows and 0 <= y < self.columns and idx in self._data:
#                 yield Coordinate(x, y)
#             else:
#                 continue

#     def remove(self, coordinate: Coordinate):
#         idx = coordinate.x + self._stride * coordinate.y
#         if idx in self._data:
#             self._data.pop(idx)
