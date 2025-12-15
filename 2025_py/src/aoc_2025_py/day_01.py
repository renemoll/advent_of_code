"""Day 1: Secret Entrance

Part 1:
    The goal is to find the number of times the rotation ends up at 0.

    This sounds easy enough: generate a cumulative sum for each rotation while ensuring to wrap around at 100, and
    count the number of times we hit 0. I want to use a functional programming approach for this as I think it shows
    the intent clearly. So I generate a stream of sums, transform that into a stream of ones and zero to represent
    zero positions and finally sum that.

Part 2:
    For part 2 we need to count the number of times 0 is crossed.

    Now, we need to determine the number of zero crossings for each rotation, noting that a single rotation can cross
    zero multiple times. The naive way is to simulate each step of the rotation.

Improvements:
    - Instead of simulating each step, calculate the number of full rotations and partial rotations to determine the
      number of zero crossings. The only tricky part is here is the behaviour of the modulo operator with negative
      numbers in Python.
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
    position = 50
    for x in data:
        position = (position + x) % maximum
        yield position


def _part1(parsed_input) -> int:
    rotation = range_limited_sum(parsed_input)
    return sum(map(lambda x: 1 if x == 0 else 0, rotation))


def range_limited_sum_with_crossings(data: list[int]) -> Iterator[int]:
    """Yields the number of times 0 is crossed for each rotation in data."""
    maximum = 100
    position = 50
    for x in data:
        full_rotations = abs(x) // maximum
        partial_rotation = math.fmod(x, maximum)

        result = full_rotations

        # Note: using math.fmod to get (my) expected behaviour with negatives :)
        next_position = position + partial_rotation
        if next_position >= maximum or (position > 0 and next_position <= 0):
            result += 1

        position = next_position % maximum

        yield result


def _part2(parsed_input) -> int:
    rotation = range_limited_sum_with_crossings(parsed_input)
    return sum(rotation)


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))
