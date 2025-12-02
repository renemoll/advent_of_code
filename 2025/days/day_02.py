"""Day 2: Gift Shop"""


def _parse(input_data: str) -> list[tuple[str, str]]:
    input_data = input_data.replace("\n", "")
    ranges = "".join(input_data).split(",")
    ranges = [tuple(r.split("-")) for r in ranges]
    return ranges


def _part1(parsed_input: list[tuple[str, str]]) -> int:
    result = 0
    for start, end in parsed_input:
        for x in range(int(start), int(end) + 1):
            y = str(x)
            if len(y) % 2 == 0:
                n = len(y) // 2
                left = y[0:n]
                right = y[n:]
                result += x if left == right else 0

    return result


def _part2(parsed_input: list[tuple[str, str]]) -> int:
    result = 0
    for start, end in parsed_input:
        for x in range(int(start), int(end) + 1):
            y = str(x)
            for n in range(len(y) // 2, 0, -1):
                expected = len(y) // n
                if expected != len(y) / n:
                    continue

                chunk = y[0:n]
                if y.count(chunk) == expected:
                    result += x
                    break

    return result


def solve(input_data: str) -> tuple[int, int]:
    """Solve both parts of the puzzle."""
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2025, day=2)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
