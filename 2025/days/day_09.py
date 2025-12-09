"""Day 9: Movie Theater

Part 1:
    Given coordinates of red tiles, find the biggest rectangle that can be formed using two red tiles as opposite corners.

Part 2:
    Find the biggest rectangle that can be formed within the shape formed by all red tiles.
"""

import itertools


def _parse(input_data: str) -> list[tuple[int, int]]:
    red_tiles = [tuple(map(int, line.split(","))) for line in input_data.splitlines()]
    return red_tiles


def euclidean_distance(lhs: tuple[int, int], rhs: tuple[int, int]) -> int:
    """Calculate the squared Euclidean distance between two 3D coordinates.

    Note:
        Omitting the square root for performance reasons (not needed).
    """

    return (lhs[0] - rhs[0]) ** 2 + (lhs[1] - rhs[1]) ** 2


def area(lhs: tuple[int, int], rhs: tuple[int, int]) -> int:
    width = abs(lhs[0] - rhs[0]) + 1
    height = abs(lhs[1] - rhs[1]) + 1
    return width * height


def _part1(red_tiles: list[tuple[int, int]]) -> int:
    max_area = 0
    for a, b in itertools.combinations(red_tiles, 2):
        area_ab = area(a, b)
        max_area = max(max_area, area_ab)

    return max_area


def generate_edges(start: tuple[int, int], end: tuple[int, int]) -> list[list[int]]:
    return [
        min(start[0], end[0]),
        min(start[1], end[1]),
        max(start[0], end[0]),
        max(start[1], end[1]),
    ]


def generate_perimeter(red_tiles: list[tuple[int, int]]) -> list[list[int]]:
    result = []
    for i, end in enumerate(red_tiles):
        start = red_tiles[i - 1]
        result += [generate_edges(start, end)]

    return result


def area_inside_perimeter(edges: list[int], perimeter: list[list[int]]) -> bool:
    min_x, min_y, max_x, max_y = edges
    for p_min_x, p_min_y, p_max_x, p_max_y in perimeter:
        if min_x < p_max_x and max_x > p_min_x and min_y < p_max_y and max_y > p_min_y:
            return False
    return True


def _part2(red_tiles: list[tuple[int, int]]) -> int:
    perimeter = generate_perimeter(red_tiles)

    max_area = 0
    for a, b in itertools.combinations(red_tiles, 2):
        area_ab = area(a, b)
        if area_ab <= max_area:
            continue

        edges = generate_edges(a, b)
        if area_inside_perimeter(edges, perimeter):
            max_area = area_ab

    return max_area


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2025, day=9)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
