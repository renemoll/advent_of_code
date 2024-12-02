"""Day 1: Trebuchet?!"""

NAMES = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def extract_numbers_from_line(line: str) -> int:
    numbers = [x for x in line if x.isdigit()]
    return int(numbers[0] + numbers[-1])


def _part1(input_data: str) -> int:
    return sum(extract_numbers_from_line(line) for line in input_data.splitlines())


def _part2(input_data: str) -> int:
    result = 0
    for line in input_data.splitlines():
        xs = []
        for i, c in enumerate(line):
            if c.isdigit():
                xs.append(c)
            for j, number in enumerate(NAMES):
                if line[i:].startswith(number):
                    xs.append(str(j + 1))
        result += int(xs[0] + xs[-1])
    return result


def solve(input_data: str) -> tuple[int, int]:
    return (_part1(input_data), _part2(input_data))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=1)
    example = puzzle.examples[0]
    example_input = example.input_data
    print(f"Part 1: {_part1(example_input)}, expecting: {example.answer_a}")

    example = puzzle.examples[1]
    example_input = example.input_data
    print(f"Part 2: {_part2(example_input)}, expecting: {example.answer_b}")
