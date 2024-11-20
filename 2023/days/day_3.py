"""Day 3: Gear Ratios"""

from .utilities import Grid, Coordinate


def _parse(input_lines):
    indices = Grid(input_lines)
    numbers = []
    symbols = []

    for r, line in enumerate(input_lines):
        number = 0
        for c, char in enumerate(line):
            if char.isdigit():
                number = 10 * number + int(char)
                indices.set(Coordinate(r, c), str(len(numbers)))
            else:
                if number > 0:
                    numbers.append(number)
                    number = 0

                if char != ".":
                    symbols.append((Coordinate(r, c), char))

        if number > 0:
            numbers.append(number)

    return (indices, numbers, symbols)


def _part1(parsed_data):
    indices, numbers, symbols = parsed_data
    result = 0
    for coordinate, _ in symbols:
        seen = []
        for neighbour in coordinate.neighbours():
            index = indices.get(neighbour)
            if index.isdigit() and not index in seen:
                result += numbers[int(index)]
                seen.append(index)

    return result


def _part2(parsed_data):
    indices, numbers, symbols = parsed_data
    result = 0
    for coordinate, symbol in symbols:
        if symbol != "*":
            continue

        ratio = 1
        seen = []
        for neighbour in coordinate.neighbours():
            index = indices.get(neighbour)
            if index.isdigit() and not index in seen:
                ratio = ratio * numbers[int(index)]
                seen.append(index)

        if len(seen) > 1:
            result += ratio

    return result


def solve(input_lines):
    parsed_input = _parse(input_lines)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=3)
    example = puzzle.examples[0]
    example_input = example.input_data.splitlines()

    parsed = _parse(example_input)
    print(f"Part 1: {_part1(parsed)}, expecting: {example.answer_a}")
    print(f"Part 2: {_part2(parsed)}, expecting: {example.answer_b}")
