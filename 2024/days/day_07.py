"""Day 7: Bridge Repair"""


from .utilities import parse_ints


def _parse(input_data: str) -> list[list[int]]:
    return [parse_ints(x) for x in input_data.splitlines()]


def _part1(parsed_input: list[list[int]]) -> int:
    result = 0
    for equation in parsed_input:
        lhs = equation[0]
        intermediate = [equation[1]]
        values = equation[2:]

        for x in values:
            options = []
            for i in intermediate:
                options.append(i * x)
                options.append(i + x)
            intermediate = [x for x in options if x <= lhs]

        if lhs in intermediate:
            result += lhs

    return result


def _part2(parsed_input: list[list[int]]) -> int:
    result = 0
    for equation in parsed_input:
        lhs = equation[0]
        intermediate = [equation[1]]
        values = equation[2:]

        for x in values:
            options = []
            for i in intermediate:
                options.append(i * x)
                options.append(i + x)
                options.append(int(str(i) + str(x)))
            intermediate = [x for x in options if x <= lhs]

        if lhs in intermediate:
            result += lhs

    return result


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=7)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
