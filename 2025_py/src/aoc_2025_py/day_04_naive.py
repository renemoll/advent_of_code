"""Day 4: Printing Department

Part 1:
    The goal is to find the number of grid items that have less than 4 adjacent items.

    Sounds like the first grid problem for this year. I will parse the input into a sparse grid, which means the grid
    only stores the items present on the grid. Next, for each item in the grid: check if it has less than 4 adjacent items.
    This means determining the number of neighbours (including diagonals).

Part 2:
    For part 2 we actually remove items, and keep removing items, until there are no more items that have less than 4
    adjacent items. This means looping over the grid a few times, using the same logic as in part 1, until there are no
    more items to remove.
"""

from utilities_py import SparseMatrix


def _parse(input_data: str):
    return SparseMatrix("".join(input_data).splitlines(), predicate=lambda x: x == "@")


def _part1(grid) -> int:
    max_rolls = 4
    return sum(
        [1 if len(list(grid.neighbours(roll))) < max_rolls else 0 for roll in grid]
    )


def _part2(grid) -> int:
    max_rolls = 4
    result = 0

    while True:
        to_be_removed = [
            roll for roll in grid if len(list(grid.neighbours(roll))) < max_rolls
        ]
        if not to_be_removed:
            break

        result += len(to_be_removed)
        for roll in to_be_removed:
            grid.remove(roll)

    return result


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))
