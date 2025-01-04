"""Day 23: LAN Party"""

import collections

from .utilities import parse_words, take_n


def _parse(input_data: str):
    networks = collections.defaultdict(set)
    for n1, n2 in take_n(parse_words(input_data), 2):
        networks[n1].add(n2)
        networks[n2].add(n1)

    return networks


def _part1(parsed_input) -> int:
    networks = parsed_input

    triplets = []
    for base, options in networks.items():
        for option in options:
            intersect = networks[option] & options
            if len(intersect) > 0:
                for x in intersect:
                    y = sorted([base, option, x])
                    if y not in triplets:
                        triplets.append(y)

    result = 0
    for nodes in triplets:
        if any(n[0] == "t" for n in nodes):
            result += 1

    return result


def _part2(parsed_input) -> int:
    networks = parsed_input

    counter = collections.Counter()
    for base, options in networks.items():
        for option in options:
            intersect = networks[option] & options
            if len(intersect) > 1:
                y = sorted([base, option, *intersect])
                counter[",".join(y)] += 1

    def length_check(key):
        x = (len(key) + 1) // 3
        return x * (x - 1)

    results = {k: v for k, v in counter.items() if length_check(k) == v}
    return max(results, key=results.get)


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=23)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
