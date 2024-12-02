"""Day 8: Haunted Wasteland"""

import math


def _parse(input_data: str) -> list[dict[str, tuple[str, str]]]:
    input_lines = input_data.splitlines()
    directions = input_lines[0]

    nodes = {}
    for line in input_lines[2:]:
        key, values = line.split(" = ")
        left, right = values.split(", ")
        nodes[key] = (left[1:], right[:3])

    return (directions, nodes)


def _part1(parsed_data: list[dict[str, tuple[str, str]]]) -> int:
    directions, nodes = parsed_data

    current_node = "AAA"
    steps = 0

    while True:
        left, right = nodes[current_node]
        direction = directions[steps % len(directions)]
        match direction:
            case "L":
                current_node = left
            case "R":
                current_node = right
        steps += 1

        if current_node == "ZZZ":
            break

    return steps


def _part2(parsed_data: list[dict[str, tuple[str, str]]]) -> int:
    directions, nodes = parsed_data

    current_nodes = list(filter(lambda x: x[2] == "A", nodes.keys()))
    steps = 0
    result = len(directions)

    while len(list(current_nodes)) > 0:
        for node in current_nodes:
            if node[2] == "Z":
                result = math.lcm(result, steps)
                current_nodes.remove(node)

        for n, node in enumerate(current_nodes):
            left, right = nodes[node]
            direction = directions[steps % len(directions)]
            match direction:
                case "L":
                    current_nodes[n] = left
                case "R":
                    current_nodes[n] = right
        steps += 1

    return result


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=8)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
