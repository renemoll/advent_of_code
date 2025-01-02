"""Day 21: Keypad Conundrum"""

import itertools
import functools

from .utilities import Coordinate, parse_ints


class Keypad:
    """Represent a keypad."""

    def __init__(self, keys: list[str]):
        k = {
            c: Coordinate(x, y) for y, row in enumerate(keys) for x, c in enumerate(row)
        }
        self.invalid = k["x"]
        del k["x"]
        self.valid = k

    def generate_path(self, start: str, destination: str):
        """
        Lattice paths -> attempted under the assumption we have to determine the number of options -> bad end

        We want to move over a keypad as quickly (least steps) as possible.
        This implies limiting the number of directional changes and favoring long straight movements.
        However we need to avoid the empty space, this can be achieved by prefering a certain order X/Y or Y/X.

        Doing this sequentially (complete the commands for robot 1 and then robot 2) may not yield the shortest path... instead we have to following a path trough...
        """
        delta = self.valid[destination] - self.valid[start]

        x_movement = ["<", ">"][delta.x > 0] * abs(delta.x)
        y_movement = ["v", "^"][delta.y < 0] * abs(delta.y)

        if self.valid[start] + Coordinate(delta.x, 0) != self.invalid:
            yield x_movement + y_movement + "A"
        if self.valid[start] + Coordinate(0, delta.y) != self.invalid:
            yield y_movement + x_movement + "A"


numeric_keypad = Keypad(["789", "456", "123", "x0A"])
directional_keypad = Keypad(["x^A", "<v>"])


@functools.cache
def determine_path(start: str, destination: str, level: int, top_level: int):
    if level == 1:
        return 1

    keypad = directional_keypad if top_level != level else numeric_keypad
    return min(
        find_shorted_path(path, level - 1, top_level)
        for path in keypad.generate_path(start, destination)
    )


def find_shorted_path(code: str, level: int, top_level: int):
    return sum(
        determine_path(p1, p2, level, top_level)
        for p1, p2 in itertools.pairwise("A" + code)
    )


def _parse(input_data: str):
    return input_data.splitlines()


def _part1(parsed_input) -> int:
    codes = parsed_input

    complexity = 0
    keypads = 4
    for code in codes:
        movement = find_shorted_path(code, keypads, keypads)
        complexity += movement * parse_ints(code)[0]

    return complexity


def _part2(parsed_input) -> int:
    codes = parsed_input

    complexity = 0
    keypads = 27
    for code in codes:
        movement = find_shorted_path(code, keypads, keypads)
        complexity += movement * parse_ints(code)[0]

    return complexity


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=21)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
