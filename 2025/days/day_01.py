"""Day 1: Secret Entrance"""

import math


def _parse(input_data: str):
    rotations = [
        int(line[1:]) * (1 if line[0] == "R" else -1)
        for line in input_data.splitlines()
    ]
    return rotations


def circular_sum(data: list[int], initial: int, maximum: int) -> int:
    """Returns the number of times the sum ends up at 0."""
    result = 0
    position = initial
    for x in data:
        position = (position + x) % maximum
        result += 1 if position == 0 else 0
    return result


def _part1(parsed_input) -> int:
    return circular_sum(parsed_input, initial=50, maximum=100)


def count_zero_crossings(data: list[int], initial: int, maximum: int) -> int:
    """Returns the number of times 0 is crossed for each rotation in data."""
    result = 0
    position = initial
    for x in data:
        full_rotations = abs(x) // maximum
        partial_rotation = math.fmod(x, maximum)

        result += full_rotations

        # Note: using math.fmod to get (my) expected behavior with negatives :)
        next_position = position + partial_rotation
        if next_position >= maximum or (position > 0 and next_position <= 0):
            result += 1

        position = next_position % maximum

    return result


def _part2(parsed_input) -> int:
    return count_zero_crossings(parsed_input, initial=50, maximum=100)


def solve(input_data: str) -> tuple[int, int]:
    """Solve both parts of the puzzle."""
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2025, day=1)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
