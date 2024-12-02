"""Day 14: Parabolic Reflector Dish"""

import pprint


def _parse(input_data: str):
    pprint.pprint(input_data)
    return []


def _part1(parsed_input) -> int:
    pprint.pprint(parsed_input)
    return 0


def _part2(parsed_input) -> int:
    pprint.pprint(parsed_input)
    return 0


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=14)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
