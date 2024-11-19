import logging
import pkgutil
import pathlib
import importlib

from aocd import get_data


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s: %(message)s",
        datefmt="%Y.%m.%d %H:%M:%S",
    )

    tasks_path = pathlib.Path(__file__).parent.resolve() / "days"
    modules = [name for _, name, _ in pkgutil.iter_modules([str(tasks_path)])]
    logging.debug("Found the following modules: %s", modules)

    for day in modules:
        day_number = int(day.split("_")[1])
        data = get_data(day=day_number, year=2023).splitlines()

        module = importlib.import_module(f"days.{day}")
        solution = module.solve(data)
        print(f"Day {day_number}, part 1: {solution[0]}, part 2: {solution[1]}")


if __name__ == "__main__":
    main()
