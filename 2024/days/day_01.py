"""Day 1: Historian Hysteria"""

import collections
from .utilities import parse_ints


def _parse(input_data: str) -> tuple[tuple[int], tuple[int]]:
    left, right = zip(*[parse_ints(line) for line in input_data.splitlines()])
    return (sorted(left), sorted(right))


def _part1(parsed_input: tuple[tuple[int], tuple[int]]) -> int:
    left, right = parsed_input
    return sum(map(lambda x: abs(x[0] - x[1]), zip(left, right)))


def _part2(parsed_input: tuple[tuple[int], tuple[int]]) -> int:
    left, right = parsed_input
    left_count = collections.Counter(left)
    right_count = collections.Counter(right)
    return sum(
        number * left_count[number] * right_count[number]
        for number in left_count.elements()
    )


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=1)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
