"""Day 4: Ceres Search"""

from .utilities import Grid, Coordinate


def _parse(input_data: str):
    return Grid(input_data.splitlines())


def _part1(grid: Grid) -> int:
    result = 0
    for x in grid.find_all("X"):
        for option in grid.neighbours(x):
            if grid.get(option) == "M":
                delta = option - x
                coordinates = [x + n * delta for n in range(4)]
                if (
                    0 <= coordinates[-1].x < grid.columns
                    and 0 <= coordinates[-1].y < grid.rows
                ):
                    text = "".join([grid.get(c) for c in coordinates])
                    result += 1 if text == "XMAS" else 0

    return result


def _part2(grid: Grid) -> int:
    result = 0

    for pos in grid.find_all("A"):
        text = ""
        for dx, dy in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:  # note: order matters
            option = pos + Coordinate(dx, dy)
            if 0 <= option.x < grid.columns and 0 <= option.y < grid.rows:
                text += grid.get(option)
        result += 1 if text[0:2] in ["MS", "SM"] and text[2:4] in ["MS", "SM"] else 0

    return result


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=4)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")  # 2662
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")  # 2034
