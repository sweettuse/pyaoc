from __future__ import annotations
from collections import Counter, deque
from dataclasses import dataclass, field, replace
from itertools import chain, product
from math import prod
from typing import Callable, Iterable, NamedTuple
from pyaoc2019.utils import exhaust, identity, mapt, mapl, read_file
from rich import print


@dataclass
class Machine:
    workflows: dict[str, Workflow]
    parts: list[Part]
    accepted: list[Part] = field(default_factory=list)
    rejected: list[Part] = field(default_factory=list)

    @classmethod
    def from_str(cls, s: str) -> Machine:
        flows, parts = s.split("\n\n")
        return cls(
            {wf.name: wf for wf in map(Workflow.from_str, flows.splitlines())},
            mapl(Part.from_str, parts.splitlines()),
        )

    def process(self, part: Part):
        wf = self.workflows["in"]
        while (res := wf.process(part)) not in "AR":
            wf = self.workflows[res]

        (self.accepted if res == "A" else self.rejected).append(part)

    def run(self):
        exhaust(self.process, self.parts)
        return sum(p.value for p in self.accepted)


@dataclass
class Workflow:
    name: str
    rules: list[Rule]

    @classmethod
    def from_str(cls, s: str) -> Workflow:
        """example: px{a<2006:qkq,m>2090:A,rfg}"""
        name, rest = s[:-1].split("{")
        return cls(name, mapl(Rule.from_str, rest.split(",")))

    def process(self, part: Part) -> str:
        return next(filter(bool, (rule(part) for rule in self.rules)))  # type: ignore


@dataclass
class Rule:
    predicate: Callable[[Part], bool]
    output: str
    pred_str: str

    @classmethod
    def from_str(cls, s: str) -> Rule:
        """examples: s<537:gd | rfg"""
        if ":" not in s:
            return cls(identity, s, "identity")
        pred_str, output = s.split(":")
        var = pred_str[0]

        pred = pred_str.replace(var, f"lambda part: part.__dict__[{var!r}]", 1)
        return cls(eval(pred), output, pred_str)

    def __call__(self, part: Part) -> str | None:
        return self.output if self.predicate(part) else None


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def from_str(cls, s: str):
        return cls(**eval(s.replace("{", "dict(").replace("}", ")")))

    @property
    def value(self):
        return sum(self)

    def __iter__(self):
        for f in self.__dataclass_fields__:
            yield getattr(self, f)


# ==============================================================================
# PART 2
# ==============================================================================


@dataclass
class Machine2:
    workflows: dict[str, Workflow2]
    accepted: list[Part2] = field(default_factory=list)
    rejected: list[Part2] = field(default_factory=list)

    @classmethod
    def from_str(cls, s: str) -> Machine2:
        flows, _ = s.split("\n\n")
        return cls({wf.name: wf for wf in map(Workflow2.from_str, flows.splitlines())})

    def process(self, part: Part2):
        queue = deque([(part, "in")])
        while queue:
            p, name = queue.popleft()
            if name == "A":
                self.accepted.append(p)
                continue
            if name == "R":
                continue
            queue.extend(self.workflows[name].process(p))  # type: ignore


@dataclass
class Workflow2:
    name: str
    rules: list[Rule2]

    @classmethod
    def from_str(cls, s: str) -> Workflow2:
        """example: px{a<2006:qkq,m>2090:A,rfg}"""
        name, rest = s[:-1].split("{")
        return cls(name, mapl(Rule2.from_str, rest.split(",")))

    def process(self, part: Part2) -> Iterable[tuple[Part2, str | None]]:
        # print()
        # print(30 * "=")
        # print(f"workflow: {self.name}")
        to_process = [part]
        for rule in self.rules:
            if not to_process:
                break

            next_up = []
            for p in to_process:
                if not p.path or p.path[-1] != self.name:
                    p.path = p.path + [self.name]
                res = rule(p)
                # print(res)
                *_, matching, unmatched, next = res
                if matching:
                    yield matching, next
                next_up.extend(unmatched)
            to_process = next_up


class RuleRes(NamedTuple):
    debug: str
    input: Part2
    matching_part: Part2 | None
    unmatched_parts: tuple[Part2, ...]
    next_rule: str


@dataclass
class Rule2:
    predicate: Callable[[Part2], RuleRes]
    output: str
    pred_str: str
    category: str

    @classmethod
    def from_str(cls, s: str) -> Rule2:
        if ":" not in s:
            return cls(
                lambda part: RuleRes(f"all", part, part, (), s), s, "identity", "n/a"
            )

        pred_str, output = s.split(":")
        pred_range = Range.from_str(pred_str[1:])
        category = pred_str[0]

        def _pred(part: Part2) -> RuleRes:
            orig_range = part[category]
            debug = f"{pred_str}"
            if not (matching := orig_range & pred_range):
                return RuleRes(debug, part, None, (part,), output)

            matching_part = replace(part, **{category: matching})

            unmatched_category_values = (
                Range(orig_range.start, matching.start),
                Range(matching.end, orig_range.end),
            )
            new_unmatched_parts = tuple(
                replace(part, **{category: r}) for r in unmatched_category_values if r
            )

            return RuleRes(debug, part, matching_part, new_unmatched_parts, output)

        return cls(_pred, output, pred_str, category)

    def __call__(self, part: Part2) -> RuleRes:
        return self.predicate(part)


@dataclass
class Range:
    MIN = 1
    MAX = 4001
    start: int = MIN  # inclusive
    end: int = MAX  # exclusive

    @classmethod
    def from_str(cls, s: str) -> Range:
        op, num = s[0], int(s[1:])
        match op:
            case "<":
                return Range(cls.MIN, num)
            case ">":
                return Range(num + 1, cls.MAX)
            case _:
                raise ValueError(f"invalid operator {op!r}")

    def __and__(self, other: Range | str) -> Range:
        if isinstance(other, str):
            return self & Range.from_str(other)
        return Range(max(self.start, other.start), min(self.end, other.end))

    def __bool__(self):
        return self.end > self.start

    @property
    def value(self):
        return self.end - self.start


@dataclass
class Part2:
    x: Range = field(default_factory=Range)
    m: Range = field(default_factory=Range)
    a: Range = field(default_factory=Range)
    s: Range = field(default_factory=Range)
    path: list[str] = field(default_factory=list)

    def __bool__(self):
        return all(self)

    def __getitem__(self, key: str) -> Range:
        return getattr(self, key)

    def __setitem__(self, key: str, value: Range):
        setattr(self, key, value)

    def __iter__(self):
        for f in "xmas":
            yield self[f]

    @property
    def value(self):
        return prod(r.value for r in self)


def part1(fname: str):
    machine = Machine.from_str(read_file(fname, do_split=False))  # type:ignore
    return machine.run()


def part2(fname: str):
    machine = Machine2.from_str(read_file(fname, do_split=False))  # type:ignore
    machine.process(Part2())
    return sum(p.value for p in machine.accepted)


def main():
    print(part1("19.txt"))
    print(part2("19.txt"))


if __name__ == "__main__":
    main()
