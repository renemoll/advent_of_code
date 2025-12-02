# Advent of Code 2024 - Python edition

This year I decided to complete the challenge in Python. My goal for this year is to solve all puzzles and experience to solve 2023 as well.

## Setting up the development environment

Development is performed in VS Code.

To get started:
1. Open this folder in VS Code
1. Re-open the workspace in a development container
1. Configure the AoC session in the terminal

## Solving the puzzles

Run a specific example:
```bash
python3 -m days.day_01
```

Run a specific day:
```bash
python3 run.py -d 01
```

Run all days:
```bash
python3 run.py
```

## Timing

I time the complete solve step, from reading in the input file to solving both parts combined. In my opinion, parsing the input is part of the solution.

## Todo
- tests for the utilities
- multiple examples
- check answers
- redo timing on solution & parts
- profile
```bash
python -m cProfile -s tottime run.py -d 01 > profile.txt
```
