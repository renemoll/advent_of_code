"""Day 8: Playground

Part 1:
    We are given a list of 3D coordinates representing the locations of junking boxes. These junction boxes need to be connected together to form circuits.
    Our tasks is to find the 3 largest circuits that can be made by connecting boxes together through the shortest paths possible.

    To solve this, we model each box as a circuit containing a single box. Next, we reduce the number of circuits by connecting boxes together through the shortest paths possible until no more connections can be made.

Part 2:
    There are not enough cables to connect all the circuits, so now we are connecting all the boxes together into a single circuit using the shortest paths possible.
"""

import itertools
import math


class Coordinate3D:
    """A 3D coordinate."""

    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"<Coordinate3D x={self.x}, y={self.y}, z={self.z}>"


def create_connection(box1: int, box2: int) -> tuple[int, int]:
    return (min(box1, box2), max(box1, box2))


def euclidean_distance(lhs: Coordinate3D, rhs: Coordinate3D) -> int:
    """Calculate the squared Euclidean distance between two 3D coordinates.

    Note:
        Omitting the square root for performance reasons (not needed).
    """
    return (lhs.x - rhs.x) ** 2 + (lhs.y - rhs.y) ** 2 + (lhs.z - rhs.z) ** 2


def _parse(input_data: str) -> list[Coordinate3D]:
    return [
        Coordinate3D(*map(int, line.split(","))) for line in input_data.splitlines()
    ]


def find_distances(boxes: list[Coordinate3D]) -> dict[int, set[tuple[int, int]]]:
    distances = {}
    for a, b in itertools.combinations(range(len(boxes)), 2):
        distance = euclidean_distance(boxes[a], boxes[b])
        if distance not in distances:
            distances[distance] = set([create_connection(a, b)])
        else:
            distances[distance].add(create_connection(a, b))
    return distances


def _part1(boxes: list[Coordinate3D]) -> int:
    circuits = {i: [boxes[i]] for i in range(len(boxes))}
    circuits_lookup = {boxes[i]: i for i in range(len(boxes))}
    distances = find_distances(boxes)

    n = 0
    while distances:
        if n >= 1000:
            break
        min_distance = min(distances.keys())
        connections = distances.pop(min_distance)
        n += 1

        for box1, box2 in connections:
            circuit1_index = circuits_lookup[boxes[box1]]
            circuit2_index = circuits_lookup[boxes[box2]]

            if circuit1_index != circuit2_index:
                circuit1 = circuits[circuit1_index]
                circuit2 = circuits[circuit2_index]

                circuit1.extend(circuit2)

                for box in circuit2:
                    circuits_lookup[box] = circuit1_index

                del circuits[circuit2_index]

    lengths = sorted([len(circuit) for circuit in circuits.values()], reverse=True)
    return math.prod(lengths[:3])


def _part2(boxes: list[Coordinate3D]) -> int:
    circuits = {i: [boxes[i]] for i in range(len(boxes))}
    circuits_lookup = {boxes[i]: i for i in range(len(boxes))}
    distances = find_distances(boxes)

    last_box1 = None
    last_box2 = None

    while distances:
        min_distance = min(distances.keys())
        connections = distances.pop(min_distance)

        for box1, box2 in connections:
            circuit1_index = circuits_lookup[boxes[box1]]
            circuit2_index = circuits_lookup[boxes[box2]]

            if circuit1_index != circuit2_index:
                last_box1 = boxes[box1]
                last_box2 = boxes[box2]

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


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2025, day=8)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
