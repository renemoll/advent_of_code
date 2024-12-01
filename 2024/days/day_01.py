"""Day 1: Historian Hysteria"""

import collections


def _parse(input_lines: list[str]):
    left = []
    right = []
    for line in input_lines:
        l, r = line.split()
        left.append(l)
        right.append(r)
    left = list(map(int, left))
    left.sort()
    right = list(map(int, right))
    right.sort()
    return left, right


def _part1(parsed_input) -> int:
    left, right = parsed_input
    return sum(map(lambda x: abs(x[0] - x[1]), zip(left, right)))


def _part2(parsed_input) -> int:
    left, right = parsed_input
    left_count = collections.Counter(left)
    right_count = collections.Counter(right)
    return sum(
        number * left_count[number] * right_count[number]
        for number in left_count.elements()
    )


def solve(input_lines: list[str]) -> tuple[int, int]:
    parsed_input = _parse(input_lines)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=1)
    example = puzzle.examples[0]
    example_input = example.input_data.splitlines()

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
