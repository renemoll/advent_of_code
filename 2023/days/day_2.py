"""Day 2: Cube Conundrum"""


def _line_to_game(line):
    game, sets = line.split(":")
    number = int(game[4:])

    results = []
    for s in sets.split(";"):
        cubes = s.split(",")
        result = {"red": 0, "green": 0, "blue": 0}
        for x in cubes:
            amount, colour = x.strip().split(" ")
            result[colour] = int(amount)
        results.append(result)

    return (number, results)


def _game_within_limit(game):
    limit = {"red": 12, "green": 13, "blue": 14}
    for colour, amount in game.items():
        if amount > limit[colour]:
            return False
    return True


def _part1(input_lines):
    result = 0
    for line in input_lines:
        game = _line_to_game(line)
        if all(_game_within_limit(x) for x in game[1]):
            result += game[0]
    return result


def _part2(input_lines):
    result = 0
    for line in input_lines:
        game = _line_to_game(line)
        r = max(x["red"] for x in game[1])
        g = max(x["green"] for x in game[1])
        b = max(x["blue"] for x in game[1])
        result += r * g * b
    return result


def solve(input_lines):
    return (_part1(input_lines), _part2(input_lines))


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=2)
    example = puzzle.examples[0]
    example_input = example.input_data.splitlines()

    solution = solve(example_input)
    print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
    print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
