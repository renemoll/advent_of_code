"""Day 1: Secret Entrance

Part 1:
    The goal is to find the number of times the sum ends up at 0.

    This sounds easy enough, perform a cumulative sum, wrapping around at 100, and count the number of times we hit 0.
    I want to use a functional programming approach for this as I think it shows the intent clearly. So I generate the sum into a stream, transforms that into a stream indicating a zero position and finally sum that stream.

Part 2:
    For part 2 we need to count the number of times 0 is crossed.

    Now we need to determine zero crossings for each rotation in data, noting that a single instruction can cross zero multiple times.
    The naive way is to simulate each step of the rotation.
"""

from collections.abc import Iterator
import math


def _parse(input_data: str):
    rotations = [
        int(line[1:]) * (1 if line[0] == "R" else -1)
        for line in input_data.splitlines()
    ]
    return rotations


def range_limited_sum(data: list[int]) -> Iterator[int]:
    """Yields the cumulative sum of data, wrapped around at 100."""
    maximum = 100
    result = 50
    for x in data:
        result = (result + x) % maximum
        yield result


def _part1(parsed_input) -> int:
    rotation = range_limited_sum(parsed_input)
    return sum(map(lambda x: 1 if x == 0 else 0, rotation))


def range_limited_sum_with_crossings(data: list[int]) -> Iterator[int]:
    """Yields the number of times 0 is crossed for each rotation in data."""
    maximum = 100
    result = 50
    for x in data:
        crossings = 0
        for _ in range(abs(x)):
            s = math.copysign(1, x)
            result = (result + s) % maximum
            crossings += 1 if result == 0 else 0
        yield crossings


def _part2(parsed_input) -> int:
    rotation = range_limited_sum_with_crossings(parsed_input)
    return sum(rotation)


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
