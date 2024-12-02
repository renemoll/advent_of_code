"""Day 2: Red-Nosed Reports"""

import math
from .utilities import diff, parse_ints


def report_is_valid(report: list[int]) -> bool:
    dxs = diff(report)
    signs = map(lambda x: math.copysign(1, x), dxs)
    if abs(sum(signs)) == len(dxs) and all(0 < abs(x) < 4 for x in dxs):
        return True
    return False


def _parse(input_data: str) -> list[list[int]]:
    return [parse_ints(line) for line in input_data.splitlines()]


def _part1(parsed_input: list[list[int]]) -> int:
    return sum(report_is_valid(x) for x in parsed_input)


def _part2(parsed_input: list[list[int]]) -> int:
    result = 0
    for report in parsed_input:
        if report_is_valid(report):
            result += 1
            continue

        for i in range(len(report)):
            if report_is_valid(report[:i] + report[i + 1 :]):
                result += 1
                break

    return result


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=2)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
