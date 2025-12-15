"""Day 8: Playground

Part 1:
    Given a list of coordinates (nodes), the goal is to find the 3 largest graphs that can be formed.

    To solve this, we model each coordinate as a node in a graph. Next, we reduce the number of graphs by connecting
    nodes together through the shortest paths possible until we reach the maximum connections.

Part 2:
    Instead of forming multiple graphs, all nodes are to be connected into a single graph using the shortest paths
    possible. We need to find the last two nodes that were connected together.

Improvements:
    * Simplify the data structure by giving each pair and distance a unique entry in a list. This avoids the need for
      sets and dictionaries.
    * Additionally, make connections by using identifiers (indices) instead of the actual Coordinate3D objects. This
      avoids the need for hashing and equality checks on the objects.
    * Sort the list of distances once and then iterate over it, instead of searching for the minimum distance each time.

Discarded alternative ideas:
    * Turns out there is an algorithm for the "Closest Pair Problem" and has well-known efficient solutions.
      While this seems interesting, it would still have to be executed N times. My intuition is that this would make
      the overall complexity too high.
"""

import math
import functools


class Coordinate3D:
    """A 3D coordinate."""

    __slots__ = ("x", "y", "z")

    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"<Coordinate3D x={self.x}, y={self.y}, z={self.z}>"


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
    return sorted(junction_boxes, key=lambda coord: coord.x)


def calculate_distances(
    junction_boxes: list[Coordinate3D],
) -> list[tuple[int, tuple[int, int]]]:
    """Calculates the squared Euclidean distances between all nodes.

    Args:
        junction_boxes: The list of nodes (3D coordinates).

    Returns:
        A dictionary mapping distances to sets of connections (tuples of box indices).
    """
    result = []
    for i in range(len(junction_boxes)):
        a = junction_boxes[i]
        for j in range(i + 1, len(junction_boxes)):
            b = junction_boxes[j]
            distance = euclidean_distance(a, b)
            result.append((distance, (i, j)))
    return sorted(result, key=lambda item: item[0])


def _part1(junction_boxes: list[Coordinate3D]) -> int:
    circuits = {i: [junction_boxes[i]] for i in range(len(junction_boxes))}
    circuits_lookup = {junction_boxes[i]: i for i in range(len(junction_boxes))}

    distance_pairs = calculate_distances(junction_boxes)
    max_iterations = 1000

    for n in range(max_iterations):
        _, (box1, box2) = distance_pairs[n]
        index1 = circuits_lookup[junction_boxes[box1]]
        index2 = circuits_lookup[junction_boxes[box2]]

        if index1 != index2:
            circuit1 = circuits[index1]
            circuit2 = circuits[index2]

            circuit1.extend(circuit2)
            for box in circuit2:
                circuits_lookup[box] = index1
            del circuits[index2]

    lengths = sorted([len(circuit) for circuit in circuits.values()], reverse=True)
    return math.prod(lengths[:3])


def _part2(junction_boxes: list[Coordinate3D]) -> int:
    circuits = {i: [junction_boxes[i]] for i in range(len(junction_boxes))}
    circuits_lookup = {junction_boxes[i]: i for i in range(len(junction_boxes))}

    distance_pairs = calculate_distances(junction_boxes)

    last_box1 = None
    last_box2 = None

    for n in range(len(distance_pairs)):
        _, (box1, box2) = distance_pairs[n]
        index1 = circuits_lookup[junction_boxes[box1]]
        index2 = circuits_lookup[junction_boxes[box2]]

        if index1 != index2:
            last_box1 = junction_boxes[box1]
            last_box2 = junction_boxes[box2]

            circuit1 = circuits[index1]
            circuit2 = circuits[index2]

            circuit1.extend(circuit2)
            for box in circuit2:
                circuits_lookup[box] = index1
            del circuits[index2]

    return last_box1.x * last_box2.x


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))
