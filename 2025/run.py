"""AoC 2025"""

import argparse
import contextlib
import logging
import pkgutil
import pathlib
import importlib
import typing
import types
import time

from aocd import get_data


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
        self._start = time.perf_counter_ns()
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
        stop = time.perf_counter_ns()
        self.duration_ns = stop - self._start
        self.duration_ms = self.duration_ns * 1e-6
        self.duration = self.duration_ns * 1e-9
        return False


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s: %(message)s",
        datefmt="%Y.%m.%d %H:%M:%S",
    )

    parser = argparse.ArgumentParser(prog="AoC 2024", description="AoC 2024")
    parser.add_argument("-d", "--day", type=int, required=False)

    args = parser.parse_args()
    specific_day = args.day

    tasks_path = pathlib.Path(__file__).parent.resolve() / "days"
    modules = [name for _, name, _ in pkgutil.iter_modules([str(tasks_path)])]
    logging.debug("Found the following modules: %s", modules)

    for day in modules:
        try:
            day_number = int(day.split("_")[1])
            if specific_day is not None and specific_day != day_number:
                continue

            data = get_data(day=day_number, year=2025)

            module = importlib.import_module(f"days.{day}")
            with ExecutionTimer() as timer:
                solution = module.solve(data)
            print(
                f"Day {day_number}, part 1: {solution[0]}, part 2: {solution[1]}, time: {timer.duration:.6}s"
            )
        except IndexError:
            continue
