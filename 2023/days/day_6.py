"""Day 6: Wait For It"""

import math


class Race:
    """Represents race data."""

    time: int
    distance: int

    def __init__(self, time, distance) -> None:
        self.time = time
        self.distance = distance

    def __repr__(self) -> str:
        return f"<Race: time: {self.time}, distance: {self.distance}>"


def _parse(input_lines: list[str]) -> list[Race]:
    time, distance = [map(int, line.split(":")[1].split()) for line in input_lines]
    races = zip(time, distance)
    return [Race(*x) for x in races]


def _calculate_number_of_winning_options(time: int, distance: int) -> int:
    wins = filter(lambda x: x > distance, map(lambda x: (time - x) * x, range(1, time)))
    return len(list(wins))


def _part1(parsed_data: list[Race]) -> int:
    result = 1
    for race in parsed_data:
        result *= _calculate_number_of_winning_options(race.time, race.distance)

    return result


def _part2(parsed_data: list[Race]) -> int:
    time = int("".join([str(race.time) for race in parsed_data]))
    distance = int("".join([str(race.distance) for race in parsed_data]))
    return round(math.sqrt(time**2 - 4 * distance))


def solve(input_lines: list[str]) -> tuple[int, int]:
    parsed_input = _parse(input_lines)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=6)
    example = puzzle.examples[0]
    example_input = example.input_data.splitlines()

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
