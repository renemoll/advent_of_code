"""Day 1: Trebuchet?!"""

NAMES = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def _extract_numbers_from_line(line):
    numbers = [x for x in line if x.isdigit()]
    return int(numbers[0] + numbers[-1])


def _part1(input_lines):
    result = 0
    for line in input_lines:
        result += _extract_numbers_from_line(line)
    return result


def _strip_line_to_first_last_number(line):
    while not any(filter(line.startswith, NAMES)) and not line[0].isdigit():
        line = line[1:]
    while not any(filter(line.endswith, NAMES)) and not line[-1].isdigit():
        line = line[:-1]
    return line


def _replace_textual_with_digits(line):
    for i, name in enumerate(NAMES):
        if line.startswith(name) and not line[0].isdigit():
            line = line.replace(name, str(i + 1), 1)
        if line.endswith(name) and not line[-1].isdigit():
            line = (str(i + 1)).join(line.rsplit(name, 1))
    return line


def _part2(input_lines):
    result = 0
    for line in input_lines:
        line = _strip_line_to_first_last_number(line)
        line = _replace_textual_with_digits(line)
        result += _extract_numbers_from_line(line)
    return result


def solve(input_lines):
    return (_part1(input_lines), _part2(input_lines))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=1)
    example = puzzle.examples[0]
    example_input = example.input_data.splitlines()
    print(f"Part 1: {_part1(example_input)}, expecting: {example.answer_a}")

    example = puzzle.examples[1]
    example_input = example.input_data.splitlines()
    print(f"Part 2: {_part2(example_input)}, expecting: {example.answer_b}")
