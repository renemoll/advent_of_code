"""Day 2: Cube Conundrum"""

import collections
import re


def _part1(input_data: str) -> int:
    limit = {"red": 12, "green": 13, "blue": 14}
    result = 0
    for i, line in enumerate(input_data.splitlines(), 1):
        _, sets = line.split(":")
        if all(
            int(amount) < limit[colour]
            for amount, colour in re.findall(r"(\d+) (\w+)", sets)
        ):
            result += i
    return result


def _part2(input_data: str) -> int:
    result = 0
    for line in input_data.splitlines():
        _, sets = line.split(":")
        fewest = collections.defaultdict(int)
        for amount, colour in re.findall(r"(\d+) (\w+)", sets):
            fewest[colour] = max(fewest[colour], int(amount))

        result += fewest["red"] * fewest["green"] * fewest["blue"]
    return result


def solve(input_data: str) -> tuple[int, int]:
    return (_part1(input_data), _part2(input_data))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=2)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
