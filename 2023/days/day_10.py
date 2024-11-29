"""Day 10: Pipe Maze"""

import enum
import math
import collections

from .utilities import Matrix, Coordinate, list_1d_to_2d


class Pipe(enum.Enum):
    """Represents a pipe orientation."""

    NS = 1
    EW = 2
    NE = 3
    NW = 4
    SW = 5
    SE = 6
    Ground = 7
    Start = 8

    @staticmethod
    def from_str(char):
        lookup = {
            "|": Pipe.NS,
            "-": Pipe.EW,
            "L": Pipe.NE,
            "J": Pipe.NW,
            "7": Pipe.SW,
            "F": Pipe.SE,
            ".": Pipe.Ground,
            "S": Pipe.Start,
        }
        return lookup[char]

    @staticmethod
    def directions(pipe) -> list[Coordinate]:
        lookup = {
            Pipe.NS: [Coordinate(-1, 0), Coordinate(1, 0)],
            Pipe.EW: [Coordinate(0, 1), Coordinate(0, -1)],
            Pipe.NE: [Coordinate(-1, 0), Coordinate(0, 1)],
            Pipe.NW: [Coordinate(-1, 0), Coordinate(0, -1)],
            Pipe.SW: [Coordinate(1, 0), Coordinate(0, -1)],
            Pipe.SE: [Coordinate(1, 0), Coordinate(0, 1)],
            Pipe.Ground: [],
            Pipe.Start: [
                Coordinate(1, 0),
                Coordinate(-1, 0),
                Coordinate(0, 1),
                Coordinate(0, -1),
            ],
        }
        return lookup[pipe]


class PipeMaze(Matrix):
    """Specializes Matrix for the pipe maze."""

    def __init__(self, rows):
        data = [[Pipe.from_str(c) for c in row] for row in rows]
        super().__init__(data)
        self.start = self.find(Pipe.Start)


def _parse(input_lines: list[str]) -> tuple[PipeMaze, Matrix]:
    pipes = PipeMaze(input_lines)
    directions = Matrix(
        list_1d_to_2d([Pipe.directions(pipe) for pipe in pipes], pipes.columns)
    )
    return (pipes, directions)


def _part1(parsed_input: tuple[PipeMaze, Matrix]) -> int:
    maze, directions = parsed_input
    todo: list[Coordinate] = [maze.start]
    seen: set[Coordinate] = set()

    while len(todo) > 0:
        current_pos = todo.pop(0)
        if current_pos in seen:
            continue
        seen.add(current_pos)

        options = [current_pos + rel for rel in directions.get(current_pos)]
        todo += options

    depth = math.ceil(len(seen)) // 2
    return depth


def _part2(parsed_input: tuple[PipeMaze, Matrix]) -> int:
    maze, directions = parsed_input
    todo = collections.deque([(maze.start, 0)])
    seen: set[Coordinate] = set([maze.start])
    shoelace = 0

    while todo:
        current_pos, depth = todo.popleft()
        options = [current_pos + offset for offset in directions.get(current_pos)]
        for option in options:
            # Walk the pipeline in one direction
            if not option in seen:
                shoelace += (current_pos.x * option.y) - (current_pos.y * option.x)
                todo.append((option, depth + 1))
                seen.add(option)
                break
            if option == maze.start and depth > 1:
                shoelace += (current_pos.x * option.y) - (current_pos.y * option.x)
                break

    area = abs(shoelace) // 2
    depth = len(seen) // 2
    enclosed = area - depth + 1
    return enclosed


def solve(input_lines: list[str]) -> tuple[int, int]:
    parsed_input = _parse(input_lines)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=10)
    example = puzzle.examples[4]
    example_input = example.input_data.splitlines()

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
