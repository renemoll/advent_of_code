"""Day 1: Historian Hysteria"""

import math
from .utilities import diff


def _parse(input_lines: list[str]):
    return [list(map(int, line.split())) for line in input_lines]


def report_is_valid(report):
    dxs = diff(report)
    signs = [math.copysign(1, x) for x in dxs]
    if abs(sum(signs)) != len(dxs):
        return False
    if all(abs(x) > 0 and abs(x) < 4 for x in dxs):
        return True
    return False


def _part1(parsed_input) -> int:
    return sum(report_is_valid(x) for x in parsed_input)


def _part2(parsed_input) -> int:
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


def solve(input_lines: list[str]) -> tuple[int, int]:
    parsed_input = _parse(input_lines)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=2)
    example = puzzle.examples[0]
    example_input = example.input_data.splitlines()

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
