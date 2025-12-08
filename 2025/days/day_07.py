"""Day 7: Laboratories

Part 1:
    Given a map of tachyon manifold, we need to find the number of times the tachyon beam is split.

    Lets parse the map into a grid, find the starting point, and then follow the beam. Sounds like
    a typical map traversal where we track candidates and processed points.

Part 2:
    Now we need to determine the number of paths a beam can take through the manifold.

    We can:
     - try to find all possible paths by iterating through the grid;
     - calculate the number of paths to each point based on the points above it.
    Iterating through the grid may sound simpler but could be more computationally expensive as all variations need to be explored.

    In the end I opted for the second approach, but was stuck too long due to attempting to reuse the Grid structure.
    It seemed simple enough to re-use, were it not that the iteration was not in order, causing issues when updating the path counts.
    Finally I realized I did not need to retrain the Grid structure and could just update a single list (row) of path counts.
"""

from .utilities import Grid, Coordinate


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
    paths = [0] * (grid.columns)

    for row in range(grid.rows):
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


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2025, day=7)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
