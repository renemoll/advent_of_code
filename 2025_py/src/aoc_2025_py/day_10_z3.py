"""Day 10: Factory

Part 1:
    We are given several machines, each with a state we need to find, buttons that toggle certain states and a joltage
    requirement. For part 1 we can ignore the joltage requirement.

    The task is to determine the shortest sequence of button presses that will set all status lights to the expected
    state. Note that we can press buttons twice, but this has the effect as not pressing the button, so we only press
    a button once or not at all.

    One way to solve this is to model the machine status and buttons as bits in an integer, where each bit represents a
    status light (0 = off, 1 = on). This way, the result of a button press is a simple XOR operation. Next, we need to
    test all combinations of buttons, while avoiding reverting back into a previous state. This is done using a
    breadth-first search (BFS).
"""

import collections

import z3


class Instruction:
    """A machine instruction."""

    def __init__(
        self,
        lights: list[int],
        buttons: list[list[int]],
        buttons_alt: list[list[int]],
        joltages: str,
    ):
        self.lights = lights
        self.buttons = buttons
        self.buttons_alt = buttons_alt
        self.joltages = joltages

    def __repr__(self):
        return f"<Machine lights={bin(self.lights)}, buttons={[bin(x) for x in self.buttons]}, joltages={self.joltages}>"


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
                buttons_alt=[x[1:-1].split(",") for x in tmp[1:-1]],
                joltages=list(map(int, tmp[-1][1:-1].split(","))),
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
    result = 0
    for instruction in instructions:
        solver = z3.Optimize()
        goal = z3.Int("goal")

        goal_rhs = 0
        constraint_lhs = [0 for x in instruction.joltages]
        for i, button in enumerate(instruction.buttons_alt):
            b = z3.Int(f"b{i}")
            solver.add(b >= 0)
            goal_rhs += b

            for x in button:
                constraint_lhs[int(x)] += b

        solver.add(goal == goal_rhs)

        constraints = [
            lhs == rhs for lhs, rhs in zip(constraint_lhs, instruction.joltages)
        ]
        for c in constraints:
            solver.add(c)
        solver.minimize(goal)
        solver.check()
        result += solver.model()[goal].as_long()
    return result


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))
