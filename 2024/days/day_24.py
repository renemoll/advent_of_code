"""Day 24: Crossed Wires"""

import copy
import enum
import re

from .utilities import parse_ints


class Logic(enum.Enum):
    """Identifier for the diffent logic date functions."""

    AND = 1
    OR = 2
    XOR = 3


class Gate:
    """Represent a logic gate."""

    def __init__(self, input1, operation, input2, output):
        self.inputs = [input1, input2]
        self.operation = Logic[operation]
        self.output = output

    def __repr__(self):
        return f"<Gate operation: {self.operation}, inputs:{self.inputs}, output:{self.output}>"

    def can_execute(self, wires):
        for x in self.inputs:
            if not x in wires:
                return False
        return True

    def execute(self, wires):
        i1 = wires[self.inputs[0]]
        i2 = wires[self.inputs[1]]

        match self.operation:
            case Logic.AND:
                wires[self.output] = i1 and i2
            case Logic.OR:
                wires[self.output] = i1 or i2
            case Logic.XOR:
                wires[self.output] = i1 ^ i2


class Circuit:
    """Represent a circuit of logic gates."""

    def __init__(self, inputs, gates):
        # self.inputs = inputs
        # self.wires = copy.deepcopy(inputs)
        self.wires = inputs
        self.gates = gates

    def solve(self):
        gates = copy.deepcopy(self.gates)
        while gates:
            for i in range(len(gates) - 1, -1, -1):
                if gates[i].can_execute(self.wires):
                    gates[i].execute(self.wires)
                    del gates[i]

        indices = sorted(
            [name for name in self.wires.keys() if name[0] == "z"], reverse=True
        )
        binary = "".join(str(self.wires[x]) for x in indices)
        return int(binary, 2)

    def find_gate_by_input(self, gate, name):
        for g in self.gates:
            if g.operation == gate and name in g.inputs:
                return g
        return None


def _parse(input_data: str):
    sections = input_data.split("\n\n")

    wires = {(r := x.split(":"))[0]: int(r[1]) for x in sections[0].splitlines()}
    gates = [
        Gate(*x)
        for x in re.findall(r"(\w{3}) (\w{2,3}) (\w{3}) -> (\w{3})", sections[1])
    ]
    return Circuit(wires, gates)


def _part1(parsed_input) -> int:
    circuit = parsed_input
    return circuit.solve()


def _part2(parsed_input) -> int:
    """
    Options:
    - go through the input manually
    - draw it out for visual inspection
    - find the pattern and verify that the circuit follows the pattern

    We know the circuit represents an adder, in logic gates this is an full adder as we generate and take the carry bit into account.
    Special cases are the first and last adders, as the first does not take an carry in and the last connects the carry out to the last output bit.

    For a full adder, both inputs xNN and yNN go to and XOR and AND gate. The result of the XOR gate feed into the next state of an AND and XOR togehter with the carry in from the previous stage.
    The result of the last XOR is output zNN, and the result of both AND gates if fed to an OR gate to generate the carry out.

    """
    circuit = parsed_input

    def find_valid_gate(logic_type, inputs):
        options = [circuit.find_gate_by_input(logic_type, wire) for wire in inputs]
        options = [x for x in options if x is not None]
        return options[0]

    xs = sorted([x for x in circuit.wires.keys() if x[0] == "x"])
    carry = {}
    swapped = set()
    for i, x in enumerate(xs):
        number = parse_ints(x)[0]
        output = f"z{number:02d}"

        # Input stage
        input_xor = circuit.find_gate_by_input(Logic.XOR, x)
        input_and = circuit.find_gate_by_input(Logic.AND, x)

        if i == 0:
            # x00/y00 are an edge case as it does take an carry bit as input
            if input_xor.output != output:
                swapped.add(input_xor.output)
                swapped.add(output)
                carry[i] = input_xor.output
            else:
                carry[i] = input_and.output
        else:
            carry_in = carry[i - 1]
            output_xor = find_valid_gate(Logic.XOR, [input_xor.output, carry_in])
            output_and = find_valid_gate(Logic.AND, [input_xor.output, carry_in])
            output_or = find_valid_gate(Logic.OR, [input_and.output, output_and.output])

            if output_xor.output != output:
                swapped.add(output)
                swapped.add(output_xor.output)

            xor_diff = set([input_xor.output, carry_in]).difference(output_xor.inputs)
            swapped.update(xor_diff)
            and_diff = set([input_xor.output, carry_in]).difference(output_and.inputs)
            swapped.update(and_diff)
            or_diff = set([input_and.output, output_and.output]).difference(
                output_or.inputs
            )
            swapped.update(or_diff)

            #  last OR is also an output, but we don't need to process it...
            if output_or.output == output:
                carry[i] = output_xor.output
            else:
                carry[i] = output_or.output

    swapped = ",".join(sorted(swapped))
    return swapped


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
