"""Day 3: Lobby

Part 1:
    Find two numbers, per line, which when combined in order produce the largest number for that line.

    The plan here is to first find the largest number, and then find the largest number in the remaining numbers to the
    right of the first largest number. There is one edge case: when the first number is the last number in the bank. In
    that case, we look for the largest number to the left of the first largest number and swap the result.

Part 2:
    For part 2 we now have to find the combination of the 12 largest numbers.

    To solve this I need to refactor the previous idea. The first largest number needs to be found within the numbers
    from the start of that line and excluding the last 11 numbers. The second largest number needs to be found within
    the numbers from the first largest number and excluding the last 10 numbers, and so on. So first construct a list
    of options which can be searched through, then find the largest number within those options iteratively.
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
        intermediate = 0
        for i in range(0, n):
            x = bank[offset : len(bank) - (n - i - 1)]
            max_value = max(x)
            offset += x.index(max_value) + 1
            intermediate += 10 ** (n - i - 1) * max_value
        result += intermediate

    return result


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))
