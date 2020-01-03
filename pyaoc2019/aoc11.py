from enum import Enum
from typing import NamedTuple, Set

__author__ = 'acushner'

from pyaoc2019.interpreter import Instructions, parse_instruction, parse_file


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Coord(self.x + other[0], self.y + other[1])


class Direction(Enum):
    up = Coord(1, 0)
    right = Coord(0, 1)
    down = Coord(-1, 0)
    left = Coord(0, -1)

    def rotated(self, val):
        """
        0: rotate 90 deg counter-clockwise"
        1: rotate 90 deg clockwise"
        """
        dirs = list(Direction)
        val = 2 * val - 1
        new_idx = (dirs.index(self) + val) % len(dirs)
        return dirs[new_idx]


class HullRobot:
    def __init__(self, init_color=0):
        """colors are 0 (black) or 1 (white)"""
        self.whites: Set[Coord] = set()
        self._cur_pos = Coord(0, 0)
        if init_color:
            self.whites.add(self._cur_pos)
        self._cur_dir = Direction.up
        self._painted: Set[Coord] = set()

    def cur_color(self):
        while True:
            yield self._cur_pos in self.whites

    def _set_color(self, val):
        if val:
            self.whites.add(self._cur_pos)
        else:
            self.whites -= {self._cur_pos}

        self._painted.add(self._cur_pos)

    def _move(self, val):
        self._cur_dir = self._cur_dir.rotated(val)
        self._cur_pos += self._cur_dir.value

    def run(self, instructions: Instructions):
        proc = process(instructions)
        for out in proc:
            self._set_color(out)
            self._move(next(proc))
        return len(self._painted)

    def draw(self):
        min_x = min(c.x for c in self.whites)
        min_y = min(c.y for c in self.whites)

        offset = Coord(-min_x, -min_y)
        coords = {c + offset for c in self.whites}

        max_x = max(c.x for c in coords)
        max_y = max(c.y for c in coords)

        canvas = [[' '] * (max_y + 1) for _ in range(max_x + 1)]

        for c in coords:
            canvas[c.x][c.y] = 'X'

        for l in reversed(canvas):
            print(''.join(l))


def process(instructions: Instructions):
    while instructions.valid:
        inst = parse_instruction(instructions)
        inst.run()
        if inst.opcode.code == 4:
            yield instructions.output_register


def aoc11_a():
    robot = HullRobot()
    instructions = parse_file(11, robot.cur_color())
    return robot.run(instructions)


def aoc11_b():
    robot = HullRobot(1)
    instructions = parse_file(11, robot.cur_color())
    robot.run(instructions)
    robot.draw()


def __main():
    aoc11_b()


if __name__ == '__main__':
    __main()
