"""Day 4: Scratchcards"""


class Card:
    """Represent a scratchcard."""

    game_id: int
    winning_numbers: set[int]
    your_numbers: set[int]

    def __init__(
        self, game_id: int, winning_numbers: set[int], your_numbers: set[int]
    ) -> None:
        self.id = game_id
        self.winning_numbers = winning_numbers
        self.your_numbers = your_numbers

    def matches(self) -> int:
        return len(self.winning_numbers & self.your_numbers)

    def score(self) -> int:
        return 2 ** (self.matches() - 1) if self.matches() > 0 else 0


def _parse(input_data: str) -> list[Card]:
    cards = []
    for line in input_data.splitlines():
        game_id = int(line.split(":")[0].split()[1])
        lists = line.split(":")[-1].split("|")
        winning_numbers = set(map(int, lists[0].split()))
        your_numbers = set(map(int, lists[1].split()))
        cards.append(Card(game_id, winning_numbers, your_numbers))

    return cards


def _part1(parsed_data: list[Card]) -> int:
    return sum(card.score() for card in parsed_data)


def _part2(parsed_data: list[Card]) -> int:
    count = {card.id: 1 for card in parsed_data}
    for card in parsed_data:
        for i in range(card.id + 1, card.id + 1 + card.matches()):
            count[i] += count[card.id]

    return sum(count.values())


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=4)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
