"""Day 20: Race Condition"""

import heapq
import math
import collections

from .utilities import Grid


def _parse(input_data: str):
    grid = Grid(input_data.splitlines())
    start = grid.find("S")
    end = grid.find("E")

    return (grid, start, end)


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
                previous[new_node] = node
                heapq.heappush(queue, (new_cost, new_node))

    return (None, previous)


def generate_path(previous, start, end) -> list:
    node = end
    path = [node]
    while True:
        next_node = previous[node]
        if next_node is None:
            break

        path.append(next_node)
        if next_node == start:
            break
        node = next_node

    return path


def cheat_path(path, jump_from, jump_to) -> int:
    i_start = path.index(jump_from)
    i_end = path.index(jump_to)
    return (i_start - i_end) - 2


def _part1(parsed_input) -> int:
    grid, start, end = parsed_input

    _, previous = dijkstra(grid, start, end)
    path = generate_path(previous, start, end)
    path.reverse()

    cheat_options = set()
    for node in path:
        walls = [
            x
            for x in grid.neighbours(node, include_diagonals=False)
            if grid.get(x) == "#"
        ]
        for w in walls:
            options = [
                x
                for x in grid.neighbours(w, include_diagonals=False)
                if x in path and x != node
            ]
            for option in options:
                cheat_options.add((node, option))

    count = collections.Counter()
    for option in cheat_options:
        saves = cheat_path(path, option[0], option[1])
        if saves > 0:
            count[saves] += 1

    result = 0
    for k, v in count.items():
        if k >= 100:
            result += v

    return result


def _part2(parsed_input) -> int:
    grid, start, end = parsed_input

    _, previous = dijkstra(grid, start, end)
    path = generate_path(previous, start, end)
    path.reverse()

    return 0


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=20)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
