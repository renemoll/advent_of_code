"""Day 16: Reindeer Maze"""

import math
import enum
import heapq

from .utilities import Grid, SparseGrid, Coordinate


class Orientation(enum.Enum):
    """Represents an orientation."""

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @staticmethod
    def rotate(ori: "Orientation", steps: int):
        return Orientation((ori.value + steps) % 4)

    @staticmethod
    def vector(ori: "Orientation"):
        return [
            Coordinate(0, -1),  # North
            Coordinate(1, 0),  # East
            Coordinate(0, 1),  # South
            Coordinate(-1, 0),  # West
        ][ori.value]

    def __lt__(self, other: "Orientation") -> bool:
        return self.value < other.value


def dijkstra(grid, start, end):
    queue = [(0, (start, Orientation.EAST))]
    heapq.heapify(queue)
    distances = {
        (x, o): math.inf
        for x in grid.keys()
        for o in [
            Orientation.NORTH,
            Orientation.EAST,
            Orientation.SOUTH,
            Orientation.WEST,
        ]
    }
    distances[(start, Orientation.EAST)] = 0
    previous = {x: None for x in grid.keys()}
    # previous = {(x, o): None for x in grid.keys() for o in [Orientation.NORTH, Orientation.EAST, Orientation.SOUTH, Orientation.WEST]}
    visited = set()
    valid_nodes = list(grid.keys())

    while queue:
        cost, (node, direction) = heapq.heappop(queue)
        if (node, direction) in visited:
            continue
        visited.add((node, direction))

        if node == end:
            return (cost, previous)

        new_directions = [
            direction,
            Orientation.rotate(direction, 1),
            Orientation.rotate(direction, -1),
        ]
        for new_direction in new_directions:
            new_node = node + Orientation.vector(new_direction)
            new_cost = cost + (1 if new_direction == direction else 1001)

            # if (new_node, new_direction) in visited:
            #     continue
            if not new_node in valid_nodes:
                continue

            if new_cost < distances[(new_node, new_direction)]:
                distances[(new_node, new_direction)] = new_cost
                previous[new_node] = [(node, direction)]
                heapq.heappush(queue, (new_cost, (new_node, new_direction)))
            elif new_cost == distances[(new_node, new_direction)]:
                previous[new_node].append((node, direction))

    return (None, previous)


def _parse(input_data: str):
    grid = Grid(input_data.splitlines())
    start = grid.find("S")
    end = grid.find("E")
    sparse_grid = SparseGrid(input_data.splitlines(), lambda x: x != "#")
    return (sparse_grid, start, end)


def solve(input_data: str) -> tuple[int, int]:
    grid, start, end = _parse(input_data)

    part1, _ = dijkstra(grid, start, end)

    # return (0,0)
    # queue = [end]
    visited = set()
    # path = [end]
    # node = end
    # while queue:
    #     node = queue.pop(0)
    #     visited.add(node)
    #     for prev_node, direction in paths[node]:
    #         queue.append(prev_node)

    return (part1, len(visited))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=16)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
