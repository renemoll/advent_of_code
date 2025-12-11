"""Day 10: Factory

Part 1:
    Today we start with building a graph.
    Note: BFS without tracking visited nodes, as we want all paths.

"""

import functools


def _parse(input_data: str) -> dict[str, list[str]]:
    return {
        line.split(":")[0]: line.split(":")[1].strip().split()
        for line in input_data.splitlines()
    }


def _part1(connections: dict[str, list[str]]) -> int:
    start = "you"
    queue = [(start, 1)]

    result = 0
    while queue:
        current, paths = queue.pop(0)

        if current == "out":
            result += 1
            continue

        outputs = connections.get(current, [])
        for i, output in enumerate(outputs):
            queue.append((output, paths + i))

    return result


def _part2(connections: dict[str, list[str]]) -> int:
    @functools.cache
    def number_of_paths(start: str, end: str) -> int:
        if start == end:
            return 1
        return sum(
            number_of_paths(output, end) for output in connections.get(start, [])
        )

    result = (
        number_of_paths("svr", "fft")
        * number_of_paths("fft", "dac")
        * number_of_paths("dac", "out")
    )
    result += (
        number_of_paths("svr", "dac")
        * number_of_paths("dac", "fft")
        * number_of_paths("fft", "out")
    )
    return result


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2025, day=11)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
