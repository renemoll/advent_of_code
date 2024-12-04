"""Day 3: Mull It Over"""

import re


def _parse(input_data: str):
    return re.findall(r"(mul|do|don't)\((\d{1,3})?,?(\d{1,3})?\)", input_data)


def _part1(parsed_input) -> int:
    return sum(int(a) * int(b) if op == "mul" else 0 for op, a, b in parsed_input)


def _part2(parsed_input) -> int:
    result = 0
    enabled = True
    for op, a, b in parsed_input:
        match op:
            case "mul":
                result += int(a) * int(b) if enabled else 0
            case "do":
                enabled = True
            case "don't":
                enabled = False
    return result


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=3)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
