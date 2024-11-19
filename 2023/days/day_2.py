from aocd import get_data

def _line_to_game(line):
    game, draws = line.split(":")
    id = int(game[4:])

    result = []
    for draw in draws.split(";"):
        dice = draw.split(",")
        r = {'red': 0, 'green': 0, 'blue': 0}
        for d in dice:
            n, c = d.strip().split(" ")
            r[c] = int(n)
        result.append(r)
    return (id, result)

def _game_within_limit(game):
    limit = {
        'red': 12,
        'green': 13,
        'blue': 14
    }
    for c,v in game.items():
        if v > limit[c]:
            return False
    return True

def _part1(input_lines):
    result = 0
    for line in input_lines:
        game = _line_to_game(line)
        if all([_game_within_limit(x) for x in game[1]]):
            result += game[0]
    return result

def _part2(input_lines):
    result = 0
    for line in input_lines:
        game = _line_to_game(line)
        r = max([x['red'] for x in game[1]])
        g = max([x['green'] for x in game[1]])
        b = max([x['blue'] for x in game[1]])
        result += r*g*b
    return result

def solve(input_lines):
    return (_part1(input_lines), _part2(input_lines))

if __name__ == "__main__":
    from aocd.models import Puzzle
    puzzle = Puzzle(year=2023, day=2)
    data = puzzle.examples
    print(f"Part 1: {_part1(data[0].input_data.splitlines())}, expecting: {data[0].answer_a}")
    print(f"Part 2: {_part2(data[0].input_data.splitlines())}, expecting: {data[0].answer_b}")
