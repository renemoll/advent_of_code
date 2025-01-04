"""Day 23: LAN Party"""

import pprint
import collections

from .utilities import parse_words, take_n


def _parse(input_data: str):
    return list(take_n(parse_words(input_data), 2))


def _part1(parsed_input) -> int:
    # pprint.pprint(parsed_input)
    connections = parsed_input

    networks = collections.defaultdict(set)
    for n1, n2 in connections:
        networks[n1].add(n2)
        networks[n2].add(n1)
    # pprint.pprint(networks)

    triplets = []
    for base, options in networks.items():
        for option in options:
            intersect = networks[option] & options
            # pprint.pprint(f"{base=}, {option=}, {intersect=}")
            if len(intersect) > 0:
                for x in intersect:
                    y = sorted([base, option, x])
                    if y not in triplets:
                        triplets.append(y)
    # pprint.pprint(triplets)

    result = 0
    for nodes in triplets:
        if any(n[0] == "t" for n in nodes):
            result += 1

    return result


def _part2(parsed_input) -> int:
    # pprint.pprint(parsed_input)
    connections = parsed_input

    networks = collections.defaultdict(set)
    for n1, n2 in connections:
        networks[n1].add(n2)
        networks[n2].add(n1)

    for base, options in networks.items():
        for option in options:
            intersect = networks[option] & options
            pprint.pprint(f"{base=}, {option=}, {intersect=}")

    # networks = []
    # for n1, n2 in connections:
    #     found = False
    #     for network in networks:
    #         if n1 in network or n2 in network:
    #             network.add(n1)
    #             network.add(n2)
    #             found = True
    #             break

    #     if not found:
    #         networks.append(set([n1, n2]))

    # pprint.pprint(networks)

    return 0


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
