"""Day 25: Code Chronicle"""

from .utilities import transpose_2d_list


def _parse(input_data: str):
    sections = input_data.split("\n\n")

    locks = []
    keys = []
    for section in sections:
        lines = section.splitlines()
        imprint = transpose_2d_list(lines[1:-1])
        heights = [x.count("#") for x in imprint]

        if lines[0].count("#") == len(lines[0]):
            locks.append(heights)
        else:
            keys.append(heights)

    return (locks, keys)


def _part1(parsed_input) -> int:
    locks, keys = parsed_input

    options = 0
    for lock in locks:
        for key in keys:
            pins = [sum(x) for x in zip(lock, key)]
            if all(x <= 5 for x in set(pins)):
                options += 1

    return options


def _part2(parsed_input) -> int:
    _ = parsed_input
    return 0


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=25)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
