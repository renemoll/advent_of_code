"""Time related utilities."""

import contextlib
import typing
import types
import time
import argparse
import pkgutil
import logging
import importlib
import cProfile
import pathlib

import aocd


class ExecutionTimer(contextlib.AbstractContextManager):
    """High resolution timer to capture the execution time of a block.

    Attributes:
        duration (float): elapsed time in seconds.
        duration_ns (int): elapsed time in whole nanoseconds.
        duration_ms (float): elapsed time in milliseconds.
    """

    def __init__(self: "ExecutionTimer") -> None:
        """Initialize ExecutionTimer."""
        self._start = 0
        self.duration = 0.0
        self.duration_ms = 0.0
        self.duration_ns = 0

    def __enter__(self: "ExecutionTimer") -> "ExecutionTimer":
        """Start the timed context by recording the current time.

        Returns:
            The timed context.
        """
        self._start = time.thread_time_ns()
        return self

    def __exit__(
        self: "ExecutionTimer",
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_value: typing.Optional[BaseException],
        exc_traceback: typing.Optional[types.TracebackType],
    ) -> typing.Literal[False]:
        """Stop the timed context and calculate the elapsed time.

        Args:
            exc_type: optional exception type
            exc_value: optional exception value
            exc_traceback: optional exception traceback

        Returns:
            False, any captured exception will be propagated.
        """
        stop = time.thread_time_ns()
        self.duration_ns = stop - self._start
        self.duration_ms = self.duration_ns * 1e-6
        self.duration = self.duration_ns * 1e-9
        return False


def aoc_runner(project_path: pathlib.Path, year: int):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s: %(message)s",
        datefmt="%Y.%m.%d %H:%M:%S",
    )

    parser = argparse.ArgumentParser(prog="AoC runner", description="AoC runner")
    parser.add_argument("-d", "--day", type=int, required=False)
    parser.add_argument("--example", action="store_true", required=False, default=False)
    parser.add_argument(
        "--run_variants", action="store_true", required=False, default=False
    )
    parser.add_argument("--profile", action="store_true", required=False, default=False)

    args = parser.parse_args()
    specific_day = args.day
    use_example = args.example
    run_variants = args.run_variants

    modules = [name for _, name, _ in pkgutil.iter_modules([str(project_path)])]
    logging.debug("Found the following modules: %s", modules)

    for module in modules:
        try:
            if specific_day is not None:
                if not run_variants and module != f"day_{specific_day:02d}":
                    continue
                elif run_variants and not module.startswith(f"day_{specific_day:02d}"):
                    continue

            day_number = int(module.split("_")[1])
            module = importlib.import_module(f".{module}", f"aoc_{year}_py")

            if use_example:
                puzzle = aocd.models.Puzzle(year, day_number)
                example = puzzle.examples[0]

                if args.profile:
                    profiler = cProfile.Profile()
                    profiler.enable()
                    solution = module.solve(example.input_data)
                    profiler.disable()
                    profiler.print_stats(sort="time")
                else:
                    solution = module.solve(example.input_data)
                print(f"Part 1: {solution[0]}, expecting: {example.answer_a}")
                print(f"Part 2: {solution[1]}, expecting: {example.answer_b}")
            else:
                data = aocd.get_data(day=day_number, year=year)

                if args.profile:
                    profiler = cProfile.Profile()
                    profiler.enable()
                    solution = module.solve(data)
                    profiler.disable()
                    profiler.print_stats(sort="time")
                else:
                    with ExecutionTimer() as timer:
                        solution = module.solve(data)
                    print(
                        f"Day {day_number} (module: {module.__name__}), part 1: {solution[0]}, part 2: {solution[1]}, time: {timer.duration:.6}s"
                    )
        except IndexError:
            continue
