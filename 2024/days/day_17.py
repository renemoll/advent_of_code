"""Day 17: Chronospatial Computer"""


import enum
from .utilities import parse_ints, take_n


class Opcode(enum.Enum):
    """Represents the different opcodes."""

    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


class Instruction:
    """Represents a single instruction."""

    opcode: int
    operand: int

    def __init__(self, opcode: Opcode, operand: int):
        self.opcode = opcode
        self.operand = operand

    def __repr__(self):
        return f"<Instruction op: {self.opcode}, arg: {self.operand}>"


class Processor:
    """Single processor emulator, executing instructions."""

    ip: int

    def __init__(self, instructions: list[Instruction], registers: dict):
        self.ip = 0
        self.instructions = instructions
        self.registers = registers
        self.output = []

    def _combo(self, operand):
        if 0 <= operand < 4:
            return operand
        if operand == 4:
            return self.registers["A"]
        if operand == 5:
            return self.registers["B"]
        if operand == 6:
            return self.registers["C"]
        return None

    def _execute(self, instruction):
        jump = None
        match instruction.opcode:
            case Opcode.ADV:
                self.registers["A"] = self.registers["A"] // 2 ** self._combo(
                    instruction.operand
                )
            case Opcode.BXL:
                self.registers["B"] = self.registers["B"] ^ instruction.operand
            case Opcode.BST:
                self.registers["B"] = self._combo(instruction.operand) % 8
            case Opcode.JNZ:
                if self.registers["A"] != 0:
                    jump = (
                        instruction.operand // 2
                    )  # divide by two as I parse the instruction with the operand in one
            case Opcode.BXC:
                self.registers["B"] = self.registers["B"] ^ self.registers["C"]
            case Opcode.OUT:
                self.output.append(self._combo(instruction.operand) % 8)
            case Opcode.BDV:
                self.registers["B"] = self.registers["A"] // 2 ** self._combo(
                    instruction.operand
                )
            case Opcode.CDV:
                self.registers["C"] = self.registers["A"] // 2 ** self._combo(
                    instruction.operand
                )
        return jump

    def run(self):
        while self.ip < len(self.instructions):
            jump = self._execute(self.instructions[self.ip])
            self.ip = self.ip + 1 if jump is None else jump
        return self.output

    def reset(self):
        self.registers["A"] = 0
        self.registers["B"] = 0
        self.registers["C"] = 0
        self.ip = 0
        self.output = []


def _parse(input_data: str):
    sections = input_data.split("\n\n")

    registers = dict(zip("ABC", parse_ints(sections[0])))
    instructions = []
    for op, arg in take_n(parse_ints(sections[1]), 2):
        instructions.append(Instruction(Opcode(op), arg))

    return Processor(instructions, registers), parse_ints(sections[1])


def _part1(parsed_input: Processor) -> int:
    pc, _ = parsed_input
    return ",".join(str(x) for x in pc.run())


def _part2(parsed_input) -> int:
    pc, _ = parsed_input

    return pc.ip


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=17)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
