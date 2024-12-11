"""Day 6: guard_position Gallivant"""

from .utilities import SparseGrid, Coordinate


DIRECTIONS = [
    Coordinate(0, -1),
    Coordinate(1, 0),
    Coordinate(0, 1),
    Coordinate(-1, 0),
]


def position_on_grid(grid: SparseGrid, position: Coordinate):
    return 0 <= position.x < grid.columns and 0 <= position.y < grid.rows


def _parse(input_data: str) -> tuple[SparseGrid, Coordinate]:
    obstacles = SparseGrid(input_data.splitlines(), lambda x: x == "#")
    start = SparseGrid(input_data.splitlines(), lambda x: x == "^").find("^")
    return obstacles, start


def _part1(parsed_input: tuple[SparseGrid, Coordinate]) -> int:
    grid, start = parsed_input

    direction_index = 0
    guard_position = start
    seen = set([start])
    obstacle_positions = grid.keys()
    while True:
        new_position = guard_position + DIRECTIONS[direction_index]
        if new_position in obstacle_positions:
            direction_index = (direction_index + 1) % 4
            continue

        if position_on_grid(grid, new_position):
            guard_position = new_position
            if not guard_position in seen:
                seen.add(guard_position)
        else:
            break

    return len(seen)


def _part2(parsed_input: tuple[SparseGrid, Coordinate]) -> int:
    grid, start = parsed_input

    direction_index = 0
    guard_position = start
    seen = set((start, direction_index))
    obstacle_positions = grid.keys()
    options = []
    while True:
        new_position = guard_position + DIRECTIONS[direction_index]
        if new_position in obstacle_positions:
            direction_index = (direction_index + 1) % 4
            continue

        if position_on_grid(grid, new_position):
            peek_direction_index = (direction_index + 1) % 4
            peek = new_position + DIRECTIONS[peek_direction_index]
            while position_on_grid(grid, peek):
                if (peek, peek_direction_index) in seen:
                    options.append(peek)
                    break
                if (
                    peek in obstacle_positions
                    and (
                        peek - DIRECTIONS[peek_direction_index],
                        ((direction_index + 2) % 4),
                    )
                    in seen
                ):
                    options.append(peek)
                    break

                peek += DIRECTIONS[peek_direction_index]

            guard_position = new_position
            if not (guard_position, direction_index) in seen:
                seen.add((guard_position, direction_index))
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
