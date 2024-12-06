"""Day 6: guard_position Gallivant"""

from .utilities import SparseGrid, Coordinate


def rotate(c: Coordinate):
    directions = [
        Coordinate(0, -1),
        Coordinate(1, 0),
        Coordinate(0, 1),
        Coordinate(-1, 0),
    ]
    return directions[(directions.index(c) + 1) % len(directions)]


def position_on_grid(grid: SparseGrid, position: Coordinate):
    return 0 <= position.x < grid.columns and 0 <= position.y < grid.rows


def _parse(input_data: str):
    obstacles = SparseGrid(input_data.splitlines(), lambda x: x == "#")
    start = SparseGrid(input_data.splitlines(), lambda x: x == "^").find("^")
    return obstacles, start


def _part1(parsed_input) -> int:
    grid, start = parsed_input

    direction = Coordinate(0, -1)
    guard_position = start
    seen = [start]
    while True:
        new_position = guard_position + direction
        if new_position in grid.keys():
            direction = rotate(direction)
            continue

        if position_on_grid(grid, new_position):
            guard_position = new_position
            if not guard_position in seen:
                seen.append(guard_position)
        else:
            break

    return len(seen)


def _part2(parsed_input) -> int:
    grid, start = parsed_input

    direction = Coordinate(0, -1)
    guard_position = start
    seen = set((start, direction))
    options = []
    while True:
        new_position = guard_position + direction
        if new_position in grid.keys():
            direction = rotate(direction)
            continue

        if position_on_grid(grid, new_position):
            looking_at = new_position + rotate(direction)
            while position_on_grid(grid, looking_at):
                if (looking_at, rotate(direction)) in seen:
                    options.append(looking_at)
                    break
                if (
                    looking_at in grid.keys()
                    and (looking_at - rotate(direction), rotate(rotate(direction)))
                    in seen
                ):
                    options.append(looking_at)
                    break

                looking_at += rotate(direction)

            guard_position = new_position
            if not (guard_position, direction) in seen:
                seen.add((guard_position, direction))
        else:
            break

    return len(options)


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=6)
    for example in puzzle.examples:
        example_input = example.input_data

        solution = solve(example_input)
        print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
        print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
