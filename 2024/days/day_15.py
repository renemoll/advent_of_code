"""Day 15: Warehouse Woes"""

import enum

from .utilities import Grid, Coordinate


class Direction(enum.Enum):
    """Represents a direction the robot moves towards."""

    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    @staticmethod
    def from_char(char: str) -> "Direction":
        match char:
            case "<":
                return Direction.LEFT
            case ">":
                return Direction.RIGHT
            case "^":
                return Direction.UP
            case "v":
                return Direction.DOWN


def direction_to_vector(move: Direction) -> Coordinate:
    match move:
        case Direction.LEFT:
            delta = Coordinate(-1, 0)
        case Direction.RIGHT:
            delta = Coordinate(1, 0)
        case Direction.UP:
            delta = Coordinate(0, -1)
        case Direction.DOWN:
            delta = Coordinate(0, 1)
    return delta


def _parse(input_data: str):
    sections = input_data.split("\n\n")

    grid = Grid(sections[0].splitlines())
    movements = list(map(Direction.from_char, "".join(sections[1].splitlines())))

    return (grid, movements)


def within_bounds(grid, position):
    return 0 <= position.x < grid.columns and 0 <= position.y < grid.rows


def _part1(parsed_input) -> int:
    grid, movements = parsed_input

    position = grid.find("@")
    for move in movements:
        delta = direction_to_vector(move)
        option = position + delta

        match grid.get(option):
            case ".":
                grid.set(option, "@")
                grid.set(position, ".")
                position = option
            case "O":
                space = option + delta
                while within_bounds(grid, space):
                    if grid.get(space) == "#":
                        break
                    if grid.get(space) == ".":
                        grid.set(space, "O")
                        grid.set(option, "@")
                        grid.set(position, ".")
                        position = option
                        break
                    space += delta

    result = 0
    for box in grid.find_all("O"):
        result += 100 * box.y + box.x

    return result


def _part2(parsed_input) -> int:
    _, _ = parsed_input
    return 0


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=15)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
