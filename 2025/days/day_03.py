"""Day 3: Lobby

Part 1:
    The goal is to find two numbers, per battery bank, that when combined in order produce the largest number and sum the results of all banks.

    The plan is to first find the largest number (per bank), and then find the largest number in the remaining number to the right of the first largest number.
    There is one edge case: when the first number is the last number in the bank. In that case, we look for the largest number to the left of the first largest number.

Part 2:
    For part 2 we now have to find the combination of 12 numbers.

    Lets refactor the above idea. Now, the first largest number needs to be found in a list of numbers excluding the last 11 numbers. The second largest number needs to be found in a list of numbers excluding the last 10 numbers, and so on.

"""


def _parse(input_data: str) -> list[list[int]]:
    return [[int(x) for x in bank] for bank in input_data.splitlines()]


def _part1(banks: list[list[int]]) -> int:
    result = 0
    for bank in banks:
        max1_value = max(bank)
        max1_index = bank.index(max1_value)

        remainder = bank[max1_index + 1 :]
        remainder_offset = max1_index + 1
        if remainder == []:
            remainder = bank[0:max1_index]
            remainder_offset = 0

        max2_value = max(remainder)
        max2_index = remainder_offset + remainder.index(max2_value)

        if max2_index < max1_index:
            result += max2_value * 10 + max1_value
        else:
            result += max1_value * 10 + max2_value
    return result


def _part2(banks: list[list[int]]) -> int:
    result = 0
    for bank in banks:
        n = 12
        offset = 0
        combi = 0
        for i in range(0, n):
            x = bank[offset : len(bank) - (n - i - 1)]
            max_value = max(x)
            offset += x.index(max_value) + 1
            combi += 10 ** (n - i - 1) * max_value
        result += combi

    return result


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2025, day=3)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
