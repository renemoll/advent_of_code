# Advent of Code 2024 - Python edition


## Setting up
1. Open this folder in VS Code
1. Re-open the workspace in a dev container
1. Configure the AoC session

## Solving the puzzles

Run a specifc example:
```bash
python3 -m days.day_01
```

Run a specifc day:
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
- redo timing on solution & parts
- profile
```bash
python -m cProfile -s tottime run.py -d 01 > profile.txt
```
