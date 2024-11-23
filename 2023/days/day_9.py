"""Day 9: Mirage Maintenance"""

import itertools


class Sequence:
    """Represents a single measurement sequence."""

    values: list[int]

    def __init__(self, values: list[int]) -> None:
        self.values = values

    def __repr__(self) -> str:
        return f"<Sequence values: {self.values}>"

    def diff(self) -> "Sequence":
        result = [b - a for a, b in itertools.pairwise(self.values)]
        return Sequence(result)

    def all_zero(self) -> bool:
        if len(self.values) == 0:
            return True

        return not any(x > 0 or x < 0 for x in self.values)


def _parse(input_lines: list[str]) -> list:
    return [Sequence(list(map(int, line.split()))) for line in input_lines]


def _process_forwards(sequence: Sequence) -> int:
    if sequence.all_zero():
        return 0

    diff = sequence.diff()
    return sequence.values[-1] + _process_forwards(diff)


def _part1(parsed_data: list[Sequence]) -> int:
    return sum(_process_forwards(sequence) for sequence in parsed_data)


def _process_backwards(sequence: Sequence) -> int:
    if sequence.all_zero():
        return 0

    diff = sequence.diff()
    return sequence.values[0] - _process_backwards(diff)


def _part2(parsed_data: list) -> int:
    return sum(_process_backwards(sequence) for sequence in parsed_data)


def solve(input_lines: list[str]) -> tuple[int, int]:
    parsed_input = _parse(input_lines)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=9)
    example = puzzle.examples[0]
    example_input = example.input_data.splitlines()

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
