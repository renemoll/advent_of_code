"""Day 19: Linen Layout"""

import functools


def _parse(input_data: str):
    sections = input_data.split("\n\n")
    available = [x.strip() for x in sections[0].split(",")]
    desired = sections[1].splitlines()
    return available, desired


def is_design_possible(design: str, patterns: list[str]) -> bool:
    @functools.cache
    def is_possible(design) -> bool:
        return (
            1
            if len(design) == 0
            else sum(
                is_possible(design[len(p) :]) for p in patterns if design.startswith(p)
            )
        )

    return is_possible(design)


def _part1(parsed_input) -> int:
    available, desired = parsed_input
    return sum(1 for item in desired if is_design_possible(item, available))


def _part2(parsed_input) -> int:
    available, desired = parsed_input
    return sum(is_design_possible(item, available) for item in desired)


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=19)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
