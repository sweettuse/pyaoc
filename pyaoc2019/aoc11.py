from typing import NamedTuple, Set

__author__ = 'acushner'

from pyaoc2019.interpreter import Program, parse_file, process
from pyaoc2019.utils import Coord, Direction


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

    def run(self, program: Program):
        proc = process(program)
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


def aoc11_a():
    robot = HullRobot()
    program = parse_file(11, robot.cur_color())
    return robot.run(program)


def aoc11_b():
    robot = HullRobot(1)
    program = parse_file(11, robot.cur_color())
    robot.run(program)
    robot.draw()


def __main():
    print(aoc11_a())
    # aoc11_b()


if __name__ == '__main__':
    __main()
