"""Day 7: Camel Cards"""


class Hand:
    """Represents a single hand in camel poker."""

    hand: str
    bid: int

    def __init__(self, hand, bid) -> None:
        self.hand = hand
        self.bid = bid

        self._card_scores = {
            card: score for score, card in enumerate("23456789TJQKA", start=2)
        }

    def __repr__(self) -> str:
        return f"<Hand: hand: {self.hand}, bid: {self.bid}>"

    def score(self, joker: int) -> int:
        self._card_scores["J"] = joker
        card_score = [self._card_scores[x] for x in self.hand]

        #
        # Determine the frequency of each card, taking out Jokers as multipliers for the best card.
        #

        frequency = [0] * 15  # note score is from 1 up to 14
        for x in card_score:
            frequency[x] += 1

        j = frequency[1]
        frequency[1] = 0
        frequency.sort()
        frequency.reverse()
        frequency[0] += j

        #
        # Using the frequency and card score, generate an overall score for the hand.
        # Frequency is limited to 5 cards (3 bits), score is limited to 14 (4 bits).
        #

        score = 0
        for f in frequency[0:5]:
            score = (score << 3) + f
        for d in card_score:
            score = (score << 4) + d
        return score


def _parse(input_data: str) -> list[Hand]:
    result = []
    for line in input_data.splitlines():
        hand, bid = line.split(" ")
        result.append(Hand(hand, int(bid)))

    return result


def _score_hands(hands: list[Hand], joker: int) -> int:
    scored_hands = []
    for hand in hands:
        scored_hands.append((hand.score(joker), hand.bid))
    scored_hands.sort()

    return sum((n + 1) * bid for n, (_, bid) in enumerate(scored_hands))


def _part1(parsed_data: list[Hand]) -> int:
    return _score_hands(parsed_data, 11)


def _part2(parsed_data: list[Hand]) -> int:
    return _score_hands(parsed_data, 1)


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=7)
    example = puzzle.examples[0]
    example_input = example.input_data

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
