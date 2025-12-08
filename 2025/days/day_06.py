"""Day 6: Trash Compactor

Part 1:
    We need to do some calculations on columns of data given an operator at the end.

    An easy solution is to transpose the data, then process each row accordingly.

Part 2:

"""

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
    lines = input_data.splitlines()

    # Extract the numbers into individual digits (reserved), each row representing a number
    numbers = lines[:-1]
    digit_lines = transpose_2d_list([line[::-1] for line in numbers])
    # And then merging the digits back into numbers
    values = ["".join(line).strip() for line in digit_lines]

    operations = lines[-1][::-1].split()

    def slice_by_empty_string(values):
        result = []
        for value in values:
            if len(value) > 0:
                result.append(int(value))
            else:
                yield result
                result = []

        yield result

    result = 0
    for sliced_values in slice_by_empty_string(values):
        op = operations.pop(0)
        match op:
            case "*":
                result += functools.reduce(operator.mul, sliced_values, 1)
            case "+":
                result += sum(sliced_values)

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
