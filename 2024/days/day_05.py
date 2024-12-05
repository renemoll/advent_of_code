"""Day 5: Print Queue"""

import collections

from .utilities import pairwise_without_overlap, parse_ints


def _parse(input_data: str):
    rules, updates = input_data.split("\n\n")

    rule_map = collections.defaultdict(list)
    for k, v in pairwise_without_overlap(parse_ints(rules)):
        rule_map[k].append(v)
    updates = [parse_ints(line) for line in updates.splitlines()]
    return (rule_map, updates)


def _part1(parsed_input) -> int:
    rules, updates = parsed_input

    result = 0
    for update in updates:
        valid = True
        for i, page in enumerate(update):
            for remainder in update[i:]:
                if remainder in rules and page in rules[remainder]:
                    valid = False
                    break
        if valid:
            result += update[len(update) // 2]

    return result


def _part2(parsed_input) -> int:
    rules, updates = parsed_input

    result = 0
    for update in updates:
        valid = True
        for i, _ in enumerate(update):
            for j, remainder in enumerate(update[i:]):
                if remainder in rules and update[i] in rules[remainder]:
                    valid = False
                    update[i + j], update[i] = update[i], update[i + j]

        if not valid:
            result += update[len(update) // 2]

    return result


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=5)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
