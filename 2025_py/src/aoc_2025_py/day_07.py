"""Day 7: Laboratories

Part 1:
    Another grid traversal problem, now we need to find the number of paths through a map.

    This can be solved by traversing the grid and counting the times the path splits.

    First, parse the data into a grid, next find the starting point, and then follow the path. When we encounter
    a split, we record the split and traverse both options. Sounds like a breadth-first search algorithm to me.

Part 2:
    For part 2, we need to determine the total number of paths possible.

    We can:
     - try to find all possible paths by iterating through the grid;
     - track the number of paths to each point based on the points above it.

    Iterating through the grid may sound simpler but could be more computationally expensive as all variations need to
    be explored.

    In the end, I opted for the second approach, but was stuck too long due to attempting to reuse the Grid structure.
    It seemed simple enough to re-use, were it not that the iteration was not in order, causing issues when updating
    the path counts. Finally, I realized I did not need to retrain the Grid structure and could just update a single
    list (row) of path counts.
"""

from utilities_py import Grid, Coordinate


def _parse(input_data: str) -> Grid:
    return Grid(input_data.splitlines())


def _part1(grid: Grid) -> int:
    start = grid.find("S")

    seen = set()
    candidates = set()
    candidates.add(start + Coordinate(0, 1))
    split_count = 0

    while candidates:
        current = candidates.pop()

        try:
            options = []
            match grid[current]:
                case ".":
                    options.append(current + Coordinate(0, 1))
                case "^":
                    split_count += 1
                    options.append(current + Coordinate(1, 0))
                    options.append(current + Coordinate(-1, 0))

            seen.add(current)
            for option in options:
                if option not in seen:
                    candidates.add(option)

        except IndexError:
            continue

    return split_count


def _part2(grid: Grid) -> int:
    rows, columns = grid.size()
    paths = [0] * columns

    for row in range(rows):
        for i, val in enumerate(grid.row(row)):
            match val:
                case "S":
                    paths[i] = 1
                case "^":
                    paths[i - 1] += paths[i]
                    paths[i + 1] += paths[i]
                    paths[i] = 0

    return sum(paths)


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))
