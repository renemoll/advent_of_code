"""Day 24: Crossed Wires"""

# import pprint
import re


class Operation:
    """Represent a single operation."""

    def __init__(self, input1, operation, input2, output):
        self.input = [input1, input2]
        self.operation = operation
        self.output = output

    def can_execute(self, wires):
        for x in self.input:
            if not x in wires:
                # pprint.pprint(f"Cannot execute {self.input=}, {self.operation}, {self.output}")
                return False
        return True

    def execute(self, wires):
        # pprint.pprint(f"Executing {self.input=}, {self.operation}, {self.output}")
        i1 = wires[self.input[0]]
        i2 = wires[self.input[1]]

        match self.operation:
            case "AND":
                wires[self.output] = i1 and i2
            case "OR":
                wires[self.output] = i1 or i2
            case "XOR":
                wires[self.output] = i1 ^ i2


class Circuit:
    """Represent a circuit of logic gates."""

    def __init__(self, wires, operations):
        self.wires = wires
        self.operations = operations

    def solve(self):
        while self.operations:
            for i in range(len(self.operations) - 1, -1, -1):
                if self.operations[i].can_execute(self.wires):
                    self.operations[i].execute(self.wires)
                    del self.operations[i]

        # pprint.pprint(self.wires)

        outputs = {name: state for name, state in self.wires.items() if name[0] == "z"}
        indices = outputs.keys()
        indices = sorted(indices, reverse=True)
        binary = "".join(str(outputs[x]) for x in indices)
        return int(binary, 2)


def _parse(input_data: str):
    sections = input_data.split("\n\n")

    wires = {(r := x.split(":"))[0]: int(r[1]) for x in sections[0].splitlines()}
    operations = [
        Operation(*x)
        for x in re.findall(r"(\w{3}) (\w{2,3}) (\w{3}) -> (\w{3})", sections[1])
    ]
    return Circuit(wires, operations)


def _part1(parsed_input) -> int:
    circuit = parsed_input
    return circuit.solve()


def _part2(parsed_input) -> int:
    _ = parsed_input
    return 0


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=24)
    example = puzzle.examples[1]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
