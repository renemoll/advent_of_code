import pathlib

from utilities_py import aoc_runner


def main() -> None:
    project_path = pathlib.Path(__file__).parent.resolve()
    aoc_runner(project_path, 2025)
