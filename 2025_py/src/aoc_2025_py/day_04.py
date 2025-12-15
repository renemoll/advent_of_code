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

Improvements:
    * Store the number of adjacent items for each item and update it as items are removed.
      While it adds some additional administration, it reduces the times determining the number of neighbours.

    * Instead of checking all items in each iteration, we could keep track of items that were adjacent to removed items
      and only check those in the next iteration. This should reduce the number of items to look up in each iteration.

Discarded alternative solutions:
    * Perform a convolution over the grid with a 3x3 kernel to count the adjacent items in one go.
    I doubt this will be faster, as you still need to loop over the entire grid multiple times and access all
    available neighbours.
"""

from utilities_py import SparseMatrix


def _parse(input_data: str):
    grid = SparseMatrix("".join(input_data).splitlines(), predicate=lambda x: x == "@")
    for roll in grid:
        grid[roll] = len(list(grid.neighbours(roll)))
    return grid


def _part1(grid: SparseMatrix) -> int:
    max_rolls = 4
    return sum(
        [1 if len(list(grid.neighbours(roll))) < max_rolls else 0 for roll in grid]
    )


def _part2(grid) -> int:
    max_rolls = 4
    result = 0

    candidates = grid.keys()

    while True:
        to_be_removed = [roll for roll in candidates if grid[roll] < max_rolls]
        if not to_be_removed:
            break

        result += len(to_be_removed)

        candidates = set()
        for roll in to_be_removed:
            for neighbour in grid.neighbours(roll):
                candidates.add(neighbour)
                grid[neighbour] -= 1

            grid.remove(roll)
            candidates.discard(roll)

    return result


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))
