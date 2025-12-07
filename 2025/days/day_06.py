"""Day 6: Trash Compactor"""

import functools
import operator

from .utilities import transpose_2d_list


def _parse(input_data: str):
    return input_data


def _part1(input_data) -> int:
    parsed_input = transpose_2d_list([line.split() for line in input_data.splitlines()])
    result = 0
    for line in parsed_input:
        op = line[-1]
        values = map(int, line[0:-1])
        match op:
            case "*":
                result += functools.reduce(operator.mul, values, 1)
            case "+":
                result += sum(values)
    return result


def _part2(input_data) -> int:
    n = 4  # note: this only works for the example...
    parsed_input = transpose_2d_list(
        [
            [line[i : i + n - 1] for i in range(0, len(line), n)]
            for line in input_data.splitlines()
        ]
    )
    result = 0
    for line in parsed_input:
        op = line[-1].strip()
        cols = line[0:-1]
        values = ["".join(x) for x in zip(*cols)]
        match op:
            case "*":
                values = [int(v) if v.strip() != "" else 1 for v in values]
                result += functools.reduce(operator.mul, values, 1)
            case "+":
                values = [int(v) if v.strip() != "" else 0 for v in values]
                result += sum(values)
    return result


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2025, day=6)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
