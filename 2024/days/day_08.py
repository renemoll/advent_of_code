"""Day 8: Resonant Collinearity"""

import itertools
import math

from .utilities import SparseGrid, Coordinate, clamp


def position_on_grid(grid: SparseGrid, position: Coordinate):
    return 0 <= position.x < grid.columns and 0 <= position.y < grid.rows


def _parse(input_data: str) -> SparseGrid:
    return SparseGrid(input_data.splitlines(), lambda x: x != ".")


def _part1(grid: SparseGrid) -> int:
    antennas = set(grid.values())
    options = set()
    for antenna in antennas:
        positions = list(grid.find_all(antenna))
        for x, y in itertools.combinations(positions, 2):
            delta = y - x
            options.add(x - delta)
            options.add(y + delta)

    options = [x for x in options if position_on_grid(grid, x) and x not in antennas]

    return len(options)


def _part2(grid: SparseGrid) -> int:
    antennas = set(grid.values())
    options = set()
    for antenna in antennas:
        positions = list(grid.find_all(antenna))
        for p1, p2 in itertools.combinations(positions, 2):
            delta = p2 - p1

            m = delta.y / delta.x
            b = p1.y - (m * p1.x)
            x_min = p1.x - int(
                math.floor(math.fabs(p1.x / delta.x)) * math.fabs(delta.x)
            )
            if delta.x > 0:
                x_max = clamp(math.floor((grid.columns - b) / m), 0, grid.columns)
            else:
                x_max = clamp(math.ceil(-b / m), 0, grid.columns)

            for x in range(x_min, x_max + 1, int(math.fabs(delta.x))):
                option = Coordinate(x, int(round(x * m + b, 0)))
                if not position_on_grid(grid, option):
                    continue
                options.add(option)

    return len(options)


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=8)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
