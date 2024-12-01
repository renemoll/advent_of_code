"""Day 5: If You Give A Seed A Fertilizer"""

from .utilities import pairwise_without_overlap


class Rule:
    """Represents a translation rule."""

    destination: int
    source: range

    def __init__(self, destination, source) -> None:
        self.destination = destination
        self.source = source

    def __repr__(self) -> str:
        return f"<Rule: destination: {self.destination}, source: {self.source}>"


class CategoryMap:
    """Maps a location from source to destination following a list of rules."""

    rules: list[Rule]

    def __init__(self) -> None:
        self.rules = []

    def add_rule(self, rule: Rule) -> None:
        self.rules.append(rule)
        self.rules.sort(key=lambda x: x.source.start)

    def transform_location(self, location: int) -> int:
        for rule in self.rules:
            if location in rule.source:
                location = rule.destination + location - rule.source.start
                break
        return location

    def transform_range(self, locations: list[range]) -> list[range]:
        results = []

        for rule in self.rules:
            new_ranges = []
            while locations:
                current_range = locations.pop()

                #
                # Find the interval(s) which overlap with the current rule
                # - left: internal before the rule, may overlap with a different rule
                # - mid: internal overlapping with the rule
                # - right: internal after the rule, may overlap with a different rule
                #

                left = range(
                    current_range.start, min(rule.source.start, current_range.stop)
                )
                if left.stop > left.start:
                    new_ranges.append(left)

                mid = range(
                    max(current_range.start, rule.source.start),
                    min(current_range.stop, rule.source.stop),
                )
                if mid.stop > mid.start:
                    results.append(
                        range(
                            mid.start - rule.source.start + rule.destination,
                            mid.stop - rule.source.start + rule.destination,
                        )
                    )

                right = range(
                    max(current_range.start, rule.source.stop), current_range.stop
                )
                if right.stop > right.start:
                    new_ranges.append(right)

            locations += new_ranges

        return results + new_ranges


def _parse(input_lines: list[str]) -> tuple[list[int], list[CategoryMap]]:
    input_lines = "\n".join(input_lines)
    sections = input_lines.split("\n\n")
    seeds = list(map(int, sections[0].split(": ")[1].split()))

    maps = []
    for section in sections[1:]:
        lines = section.splitlines()[1:]
        garden_map = CategoryMap()
        for line in lines:
            x = list(map(int, line.split()))
            garden_map.add_rule(Rule(x[0], range(x[1], x[1] + x[2])))
        maps.append(garden_map)

    return (seeds, maps)


def _locate_seed(maps, seed):
    location = seed
    for mapping in maps:
        location = mapping.transform_location(location)
    return location


def _part1(parsed_data: tuple[list[int], list[CategoryMap]]) -> int:
    seeds, maps = parsed_data
    return min(_locate_seed(maps, seed) for seed in seeds)


def _part2(parsed_data: tuple[list[int], list[CategoryMap]]) -> int:
    seeds, maps = parsed_data
    locations = []
    for start, length in pairwise_without_overlap(seeds):
        seed_range = range(start, start + length)
        seed_ranges = [seed_range]
        for mapping in maps:
            seed_ranges = mapping.transform_range(seed_ranges)
        locations.append(min(x.start for x in seed_ranges))
    return min(locations)


def solve(input_lines: list[str]) -> tuple[int, int]:
    parsed_input = _parse(input_lines)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=5)
    example = puzzle.examples[0]
    example_input = example.input_data.splitlines()

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
