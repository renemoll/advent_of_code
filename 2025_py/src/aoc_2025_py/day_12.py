"""Day 12: Christmas Tree Farm

Part 1:
    We are given several layouts and need to determine how to fit several of these layers into a given area.

    Lets first see if everything can fit into the area without overlapping any of the layouts...
"""


def _parse(input_data: str) -> tuple[dict[str, list[str]], list[dict[str, object]]]:
    sections = input_data.split("\n\n")
    section_presents = sections[0:-1]
    section_regions = sections[-1]

    presents = {
        int(line.split(":")[0]): {
            "area": line.split(":")[1].strip().splitlines(),
            "units": line.split(":")[1].count("#"),
        }
        for line in section_presents
    }
    regions = [
        {
            "width": int(line.split(":")[0].split("x")[0].strip()),
            "height": int(line.split(":")[0].split("x")[1].strip()),
            "presents": list(map(int, line.split(":")[1].strip().split())),
        }
        for line in section_regions.splitlines()
    ]

    return presents, regions


def _part1(parsed_input) -> int:
    presents, regions = parsed_input

    result = 0
    for region in regions:
        area_available = region["width"] * region["height"]
        area_required = 0
        for i, amount in enumerate(region["presents"]):
            area_required += amount * presents[i]["units"]
        result += 1 if area_required <= area_available else 0

    return result


def _part2(parsed_input) -> int:
    return 0


def solve(input_data: str) -> tuple[int, int]:
    parsed_input = _parse(input_data)
    return (_part1(parsed_input), _part2(parsed_input))
