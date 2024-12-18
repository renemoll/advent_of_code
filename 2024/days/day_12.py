"""Day 12: Garden Groups"""

import copy
import itertools

from .utilities import SparseGrid, Coordinate


def count_corners(grid: SparseGrid, current_pos: Coordinate, area: int) -> int:
    field = grid.get(current_pos)
    options = [
        x
        for x in grid.neighbours(current_pos, include_diagonals=False)
        if grid.get(x) == field
    ]

    corners = 0

    if len(options) == 0 and area == 1:
        corners += 4
    elif len(options) == 1:
        corners += 2
    elif len(options) == 2:
        dc = [x - current_pos for x in options]
        delta = dc[0] + dc[1]
        if delta != Coordinate(0, 0):
            # two options are not in line, so at least one corner...
            if grid.get(current_pos + delta) != field:
                # inside is a different field, so 2 corners
                corners += 2
            else:
                corners += 1
    elif len(options) >= 3:
        dc = [x - current_pos for x in options]
        for d1, d2 in itertools.combinations(dc, 2):
            delta = d1 + d2
            if delta == Coordinate(0, 0):
                continue
            if grid.get(current_pos + delta) != field:
                corners += 1

    return corners


def _parse(input_data: str):
    return SparseGrid(input_data.splitlines())


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    grid = copy.deepcopy(parsed_input)
    statistics = []

    while len(grid) > 0:
        start, field = grid.front()
        area = 0
        perimeter = 0
        corners = 0

        queue = [start]
        seen = set()
        while queue:
            current_pos = queue.pop()
            if current_pos in seen:
                continue
            seen.add(current_pos)

            area += 1
            neighbours = list(grid.neighbours(current_pos, include_diagonals=False))
            perimeter += 4 - len(neighbours)  # add the outer edges
            perimeter += sum(grid.get(x) != field for x in neighbours)
            corners += count_corners(parsed_input, current_pos, area)

            # Note: only adding options which belong to the same field
            queue += [x for x in neighbours if grid.get(x) == field and x not in seen]

        # Remove all coordinates of the field we just processed
        for c in seen:
            grid.remove(c)

        statistics.append((field, area, perimeter, corners))

    part1 = 0
    part2 = 0
    for _, size, perimeter, corners in statistics:
        part1 += size * perimeter
        part2 += size * corners

    return (part1, part2)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=12)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
