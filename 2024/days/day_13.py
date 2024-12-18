"""Day 13: Claw Contraption"""

import itertools

from .utilities import parse_ints, take_n, transpose_2d_list, Coordinate


class Machine:
    """Represents a craw machine."""

    a: Coordinate
    b: Coordinate
    prize: Coordinate

    def __init__(self, a: Coordinate, b: Coordinate, prize: Coordinate):
        self.a = a
        self.b = b
        self.prize = prize

    def __repr__(self) -> str:
        return f"<Machine A: {self.a}, B: {self.b}, prize: {self.prize}>"


class Matrix:
    """TODO: simplify data import..."""

    def __init__(self, data: list[list[float]]):
        """Input: list of lists, where each inner list represents a row"""
        self._data = list(itertools.chain.from_iterable(data))
        self.rows = len(data)
        self.columns = len(data[0])

    def get(self, row, column) -> float:
        index = row * self.columns + column
        return self._data[index]


def determinant(matrix: Matrix):
    if matrix.rows != matrix.columns:
        raise ValueError
    if matrix.rows > 2:
        # For now 2x2 is enough
        raise ValueError

    positive = 1
    negative = 1
    for x in range(matrix.rows):
        positive *= matrix.get(x, x)
        negative *= matrix.get(matrix.rows - x - 1, x)

    return positive - negative


def _parse(input_data: str) -> list[Machine]:
    result = []
    for x in take_n(parse_ints(input_data), 6):
        result.append(Machine([x[0], x[1]], [x[2], x[3]], [x[4], x[5]]))
    return result


def _part1(parsed_input) -> int:
    result = 0
    for machine in parsed_input:
        div = determinant(Matrix(transpose_2d_list([machine.a, machine.b])))
        a = determinant(Matrix(transpose_2d_list([machine.prize, machine.b]))) / div
        b = determinant(Matrix(transpose_2d_list([machine.a, machine.prize]))) / div
        if a.is_integer() and b.is_integer():
            tokens = 3 * int(a) + int(b)
            result += tokens

    return result


def _part2(parsed_input) -> int:
    result = 0
    offset = 10000000000000
    for machine in parsed_input:
        machine.prize = [offset + x for x in machine.prize]

        div = determinant(Matrix(transpose_2d_list([machine.a, machine.b])))
        a = determinant(Matrix(transpose_2d_list([machine.prize, machine.b]))) / div
        b = determinant(Matrix(transpose_2d_list([machine.a, machine.prize]))) / div
        if a.is_integer() and b.is_integer():
            tokens = 3 * int(a) + int(b)
            result += tokens

    return result


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=13)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
