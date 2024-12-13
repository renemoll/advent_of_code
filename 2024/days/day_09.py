"""Day 9: Disk Fragmenter"""

import enum
import typing
import collections
import copy


def is_even(n):
    return n % 2 == 0


class SectionType(enum.Enum):
    """Section type"""

    FILE = 1
    SPACE = 2


class Section:
    """Represents a section (span) of disk space"""

    def __init__(
        self, size: int, section_type: SectionType, file_id: typing.Optional[int] = None
    ):
        self.size = size
        self.type = section_type
        self.file_id = file_id

    def __repr__(self) -> str:
        return f"<Section type: {self.type}, size: {self.size}, id: {self.file_id}>"

    def __str__(self) -> str:
        return self.size * [".", str(self.file_id)][self.type == SectionType.FILE]


def _parse(input_data: str):
    file_id = 0
    result = collections.deque()
    for n, c in enumerate(input_data):
        if is_even(n):
            result.append(Section(int(c), SectionType.FILE, file_id))
            file_id += 1
        else:
            result.append(Section(int(c), SectionType.SPACE))
    return result


def _part1(parsed_input) -> int:
    partition = copy.deepcopy(parsed_input)
    write_index = (
        1  # The first entry is defined to be a file, so we can start at index 1
    )
    read_index = len(partition) - 1

    while read_index > write_index:
        if partition[read_index].type == SectionType.SPACE:
            partition.pop()
            read_index -= 1

        available_size = partition[write_index].size
        required_size = partition[read_index].size

        size = min(available_size, required_size)
        available_size -= size
        required_size -= size

        if available_size == 0:
            # We completely fill the available space
            partition[write_index] = Section(
                size, SectionType.FILE, partition[read_index].file_id
            )
            write_index += 2
        else:
            # We partially fill the available space
            partition.insert(
                write_index,
                Section(size, SectionType.FILE, partition[read_index].file_id),
            )
            write_index += 1
            partition[write_index].size = available_size

        if required_size == 0:
            # The last file is completely moved
            partition.pop()
            read_index -= 1
        else:
            # The last file is partially moved
            partition[read_index].size = required_size

    result = 0
    offset = 0
    for section in partition:
        if section.type == SectionType.FILE:
            for i in range(section.size):
                result += (offset + i) * section.file_id
        offset += section.size

    return result


def _part2(parsed_input) -> int:
    """TODO: improve as list manipulation is likely slow
    Idea: next to the partition map, keep track of the spaces/files by [partition idx] = space => sort and fill?
    TODO: how to avoid additional insertions?
    """
    partition = list(parsed_input)
    write_index = (
        1  # The first entry is defined to be a file, so we can start at index 1
    )
    read_index = len(partition) - 1

    while read_index > 1:
        if write_index > read_index:
            write_index = 1
            read_index -= 1

        # pprint.pprint(f"{write_index=}, {read_index=}")
        # pprint.pprint("".join([str(s) for s in partition]))

        if partition[read_index].type == SectionType.SPACE:
            read_index -= 1
            continue

        if partition[write_index].type == SectionType.FILE:
            write_index += 1
            continue

        available_size = partition[write_index].size
        required_size = partition[read_index].size

        if available_size >= required_size:
            partition.insert(
                write_index,
                Section(
                    partition[read_index].size,
                    SectionType.FILE,
                    partition[read_index].file_id,
                ),
            )
            write_index += 1
            partition[write_index].size = available_size - required_size
            write_index = 1

            read_index += 1  # to compensate for the insertion
            partition[read_index] = Section(required_size, SectionType.SPACE)
            # read_index -= 2

            # partition.pop()
        else:
            # read_index -= 1
            write_index += 1

    # pprint.pprint("".join([str(s) for s in partition]))

    result = 0
    offset = 0
    for section in partition:
        if section.type == SectionType.FILE:
            for i in range(section.size):
                result += (offset + i) * section.file_id
        offset += section.size

    return result


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=9)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
