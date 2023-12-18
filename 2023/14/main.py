"""Day 14: Parabolic Reflector Dish"""

from __future__ import annotations
from argparse import ArgumentParser
from collections import OrderedDict
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum


class Item(Enum):
    """Defines the possible items"""

    ROUNDED_ROCK = "O"
    CUBE_ROCK = "#"
    EMPTY_SPACE = "."


class Direction(Enum):
    """Defines the possible direction"""

    # The values are the required transpose operations needed to orient properly
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)


@dataclass
class Platform:
    """Defines the Platform"""

    positions: list[list[Item]]
    round_rocks: list[tuple[int, int]]

    def __hash__(self) -> list[str]:
        """Makes the platform hashable."""
        retval = []
        for row in self.positions:
            for val in row:
                retval.append(val.value)
        return hash("".join(retval))

    def cycle(self) -> None:
        """Performs a cycle operation on the platform."""
        self.slide(direction=Direction.NORTH)
        self.slide(direction=Direction.WEST)
        self.slide(direction=Direction.SOUTH)
        self.slide(direction=Direction.EAST)

    def slide(self, direction: Direction = Direction.NORTH) -> None:
        """Slides the platform in a specified direction"""

        # We'll keep performing one-row up changes until we have a pass through
        # where nothing changes.
        while True:
            complete = True
            new_rocks = []
            for rock in self.round_rocks:
                x = rock[0]
                y = rock[1]

                next_x = x + direction.value[0]
                next_y = y + direction.value[1]
                # If the round rock is on an edge, don't bother
                if next_x < 0 or next_x >= len(self.positions[0]) or next_y < 0 or next_y >= len(self.positions):
                    new_rocks.append((x, y))
                # Otherwise, find the
                elif self.positions[next_y][next_x] == Item.EMPTY_SPACE:
                    self.positions[next_y][next_x] = Item.ROUNDED_ROCK
                    self.positions[y][x] = Item.EMPTY_SPACE
                    new_rocks.append((next_x, next_y))
                    complete = False
                else:
                    new_rocks.append((x, y))
            self.round_rocks = new_rocks
            if complete:
                break

    def total_load(self) -> int:
        """Returns the load on the platform given the current state"""
        retval = 0

        # Start from the bottom, count the number of round rocks and
        # increment the retval by i*N
        for i, row in enumerate(reversed(self.positions), 1):
            for entry in row:
                row_count = 0
                if entry == Item.ROUNDED_ROCK:
                    row_count += 1
                retval += i * row_count

        return retval


def read_file(path: str) -> Platform:
    """Returns a platform given the file provided."""
    with open(path, encoding="utf-8") as f:
        data = f.read()

    lines = data.splitlines()
    platform = []
    round_rocks = []
    for y, line in enumerate(lines):
        row = []
        for x, pos in enumerate(line):
            item = Item(pos)
            row.append(item)
            if item == Item.ROUNDED_ROCK:
                round_rocks.append((x, y))
        platform.append(row)

    return Platform(positions=platform, round_rocks=round_rocks)


def part1(platform: Platform) -> int:
    """Returns the part 1 answer"""
    platform.slide()
    return platform.total_load()


def part2(platform: Platform) -> int:
    """Returns the part 2 answer"""
    # Use an ordered dict so we can do faster cycle checks.
    cycle_list = OrderedDict({platform: True})
    cycle_count = 1000000000
    counter = 0
    current_platform = platform
    while True:
        if counter > cycle_count:
            break
        current_platform = deepcopy(current_platform)
        current_platform.cycle()
        if current_platform in cycle_list:
            cycle_list_by_key = list(cycle_list.keys())
            index = cycle_list_by_key.index(current_platform)
            loop_length = counter + 1 - index
            final_instance_index = (cycle_count - index) % loop_length + index
            return cycle_list_by_key[final_instance_index].total_load()

        cycle_list.update({current_platform: True})
        counter += 1
        if counter % 100 == 0:
            print(f"Counter: {counter}")
    return current_platform.total_load()


def main():
    """Main entrypoint."""
    parser = ArgumentParser(prog="day14")
    parser.add_argument("-f", "--filename", required=True)
    args = parser.parse_args()
    platform = read_file(args.filename)
    p1 = part1(platform)
    print(f"Part1: {p1}")

    platform = read_file(args.filename)
    p2 = part2(platform)
    print(f"Part2: {p2}")


if __name__ == "__main__":
    main()
