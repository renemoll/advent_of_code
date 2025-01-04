"""Day 22: Monkey Market"""

import collections
from .utilities import parse_ints


def mix(value, secret):
    return value ^ secret


def prune(value):
    return value % 16777216


def evolve_secret(secret: int) -> int:
    step1 = prune(mix(secret * 64, secret))
    step2 = prune(mix(step1 // 32, step1))
    step3 = prune(mix(step2 * 2048, step2))
    return step3


def _parse(input_data: str):
    return parse_ints(input_data)


def _part1(parsed_input) -> int:
    initial_secrets = parsed_input

    n = 2000
    result = 0
    for s in initial_secrets:
        secret = s
        for _ in range(n):
            secret = evolve_secret(secret)
        result += secret

    return result


def price_sequence(secret, n=2000):
    sequences = {}
    deltas = collections.deque(maxlen=4)
    previous_price = secret % 10

    for _ in range(n):
        secret = evolve_secret(secret)
        price = secret % 10
        deltas.append(price - previous_price)
        previous_price = price

        index = str(deltas)
        if len(deltas) == 4 and index not in sequences:
            sequences[index] = price
    return sequences


def _part2(parsed_input) -> int:
    """
    First idea of intersection of sequences does not work as the sequence is not garuanteed to be present in all secrets
    """
    initial_secrets = parsed_input

    bananas = collections.defaultdict(int)
    for secret in initial_secrets:
        sequence = price_sequence(secret)
        for delta, price in sequence.items():
            bananas[delta] += price

    max_total = max(bananas.values())

    return max_total


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=22)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
