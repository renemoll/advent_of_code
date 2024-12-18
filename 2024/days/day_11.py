"""Day 11: Plutonian Pebbles"""

import collections

from .utilities import parse_ints, is_even


def blink(stones: list[int], blinks: int) -> int:
    for _ in range(blinks):
        new_counter = collections.Counter()
        for number, occurrences in stones.items():
            if number == 0:
                new_counter[1] += occurrences
            elif is_even(len(str(number))):
                l = len(str(number)) // 2
                new_counter[int(str(number)[:l])] += occurrences
                new_counter[int(str(number)[l:])] += occurrences
            else:
                new_counter[number * 2024] = occurrences
        stones = new_counter

    return stones.total()


def _parse(input_data: str):
    return collections.Counter(parse_ints(input_data))


def _part1(parsed_input) -> int:
    return blink(parsed_input, 25)


def _part2(parsed_input) -> int:
    return blink(parsed_input, 75)


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=11)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
