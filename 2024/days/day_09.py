"""Day 9: Disk Fragmenter"""

import pprint


def is_even(n):
    return n % 2 == 0


def _parse(input_data: str):
    files = []
    spaces = []
    file_id = 0
    for n, c in enumerate(input_data):
        if is_even(n):
            files.append((int(c), file_id))
            file_id += 1
        else:
            spaces.append((int(c)))
    return files, spaces


def _part1(parsed_input) -> int:
    files, spaces = parsed_input

    file_map = [files[0]]
    files = files[1:]  # we always start with a file, so can move that one directly

    while files:
        available_size = spaces[0]
        required_size = files[-1][0]
        file_id = files[-1][1]

        size = min(available_size, required_size)
        available_size -= size
        required_size -= size
        file_map.append((size, file_id))

        if available_size == 0:
            file_map.append(files[0])
            spaces = spaces[1:]
            files = files[1:]
        else:
            spaces[0] = available_size

        if required_size == 0:
            files = files[:-1]
        else:
            try:
                files[-1] = (required_size, file_id)
            except IndexError:
                file_map[-1] = (required_size, file_id)

    result = 0
    offset = 0
    for size, file_id in file_map:
        for i in range(size):
            result += (offset + i) * file_id
        offset += size

    return result


def _part2(parsed_input) -> int:
    pprint.pprint(parsed_input)

    return 0


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=9)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
