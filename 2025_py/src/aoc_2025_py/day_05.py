"""Day 5: Cafeteria

Part 1:
    Our goal is to determine how many produce items are still fresh, based on if their ID is in a list of ranges.

    A simple solution is to generate a list of ranges and check each ID against them, stopping at the first hit.
    This could be improved by combining overlapping ranges first.

Part 2:
    And here we are needing to determine the number of unique produce items in the ranges.

    This can be done by generating a set of all IDs in the ranges, but I assume the amount of IDs is too large for
    decent speed/memory. So we need to reduce the number of ranges to non-overlapping ranges, and then sum their
    lengths.

Improvements:
    * Merged the ranges before processing for both parts.
"""

from utilities_py import merge_overlapping_ranges


def _parse(input_data: str):
    ranges, produce = input_data.split("\n\n")

    # Note: end + 1 to make ranges inclusive
    ranges = [
        range(int(start), int(end) + 1)
        for line in ranges.splitlines()
        for start, end in (line.split("-"),)
    ]
    produce = [int(line) for line in produce.splitlines()]

    return merge_overlapping_ranges(ranges), produce


def _part1(parsed_input) -> int:
    ranges, produce = parsed_input
    return sum(1 for item in produce if any(item in r for r in ranges))


def _part2(parsed_input) -> int:
    ranges, _ = parsed_input
    return sum(r.stop - r.start for r in ranges)


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))
