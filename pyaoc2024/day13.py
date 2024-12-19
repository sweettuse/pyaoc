from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Iterator, Literal, TypeVar
from rich import print as rprint

from pyaoc2019.utils import Coord, read_file

T = TypeVar("T")


@dataclass
class Machine:
    a: Coord
    b: Coord
    prize: Coord
    cost_a: int = 3
    cost_b: int = 1
    max_presses = 100

    @classmethod
    def from_str(cls, s: str) -> Machine:
        """sample input:
        Button A: X+94, Y+34
        Button B: X+22, Y+67
        Prize: X=8400, Y=5400
        """
        a, b, prize = s.split("\n")
        return cls(
            cls._parse_offset_str(a),
            cls._parse_offset_str(b),
            cls._parse_offset_str(prize, ignore_sign=True),
        )

    @classmethod
    def _parse_offset_str(cls, s: str, *, ignore_sign: bool = False) -> Coord:
        offset = 1 + int(ignore_sign)
        *_, x_str, y_str = s.split()
        return Coord(int(x_str[offset:-1]), int(y_str[offset:]))

    def calc_cost(self, num_a_presses: int) -> int | None:
        """old method that eschewed math"""
        cur = num_a_presses * self.a
        remaining = self.prize - cur
        num_b_x = remaining.x / self.b.x
        num_b_y = remaining.y / self.b.y
        if num_b_x != num_b_y or not num_b_x.is_integer():
            return None

        num_b_presses = int(num_b_x)

        if num_a_presses > self.max_presses or num_b_presses > self.max_presses:
            return None

        return self.cost_a * num_a_presses + self.cost_b * num_b_presses

    def calc_cost2(self) -> int:
        """use linear algebra"""
        det = self.a.x * self.b.y - self.b.x * self.a.y

        if det == 0:
            raise ValueError("The system of equations has no unique solution (determinant is zero).")

        num_a = (self.prize.x * self.b.y - self.prize.y * self.b.x) / det
        num_b = (self.a.x * self.prize.y - self.a.y * self.prize.x) / det
        if num_a.is_integer() and num_b.is_integer():
            return int(self.cost_a * num_a + self.cost_b * num_b)
        return 0

def _read_data(*, test: bool) -> list[Machine]:
    fname = "13.test.txt" if test else "13.txt"
    return [Machine.from_str(s) for s in read_file(fname, do_split=False).split("\n\n")]


def _filter_nones(it: Iterable[T | None]) -> Iterator[T]:
    for v in it:
        if v is not None:
            yield v


def _calc_cheapest_cost(m: Machine) -> int | None:
    res = _filter_nones(
        m.calc_cost(num_a_presses) for num_a_presses in range(m.max_presses + 1)
    )
    return min(res, default=None)
    ...


def part1(machines: list[Machine]) -> int:
    return sum(_filter_nones(map(_calc_cheapest_cost, machines)))

def part1_2(machines: list[Machine]) -> int:
    return sum(m.calc_cost2() for m in machines)


def part2(data): 
    # num_a * a + num_b * b = target
    # what about a binary search???
    ...


def _main():
    data = _read_data(test=False)

    print(part1_2(data))

    for m in data:
        m.prize += Coord(10000000000000, 10000000000000)
    print(part1_2(data))


if __name__ == "__main__":
    _main()
