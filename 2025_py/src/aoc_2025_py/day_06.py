"""Day 6: Trash Compactor

Part 1:
    We need to do some sort of calculation on columns of data given an operator on the last line.

    An easy solution is to read the data into a matrix, transpose said matrix, and then process each row accordingly.

Part 2:
    Next we need to read the input data in a specific way, from right to left while taking empty spaces ito account
    as zeros.

    Again, transposing the data but now first reading it in reverse order.
"""

import functools
import operator

from utilities_py import transpose_2d_list


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
