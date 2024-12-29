"""Day 18: RAM Run"""

import heapq
import math

from .utilities import parse_ints, take_n, Coordinate, Grid


def coordinates_to_grid(cs: list[(Coordinate, Coordinate)], limit: int):
    x_max = y_max = 71
    grid = Grid(["." * x_max] * y_max)
    for n, c in enumerate(cs):
        if n >= limit:
            break

        grid.set(c, "#")
    return grid


def dijkstra(grid, start, end):
    queue = [(0, start)]
    heapq.heapify(queue)
    distances = {
        (x, y): math.inf for x in range(grid.columns) for y in range(grid.rows)
    }
    distances[start] = 0
    previous = {(x, y): None for x in range(grid.columns) for y in range(grid.rows)}
    visited = set()

    while queue:
        cost, node = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)

        if node == end:
            return (cost, previous)

        for new_node in grid.neighbours(node, include_diagonals=False):
            if grid.get(new_node) == "#":
                continue

            new_cost = cost + 1

            if new_cost < distances[new_node]:
                distances[new_node] = new_cost
                previous[new_node] = [node]
                heapq.heappush(queue, (new_cost, new_node))
            elif new_cost == distances[new_node]:
                previous[new_node].append(node)

    return (None, previous)


def _parse(input_data: str):
    return [Coordinate(x, y) for x, y in take_n(parse_ints(input_data), 2)]


def _part1(parsed_input) -> int:
    grid = coordinates_to_grid(parsed_input, 1024)

    cost, _ = dijkstra(grid, Coordinate(0, 0), Coordinate(70, 70))
    return cost


def _part2(parsed_input) -> int:
    grid = coordinates_to_grid(parsed_input, 1024)
    cost, _ = dijkstra(grid, Coordinate(0, 0), Coordinate(70, 70))

    remaining_bytes = parsed_input[1024:]
    for c in remaining_bytes:
        grid.set(c, "#")
        cost, _ = dijkstra(grid, Coordinate(0, 0), Coordinate(70, 70))
        if cost is None:
            return c

    return cost


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=18)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
