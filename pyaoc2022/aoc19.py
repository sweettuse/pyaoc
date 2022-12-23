from __future__ import annotations
from dataclasses import dataclass, field
from typing import Generator, Literal, TypeAlias
from rich import print

from pyaoc2019.utils import chunks, get_all_ints, read_file, mapt

Mineral: TypeAlias = str


@dataclass
class RobotSpec:
    mineral: Mineral
    costs: dict[Mineral, int]

    @classmethod
    def from_str(cls, s) -> RobotSpec:
        print(repr(s))
        mineral_str, cost_str = s.split(' costs ')
        mineral = mineral_str.split()[1]

        cost_str = cost_str.replace('and ', '')
        costs = {m: int(n) for n, m in chunks(cost_str.split(), 2)}
        return cls(mineral, costs)

    def can_build(self, stock) -> bool:
        """with this stock, can we build this spec"""
        return all(cost < stock.get(mineral, 0) for mineral, cost in self.costs.items())


@dataclass
class Blueprint:
    num: int
    robot_specs: tuple[RobotSpec, ...]

    @classmethod
    def from_str(cls, s) -> Blueprint:
        num_str, rem = s.split(':')
        num = next(get_all_ints(num_str))

        robot_specs = tuple(
            RobotSpec.from_str(stripped) for s in rem.split('.') if (stripped := s.strip())
        )
        return cls(num, robot_specs)

    def can_build(self, stock: dict[Mineral, int]) -> Generator[RobotSpec, None, None]:
        """yield each robot that could be built from this stock"""
        for spec in self.robot_specs:
            if spec.can_build(stock):
                yield spec


initial_stock = dict.fromkeys(('ore', 'clay', 'obsidian', 'geode'), 0)


@dataclass
class Executor:
    blueprint: Blueprint
    robots: dict[Mineral, int] = field(default_factory=lambda: dict(ore=1))
    stock: dict[Mineral, int] = field(default_factory=lambda: initial_stock.copy())
    time: int = 0

    def run(self, end_time=24):
        for _ in range(end_time):
            self._run_one()

    def _run_one(self):
        for spec in self.blueprint.can_build(self.stock):
            pass

    def copy(self):
        return Executor(self.blueprint, self.robots.copy(), self.stock.copy(), self.time)


def parse_data(name) -> list[Blueprint]:
    return list(map(Blueprint.from_str, read_file(name)))


print(parse_data(19))
