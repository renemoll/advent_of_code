"""Day 14: Parabolic Reflector Dish"""

import collections
import pprint


def transpose_2d_list(l):
    return list(map(list, zip(*l)))


def _parse(input_data: str):
    transposed = transpose_2d_list(input_data.splitlines())
    return transposed


def _part1(parsed_input) -> int:
    result = 0
    max_score = len(parsed_input[0])
    for column in parsed_input:
        sections = "".join(column).split("#")
        offset = 0
        for section in sections:
            count = collections.Counter(section)
            if "O" in count:
                base = max_score - offset
                result += sum(range(base, base - count["O"], -1))
            offset += len(section) + 1

    return result


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
