"""Coordinates and positions related utilities."""

import itertools
import typing


class Coordinate:
    """Represent a single point within a 2D space.

    This can be seen as a 2D vector, position or coordinate on a grid, depending on the application.

    Attributes:
        x (int): The x coordinate.
        y (int): The y coordinate.
    """

    __slots__ = ("x", "y")

    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"<Coordinate x: {self.x}, y: {self.y}>"

    def __add__(self, other: typing.Self) -> typing.Self:
        return Coordinate(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: typing.Self) -> typing.Self:
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: typing.Self) -> typing.Self:
        return Coordinate(self.x - other.x, self.y - other.y)

    def __isub__(self, other: typing.Self) -> typing.Self:
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other: int) -> typing.Self:
        return Coordinate(self.x * other, self.y * other)

    def __imul__(self, other: int) -> typing.Self:
        self.x *= other
        self.y *= other
        return self

    def __rmul__(self, other: int) -> typing.Self:
        return Coordinate(self.x * other, self.y * other)

    def __eq__(self, other: typing.Self) -> bool:
        if isinstance(other, Coordinate):
            return self.x == other.x and self.y == other.y
        if isinstance(other, tuple) and len(other) == 2:
            a, b = other
            return self.x == a and self.y == b
        raise NotImplementedError

    def __lt__(self, other: typing.Self) -> bool:
        return (self.x, self.y) < (other.x, other.y)


def generate_neighbours(
    c: Coordinate, include_diagonals=True
) -> typing.Generator[Coordinate, None, None]:
    """Generate all neighbouring Coordinates around a given Coordinate.

    Args:
        c (Coordinate): The central Coordinate.
        include_diagonals (bool): Whether to include diagonal neighbours. Defaults to True.

    Yields:
        Coordinate: Each neighbouring Coordinate.
    """

    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    if include_diagonals:
        deltas += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for delta in deltas:
        yield Coordinate(c.x + delta[0], c.y + delta[1])


T = typing.TypeVar("T")


class Grid(typing.Generic[T]):
    """Represent a 2D grid.

    Improvements:
    * factory functions to create the matrix (from string, from custom type)
    """

    __slots__ = ("_data", "_stride", "_rows", "_columns")

    _data: typing.List[T]
    _stride: int
    _rows: int
    _columns: int

    def __init__(self, data: typing.Sequence[typing.Sequence[T]]) -> None:
        if isinstance(data[0], str):
            raw = [list(x) for x in data]
        else:
            raw = data

        self._data = list(itertools.chain.from_iterable(raw))
        self._stride = len(data[0])

        self._rows = len(data)
        self._columns = self._stride

    # def __iter__(self):
    #     return iter(self._data)

    # def __repr__(self) -> str:
    #     return f"<Matrix rows: {self.rows}, columns: {self.columns}>"

    # def __str__(self) -> str:
    #     return "\n".join(
    #         " ".join(map(str, row)) for row in list_1d_to_2d(self._data, self.columns)
    #     )

    def __getitem__(self, coordinate: Coordinate) -> T:
        index = coordinate.x + self._stride * coordinate.y
        return self._data[index]

    def __setitem__(self, coordinate: Coordinate, value: T) -> None:
        index = coordinate.x + self._stride * coordinate.y
        self._data[index] = value

    def size(self) -> typing.Tuple[int, int]:
        """Return the size of the grid as (rows, columns)."""
        return (self._rows, self._columns)

    def find(self, needle: T) -> Coordinate:
        index = self._data.index(needle)
        x = index % self._stride
        y = index // self._stride
        return Coordinate(x, y)

    # def find_all(self, needle) -> typing.Generator[typing.Self, None, None]:
    #     indices = [i for i, x in enumerate(self._data) if x == needle]
    #     for i in indices:
    #         yield Coordinate(i % self._stride, i // self._stride)

    def neighbours(
        self, c: Coordinate, include_diagonals=True
    ) -> typing.Generator[Coordinate, None, None]:
        """Generate all valid neighbouring Coordinates around a given Coordinate within the grid.

        Args:
            c (Coordinate): The central Coordinate.
            include_diagonals (bool): Whether to include diagonal neighbours. Defaults to True.

        Yields:
            Coordinate: Each neighbouring Coordinate within the grid bounds.
        """

        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        if include_diagonals:
            deltas += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for delta in deltas:
            x = c.x + delta[0]
            y = c.y + delta[1]
            if 0 <= x < self._columns and 0 <= y < self._rows:
                yield Coordinate(x, y)
            else:
                continue

    # # def all_coordinates(self) -> typing.Generator[Coordinate, None, None]:
    # #     for r in range(self.rows):
    # #         for c in range(self.columns):
    # #             yield Coordinate(r, c)

    # @staticmethod
    # def distance(p1: Coordinate, p2: Coordinate) -> int:
    #     """L1 (Manhattan) distance"""
    #     return abs(p1.x - p2.x) + abs(p1.y - p2.y)

    # def transform(self, func) -> "Grid":
    #     data = [func(x) for x in self._data]
    #     return Grid(list_1d_to_2d(data, self.columns))

    def row(self, row_index: int) -> typing.List[T]:
        """TODO: remove"""
        start = row_index * self._stride
        end = start + self._stride
        return self._data[start:end]

    # # def rows(self) -> typing.Generator[list, None, None]:
    # #     for r in range(self.rows):
    # #         yield self.row(r)
