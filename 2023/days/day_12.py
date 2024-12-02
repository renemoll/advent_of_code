"""Day 12: Hot Springs"""

import functools


def _parse(input_data: str):
    parsed = []

    for line in input_data.splitlines():
        status, report = line.split(" ")
        report = tuple(map(int, report.split(",")))
        parsed.append((status, report))

    return parsed


@functools.cache
def pattern_match(pattern, counts):
    # Thanks to: https://advent-of-code.xavd.id/writeups/2023/day/12/
    if not pattern:
        return 1 if len(counts) == 0 else 0

    if not counts:
        return 1 if "#" not in pattern else 0

    current = pattern[0]
    if current == ".":
        return pattern_match(pattern[1:], counts)

    if current == "#":
        group_size = counts[0]
        if (
            # long enough
            len(pattern) >= group_size
            and
            # valid_chars
            all(c != "." for c in pattern[:group_size])
            and
            # pattern_size
            (len(pattern) == group_size or pattern[group_size] != "#")
        ):
            return pattern_match(pattern[group_size + 1 :], counts[1:])

    if current == "?":
        return pattern_match(f"#{pattern[1:]}", counts) + pattern_match(
            f".{pattern[1:]}", counts
        )

    return 0


def _part1(parsed_input) -> int:
    return sum(pattern_match(status, report) for status, report in parsed_input)


def _part2(parsed_input) -> int:
    result = 0

    for line in parsed_input:
        status, report = line
        status = "?".join(5 * [status])
        report = 5 * report
        result += pattern_match(status, report)

    return result


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=12)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
