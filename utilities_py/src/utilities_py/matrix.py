"""Matrix and related utilities."""

import itertools
from collections.abc import Callable, Generator
import typing

T = typing.TypeVar("T")
U = typing.TypeVar("U")


def list_1d_to_2d(data: typing.Sequence[T], stride: int) -> typing.List[typing.List[T]]:
    """Convert a 1D list into a 2D list with given stride.

    Args:
        data (typing.Sequence[T]): The 1D list to convert.
        stride (int): The number of elements per sublist (row).

    Returns:
        typing.List[typing.List[T]]: The resulting 2D list.
    """

    return [data[i : i + stride] for i in range(0, len(data), stride)]


def transpose_2d_list(
    data: typing.Sequence[typing.Sequence[T]],
) -> typing.List[typing.List[T]]:
    """Transpose a 2D list.

    Args:
        l (typing.Sequence[typing.Sequence[T]]): The 2D list to transpose.

    Returns:
        typing.List[typing.List[T]]: The transposed 2D list.

    TODO:
     - transpose for lists, Matrix, SparseMatrix?
    """

    return list(map(list, zip(*data)))


class Matrix(typing.Generic[T]):
    """A 2D matrix.

    Improvements:
    * factory functions to create the matrix (from string, from custom type)
    """

    def __init__(self, data: typing.Sequence[typing.Sequence[T]]) -> None:
        self._data = list(itertools.chain.from_iterable(data))
        self._stride = len(data[0])

        self._rows = len(data)
        self._columns = self._stride

    def __eq__(self, other: typing.Self) -> bool:
        return (
            self._rows == other._rows
            and self._columns == other._columns
            and self._data == other._data
        )

    def __repr__(self) -> str:
        return f"<Matrix rows: {self._rows}, columns: {self._columns}>"

    def __str__(self) -> str:
        return "\n".join(
            " ".join(map(str, row)) for row in list_1d_to_2d(self._data, self._stride)
        )

    def row(self, index: int) -> typing.List[T]:
        """Get a specific row.

        Args:
            index (int): The row index to retrieve.

        Returns:
            typing.List[T]: The requested row as a list.

        TODO: remove?
        """

        start = index * self._stride
        end = start + self._stride
        return self._data[start:end]

    def column(self, index: int) -> typing.List[T]:
        """Get a specific column.

        Args:
            index (int): The column index to retrieve.

        Returns:
            typing.List[T]: The requested column as a list.

        TODO: remove?
        """

        return [self._data[i * self._stride + index] for i in range(self._rows)]

    def gaussian_elimination(self) -> typing.Self:
        """Perform Gauss-Jordan elimination on the matrix in place.

        Args:
            None

        Returns:
            typing.Self: The matrix after Gauss-Jordan elimination.

        This method modifies the matrix to its reduced row echelon form.

        Beware: this is a simple implementation and does not handle all edge cases.
        Note: the resulting matrix may contain floating-point numbers.
        """

        for i in range(min(self._rows, self._columns)):
            # Scale the row
            diagonal_value = self._data[i * self._stride + i]
            if diagonal_value == 0:
                continue  # Cannot scale a zero row
            for c in range(i, self._columns):
                self._data[i * self._stride + c] /= diagonal_value

            # Eliminate below
            for r in range(i + 1, self._rows):
                factor = self._data[r * self._stride + i]
                for c in range(i, self._columns):
                    self._data[r * self._stride + c] -= (
                        factor * self._data[i * self._stride + c]
                    )

            # Eliminate above
            for j in range(i):
                factor = self._data[j * self._stride + i]
                for c in range(i, self._columns):
                    self._data[j * self._stride + c] -= (
                        factor * self._data[i * self._stride + c]
                    )

        return self

    def transform(self, func: Callable[[int], int]) -> typing.Self:
        """Apply a function to each element in the Matrix.

        Args:
            func (Callable[[int], int]): The function to apply to each element.

        Returns:
            typing.Self: The transformed Matrix.
        """
        self._data = [func(x) for x in self._data]
        return self


class SparseMatrix(typing.Generic[T]):
    """A spare 2D matrix representation, only storing specific values and their index."""

    __slots__ = ("_data", "_stride", "_rows", "_columns")

    _data: typing.Dict[int, T]
    _stride: int
    _rows: int
    _columns: int

    def __init__(
        self,
        data: typing.Sequence[typing.Sequence[T]] = None,
        predicate: typing.Callable[[T], bool] = lambda x: True,
    ) -> None:
        self._data = {}
        self._stride = len(data[0])

        self._rows = len(data)
        self._columns = self._stride

        for r, row in enumerate(data):
            for c, ch in enumerate(row):
                if predicate(ch):
                    index = c + self._stride * r
                    self._data[index] = ch

    def __iter__(self) -> typing.Iterator[int]:
        return iter(self.keys())

    # def __len__(self) -> int:
    #     return len(self._data)

    def __getitem__(self, index: int) -> T:
        return self._data[index]

    def __setitem__(self, index: int, value: T) -> None:
        self._data[index] = value

    def keys(self) -> typing.KeysView[int]:
        return self._data.keys()

    # def values(self):
    #     return self._data.values()

    def find(self, needle) -> int:
        for idx, v in self._data.items():
            if v == needle:
                return idx
        raise KeyError

    # def find_all(self, needle) -> typing.Generator[int, None, None]:
    #     for idx, value in self._data.items():
    #         if value == needle:
    #             yield idx

    # def get(self, index: int):
    #     return self._data[index]

    # def set(self, index: int, value):
    #     self._data[index] = value

    def neighbours(
        self, index: int, include_diagonals=True
    ) -> Generator[int, None, None]:
        """Generate neighbour indices for a given index in the sparse matrix.

        Args:
            index (int): The index in the sparse matrix to find neighbours for.
            include_diagonals (bool, optional): Whether to include diagonal neighbours. Defaults to True.

        Yields:
            int: Indices of neighbouring elements in the sparse matrix.
        """

        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        if include_diagonals:
            deltas += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        cx = index % self._stride
        cy = index // self._stride

        for delta in deltas:
            x = cx + delta[0]
            y = cy + delta[1]
            idx = x + self._stride * y
            if idx in self._data.keys():
                yield idx
            else:
                continue

    def remove(self, index: int) -> None:
        """TODO: add del operation"""
        if index in self._data:
            self._data.pop(index)
