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


def solve(input_data: str) -> tuple[int, int]:
    rules, updates = _parse(input_data)

    part1 = 0
    part2 = 0
    for update in updates:
        valid = True
        for i, _ in enumerate(update):
            for j, remainder in enumerate(update[i:]):
                if remainder in rules and update[i] in rules[remainder]:
                    valid = False
                    update[i + j], update[i] = update[i], update[i + j]

        if valid:
            part1 += update[len(update) // 2]
        else:
            part2 += update[len(update) // 2]

    return part1, part2


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=5)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
