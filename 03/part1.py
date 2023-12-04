from dataclasses import dataclass
import re


def has_gear_number(
    start: int, end: int, current_line: str, above_line: str, below_line: str
) -> bool:
    if start - 1 < 0:
        start = 0
    else:
        start = start - 1

    if end + 1 > len(current_line) + 1:
        end = len(current_line) + 1
    else:
        end = end + 1

    for line in [current_line, above_line, below_line]:
        for item in line[start:end]:
            if item not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
                return True

    return False


def get_part_numbers(current_line: str, above_line: str, below_line: str) -> list[int]:
    retval = []
    matches = re.finditer(r"\d+", current_line)
    for match in matches:
        start = match.start()
        end = match.end()
        value = int(match.group(0))
        if has_gear_number(start, end, current_line, above_line, below_line):
            retval.append(value)
    return retval


def main():
    above = ""
    current = ""
    below = None

    total = 0
    with open("03/part1.txt") as f:
        data = f.read()

    lines = data.splitlines()

    while True:
        if below is None:
            current = lines.pop(0)

        if len(lines) > 0:
            below = lines.pop(0)

        if current == "":
            break

        part_numbers = get_part_numbers(current, above, below)
        print(part_numbers)
        for part in part_numbers:
            total += part

        above = current
        current = below

        if len(lines) == 0:
            below = ""

    print(f"Total: {total}")


if __name__ == "__main__":
    main()