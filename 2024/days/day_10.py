"""Day 10: Hoof It"""

from .utilities import Grid, Coordinate


def _parse(input_data: str):
    return Grid(input_data.splitlines())


def _part1(parsed_input) -> int:
    grid = parsed_input

    result = 0
    for start in grid.find_all("0"):
        todo = [start]
        seen: set[Coordinate] = set()
        endpoints = set()

        while todo:
            current_pos = todo.pop()
            if current_pos in seen:
                continue
            seen.add(current_pos)

            height = grid.get(current_pos)
            if height == "9":
                endpoints.add(current_pos)
                continue

            options = [
                x
                for x in grid.neighbours(current_pos, include_diagonals=False)
                if x not in seen
            ]
            expected_height = str(int(height) + 1)
            todo += [x for x in options if grid.get(x) == expected_height]

        result += len(endpoints)

    return result


def _part2(parsed_input) -> int:
    grid = parsed_input

    result = 0
    for start in grid.find_all("0"):
        todo = [start]
        seen: set[Coordinate] = set()
        endpoints = {}

        while todo:
            current_pos = todo.pop()

            height = grid.get(current_pos)
            if height == "9":
                if current_pos in endpoints:
                    endpoints[current_pos] += 1
                else:
                    endpoints[current_pos] = 1
                continue

            seen.add(current_pos)

            options = grid.neighbours(current_pos, include_diagonals=False)
            expected_height = str(int(height) + 1)
            todo += [x for x in options if grid.get(x) == expected_height]

        result += sum(endpoints.values())

    return result


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=10)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
