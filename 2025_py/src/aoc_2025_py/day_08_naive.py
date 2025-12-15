"""Day 8: Playground

Part 1:
    Given a list of coordinates (nodes), the goal is to find the 3 largest graphs that can be formed.

    To solve this, we model each coordinate as a node in a graph. Next, we reduce the number of graphs by connecting
    nodes together through the shortest paths possible until we reach the maximum connections.

Part 2:
    Instead of forming multiple graphs, all nodes are to be connected into a single graph using the shortest paths
    possible. We need to find the last two nodes that were connected together.
"""

import itertools
import math
import functools


class Coordinate3D:
    """A 3D coordinate."""

    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"<Coordinate3D x={self.x}, y={self.y}, z={self.z}>"


@functools.cache
def create_connection(box1: int, box2: int) -> tuple[int, int]:
    return (min(box1, box2), max(box1, box2))


@functools.cache
def euclidean_distance(lhs: Coordinate3D, rhs: Coordinate3D) -> int:
    """Calculate the squared Euclidean distance between two 3D coordinates.

    Args:
        lhs: The left-hand side coordinate.
        rhs: The right-hand side coordinate.

    Returns:
        The squared Euclidean distance between the two coordinates.

    Note:
        Omitting the square root for performance reasons (not needed).
    """
    return (lhs.x - rhs.x) ** 2 + (lhs.y - rhs.y) ** 2 + (lhs.z - rhs.z) ** 2


def _parse(input_data: str) -> list[Coordinate3D]:
    junction_boxes = [
        Coordinate3D(*map(int, line.split(","))) for line in input_data.splitlines()
    ]
    return junction_boxes


def find_distances(boxes: list[Coordinate3D]) -> dict[int, set[tuple[int, int]]]:
    """Find the squared Euclidean distances between all boxes.

    Args:
        boxes: The list of boxes (3D coordinates).

    Returns:
        A dictionary mapping distances to sets of connections (tuples of box indices).
    """
    distances = {}
    for a, b in itertools.combinations(range(len(boxes)), 2):
        distance = euclidean_distance(boxes[a], boxes[b])
        if distance not in distances:
            distances[distance] = set([create_connection(a, b)])
        else:
            distances[distance].add(create_connection(a, b))
    return distances


def _part1(junction_boxes: list[Coordinate3D]) -> int:
    circuits = {i: [junction_boxes[i]] for i in range(len(junction_boxes))}
    circuits_lookup = {junction_boxes[i]: i for i in range(len(junction_boxes))}
    distances = find_distances(junction_boxes)

    n = 0
    while distances:
        if n >= 1000:
            break
        min_distance = min(distances.keys())
        connections = distances.pop(min_distance)
        n += 1

        for box1, box2 in connections:
            circuit1_index = circuits_lookup[junction_boxes[box1]]
            circuit2_index = circuits_lookup[junction_boxes[box2]]

            if circuit1_index != circuit2_index:
                circuit1 = circuits[circuit1_index]
                circuit2 = circuits[circuit2_index]

                circuit1.extend(circuit2)

                for box in circuit2:
                    circuits_lookup[box] = circuit1_index

                del circuits[circuit2_index]

    lengths = sorted([len(circuit) for circuit in circuits.values()], reverse=True)
    return math.prod(lengths[:3])


def _part2(junction_boxes: list[Coordinate3D]) -> int:
    circuits = {i: [junction_boxes[i]] for i in range(len(junction_boxes))}
    circuits_lookup = {junction_boxes[i]: i for i in range(len(junction_boxes))}
    distances = find_distances(junction_boxes)

    last_box1 = None
    last_box2 = None

    while distances:
        min_distance = min(distances.keys())
        connections = distances.pop(min_distance)

        for box1, box2 in connections:
            circuit1_index = circuits_lookup[junction_boxes[box1]]
            circuit2_index = circuits_lookup[junction_boxes[box2]]

            if circuit1_index != circuit2_index:
                last_box1 = junction_boxes[box1]
                last_box2 = junction_boxes[box2]

                circuit1 = circuits[circuit1_index]
                circuit2 = circuits[circuit2_index]

                circuit1.extend(circuit2)

                for box in circuit2:
                    circuits_lookup[box] = circuit1_index

                del circuits[circuit2_index]

    return last_box1.x * last_box2.x


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))
