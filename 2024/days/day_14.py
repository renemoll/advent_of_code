"""Day 14: Restroom Redoubt"""

import collections

from .utilities import parse_ints, take_n, Coordinate


def _parse(input_data: str):
    """TODO: distinguish between coordinate and vector?"""
    grid = collections.defaultdict(list)
    x_max = 0
    y_max = 0
    robots = 0
    for x in take_n(parse_ints(input_data), 4):
        grid[Coordinate(x[0], x[1])].append(Coordinate(x[2], x[3]))
        x_max = max(x_max, x[0])
        y_max = max(y_max, x[1])
        robots += 1
    return (grid, Coordinate(x_max + 1, y_max + 1), robots)


def _part1(parsed_input) -> int:
    grid, grid_size, _ = parsed_input

    iterations = 100
    updated_grid = collections.defaultdict(list)
    for position, velocities in grid.items():
        for velocity in velocities:
            new_position = (position + iterations * velocity) % grid_size
            updated_grid[new_position].append(velocity)

    x_limit = grid_size.x // 2
    y_limit = grid_size.y // 2

    quadrant = [0, 0, 0, 0]
    for p, vs in updated_grid.keys():
        robots = len(vs)
        if p.x < x_limit:
            if p.y < y_limit:
                quadrant[0] += robots
            elif p.y > y_limit:
                quadrant[2] += robots
        elif p.x > x_limit:
            if p.y < y_limit:
                quadrant[1] += robots
            elif p.y > y_limit:
                quadrant[3] += robots

    result = 1
    for x in quadrant:
        result *= x

    return result


def _part2(parsed_input) -> int:
    """I needed a hint for this one to realize it had to do with all robots being on a unique position."""
    grid, grid_size, robots = parsed_input
    max_iterations = 10000
    for i in range(max_iterations):
        updated_grid = collections.defaultdict(list)
        unique_positions = set()
        for position, velocities in grid.items():
            for velocity in velocities:
                new_position = (position + velocity) % grid_size
                updated_grid[new_position].append(velocity)
                unique_positions.add(new_position)
        grid = updated_grid

        if len(unique_positions) == robots:
            return i + 1

    return -1


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=14)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
