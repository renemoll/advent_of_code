"""Day 13: Point of Incidence"""

import itertools


def _parse(input_lines: list[str]):
    patterns = "\n".join(input_lines).split("\n\n")
    return [p.splitlines() for p in patterns]


def transpose_2d_list(l):
    return list(map(list, zip(*l)))


def string_distance(a, b):
    return sum(0 if x == y else 1 for x, y in zip(a, b))


def find_mirror(pattern, target_diff=0):
    options = []
    row = 0
    for a, b in itertools.pairwise(pattern):
        row += 1
        if string_distance(a, b) <= target_diff:
            options.append(row)

    for option in options:
        length = min(option, len(pattern) - option)

        top = range(option - 1, option - length - 1, -1)
        bottom = range(option, option + length)
        distance = sum(
            string_distance(pattern[i1], pattern[i2]) for i1, i2 in zip(top, bottom)
        )
        if distance == target_diff:
            return option

    return 0


def _part1(parsed_input) -> int:
    result = 0
    for pattern in parsed_input:
        column = find_mirror(transpose_2d_list(pattern))
        row = find_mirror(pattern)
        result += row * 100 + column

    return result


def _part2(parsed_input) -> int:
    result = 0
    for pattern in parsed_input:
        column = find_mirror(transpose_2d_list(pattern), target_diff=1)
        row = find_mirror(pattern, target_diff=1)
        result += row * 100 + column

    return result


def solve(input_lines: list[str]) -> tuple[int, int]:
    parsed_input = _parse(input_lines)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=13)
    example = puzzle.examples[0]
    example_input = example.input_data.splitlines()

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
