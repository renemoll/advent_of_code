"""Day 4: Printing Department

Part 1:
    The goal is to find the number of paper rolls that have less than 4 adjacent rolls. This sounds like the first grid problem for this year.
    I will represent in the input as a 2D array (the grid). Next, for each roll in the grid check if its neighbours (including diagonals) also contain a paper roll and how many adjacent rolls there are.
    If there are less than 4 adjacent rolls, the roll can be marked for removal.

Part 2:
    For part 2 we actually need to remove rolls that have less than 4 adjacent rolls until no more rolls can be removed.
    This means we can loop over the grid a few times, using the same logic as in part 1. This will be slow....
"""

from .utilities import SparseGrid


def _parse(input_data: str):
    return SparseGrid("".join(input_data).splitlines(), predicate=lambda x: x == "@")


def _part1(grid) -> int:
    max_rolls = 4
    result = 0

    for roll in grid:
        adjacent_rolls = len(list(grid.neighbours(roll)))
        if adjacent_rolls < max_rolls:
            result += 1
    return result


def _part2(grid) -> int:
    max_rolls = 4
    result = 0

    while True:
        to_be_removed = []
        for roll in grid:
            adjacent_rolls = len(list(grid.neighbours(roll)))
            if adjacent_rolls < max_rolls:
                to_be_removed.append(roll)

        result += len(to_be_removed)
        if not to_be_removed:
            break

        for roll in to_be_removed:
            grid.remove(roll)

    return result


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2025, day=4)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
