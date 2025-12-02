"""Day 15: Warehouse Woes"""

import copy
import enum
import itertools

import pprint

from .utilities import Grid, Coordinate, list_1d_to_2d


def direction_to_vector(char: str) -> Coordinate:
    match char:
        case "<":
            return Coordinate(-1, 0)
        case ">":
            return Coordinate(1, 0)
        case "^":
            return Coordinate(0, -1)
        case "v":
            return Coordinate(0, 1)


class Warehouse(Grid):
    """A warehouse filled with boxes and a single robot to move said boxes."""

    class BoxType(enum.Enum):
        """Types of boxes in the warehouse."""

        SLIM = 1
        WIDE = 2

    def __init__(self, data):
        super().__init__(data)
        self.robot = self.find("@")
        self.box_type = Warehouse.BoxType.SLIM

    def __str__(self) -> str:
        return "\n".join(
            "".join(map(str, row)) for row in list_1d_to_2d(self._data, self.columns)
        )

    def widen(self, factor: int = 2) -> None:
        def convert(i, x):
            if x == "@":
                return x if i / factor == i // factor else "."
            if x == "O":
                return "[" if i / factor == i // factor else "]"
            return x

        self._data = [
            convert(i, self._data[i // factor]) for i in range(len(self._data) * factor)
        ]
        self._stride = self._stride * factor
        self.columns = self.columns * factor
        self.box_type = Warehouse.BoxType.WIDE
        self.robot = self.find("@")

    def is_position_valid(self, position: Coordinate) -> bool:
        return 0 <= position.x < self.columns and 0 <= position.y < self.rows

    def path_in_direction(
        self, position: Coordinate, direction: Coordinate
    ) -> list[Coordinate]:
        result = []
        while self.is_position_valid(position):
            field = self.get(position)
            if field in "#":
                break
            result.append(position)
            position += direction
        return result

    def fan_out_path(self, position: Coordinate, delta: Coordinate) -> list[Coordinate]:
        """TODO: need to define a direction to fan out to avoid duplication"""
        current_side = self.get(position)
        match current_side:
            case "]":
                path = self.path_in_direction(position + Coordinate(-1, 0), delta)
            case "[":
                path = self.path_in_direction(position + Coordinate(1, 0), delta)

        result = list(itertools.takewhile(lambda x: self.get(x) in "[]", path))
        pprint.pprint(f"fan_out_path: {result}")
        if len(result) > 1:
            result += self.fan_out_path(result[1], delta)
        return result

    def move_robot(self, delta: Coordinate) -> None:
        # Get all Coordinates in the desired direction until we hit a wall
        path = self.path_in_direction(self.robot, delta)
        items = [self.get(c) for c in path]

        if "." in items:
            # We can actually perform a move
            pprint.pprint(f"{self.robot=}, {delta=}, {path=}")
            pprint.pprint(f"{items=}")

            if self.box_type == Warehouse.BoxType.SLIM:
                coordinates_to_move = list(
                    itertools.takewhile(lambda x: self.get(x) in "@O", path)
                )
            else:
                coordinates_to_move = list(
                    itertools.takewhile(lambda x: self.get(x) in "@[]", path)
                )
                # Hitting a wide box from the left or right does not impact the basic logic
                # Hitteng a wide box from the top or bottom means we move 2 sides and even even more then one box
                if delta.x == 0 and len(coordinates_to_move) > 1:
                    found = set()
                    for i, c in enumerate(coordinates_to_move):
                        if i == 0:
                            continue
                        if self.get(c) in found:
                            continue
                        coordinates_to_move += self.fan_out_path(
                            coordinates_to_move[i], delta
                        )
                        found.add(coordinates_to_move[i])
                        if len(found) > 2:
                            break

                pprint.pprint(f"{coordinates_to_move=}")
            for c in reversed(coordinates_to_move):
                self.set(c + delta, self.get(c))
            self.set(self.robot, ".")
            self.robot = self.robot + delta


def gps_coordinate_box(c: Coordinate) -> int:
    return 100 * c.y + c.x


def _parse(input_data: str):
    sections = input_data.split("\n\n")

    grid = Warehouse(sections[0].splitlines())
    movements = list(map(direction_to_vector, "".join(sections[1].splitlines())))

    return (grid, movements)


def _part1(parsed_input) -> int:
    grid, movements = parsed_input
    grid = copy.deepcopy(grid)

    for delta in movements:
        grid.move_robot(delta)

    return sum(gps_coordinate_box(box) for box in grid.find_all("O"))


def _part2(parsed_input) -> int:
    """
    Options:
    - model boxes as entities in a grid which may have arbitrary size and can hit eachother.
    - extend the move in line to spread out in case of a box <- lets start with this.
    """
    grid, movements = parsed_input
    grid.widen(2)
    print(grid)
    movements = [
        Coordinate(-1, 0),
        Coordinate(0, 1),
        Coordinate(-1, 0),
        Coordinate(0, -1),
    ]
    # count = 0
    for delta in movements:
        pprint.pprint(f"{delta=}")
        grid.move_robot(delta)
        # count += 1
        # if count >= 4:
        # break
    print(grid)

    return sum(gps_coordinate_box(box) for box in grid.find_all("["))


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=15)
    example = puzzle.examples[1]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
