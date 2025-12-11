"""Day 10: Factory

Part 1:
    We end up in a factory with several machines, all of them are offline and need to be initialized. Each machine has
    several status lights and buttons, where the buttons can toggle one or more status lights. To initialize a machine,
    we need to match the machine status with the expected status, this means finding the right sequence of button
    presses.

    Our task is to determine the smallest sequence of button presses needed to activate all machines.

    Note that we can press buttons twice, but this has the effect as not pressing the button, so we only press a button
    once or not at all.

    One way to solve this is to model the machine status and buttons as bits in an integer, where each bit represents a
    status light (0 = off, 1 = on). This way, the result of a button press is a simple XOR operation. Next, we need to
    test all combinations of buttons, while avoiding reverting back into a previous state. This is done using a
    breadth-first search (BFS).

"""

import collections
import pprint


class Instruction:
    """A machine instruction."""

    def __init__(self, lights: list[int], buttons: list[list[int]], joltage: str):
        self.lights = lights
        self.buttons = buttons
        self.joltage = joltage

    def __repr__(self):
        return f"<Machine lights={bin(self.lights)}, buttons={[bin(x) for x in self.buttons]}, joltage={self.joltage}>"


def press_button(status: list[int], button: list[int]):
    result = status.copy()
    try:
        for idx in button:
            result[idx] = result[idx] ^ 1
    except IndexError:
        pass
    return result


def _parse(input_data: str) -> list[Instruction]:
    instructions = input_data.splitlines()
    result = []
    for line in instructions:
        tmp = line.split(" ")
        result.append(
            Instruction(
                lights=int(tmp[0][1:-1].replace(".", "0").replace("#", "1")[::-1], 2),
                buttons=[
                    sum(map(lambda x: 2 ** int(x), x[1:-1].split(",")))
                    for x in tmp[1:-1]
                ],
                joltage=tmp[-1],
            )
        )
    return result


def find_sequence(lights: int, buttons: list[int]) -> int:
    """Find a sequence of button presses that matches the goal status."""

    start = 0
    queue = collections.deque([(start, 0)])
    visited = set([start])

    while queue:
        value, steps = queue.popleft()
        if value == lights:
            return steps

        for button in buttons:
            next_value = value ^ button
            if next_value not in visited:
                visited.add(next_value)
                queue.append((next_value, steps + 1))

    return None


def _part1(instructions: list[Instruction]) -> int:
    result = 0
    for instruction in instructions:
        steps = find_sequence(instruction.lights, instruction.buttons)
        result += steps

    return result


def _part2(instructions: list[Instruction]) -> int:
    pprint.pprint(instructions)
    return 0


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2025, day=10)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
