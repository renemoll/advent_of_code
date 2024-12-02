"""Day 11: Cosmic Expansion"""

from .utilities import Matrix, Coordinate


def _parse(input_data: str) -> tuple[Matrix, list[Coordinate]]:
    """
    Todo:
    - remove galaxy_map
    """
    galaxy_map = Matrix(input_data.splitlines())
    galaxies = galaxy_map.find_all("#")

    return (galaxy_map, galaxies)


def _expand(
    parsed_input: tuple[Matrix, list[Coordinate]], offset: int
) -> tuple[list[int], list[int]]:
    galaxy_map, galaxies = parsed_input

    offset_x = [offset] * galaxy_map.rows
    offset_y = [offset] * galaxy_map.columns
    for c in galaxies:
        offset_x[c.x] = 0
        offset_y[c.y] = 0

    sum_x = 0
    for n, x in enumerate(offset_x):
        sum_x += x
        offset_x[n] = sum_x
    sum_y = 0
    for n, y in enumerate(offset_y):
        sum_y += y
        offset_y[n] = sum_y
    return (offset_x, offset_y)


def _part1(parsed_input: tuple[Matrix, list[Coordinate]]) -> int:
    _, galaxies = parsed_input
    x, y = _expand(parsed_input, 1)

    length = 0
    for n, start in enumerate(galaxies):
        sx = start.x + x[start.x]
        sy = start.y + y[start.y]
        for other in galaxies[n + 1 :]:
            ox = other.x + x[other.x]
            oy = other.y + y[other.y]

            dx = max(sx, ox) - min(sx, ox)
            dy = max(sy, oy) - min(sy, oy)
            length += dx + dy

    return length


def _part2(parsed_input: tuple[Matrix, list[Coordinate]]) -> int:
    _, galaxies = parsed_input
    x, y = _expand(parsed_input, 1000000 - 1)

    length = 0
    for n, start in enumerate(galaxies):
        sx = start.x + x[start.x]
        sy = start.y + y[start.y]
        for other in galaxies[n + 1 :]:
            ox = other.x + x[other.x]
            oy = other.y + y[other.y]

            dx = max(sx, ox) - min(sx, ox)
            dy = max(sy, oy) - min(sy, oy)
            length += dx + dy

    return length


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=11)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
