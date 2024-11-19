from aocd import get_data

def _extract_numbers_from_line(line):
    numbers = [x for x in line if x.isdigit()]
    return int(numbers[0] + numbers[-1])

def _part1(input_lines):
    result = 0
    for line in input_lines:
        result += _extract_numbers_from_line(line)
    return result

NAMES = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

def _strip_line_to_first_last_number(line):
    while not any(filter(lambda x: line.startswith(x), NAMES)) and not line[0].isdigit():
        line = line[1:]
    while not any(filter(lambda x: line.endswith(x), NAMES)) and not line[-1].isdigit():
        line = line[:-1]
    return line

def _replace_textual_with_digits(line):
    for i,name in enumerate(NAMES):
        if line.startswith(name) and not line[0].isdigit():
            line = line.replace(name, str(i+1), 1)
        if line.endswith(name) and not line[-1].isdigit():
            line = (str(i+1)).join(line.rsplit(name, 1))
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
    data = get_data(day=1, year=2023).splitlines()
    print(f"Part 1: {_part1(data)}")
    print(f"Part 2: {_part2(data)}")
