from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable
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
        flows, parts = s.split('\n\n')
        wfs = {wf.name: wf for wf in map(Workflow.from_str, flows.splitlines())}
        parts = mapl(Part.from_str, parts.splitlines())
        return cls(wfs, parts)

    def process(self, part: Part):
        wf = self.workflows['in']
        while (res := wf.process(part)) not in 'AR':
            wf = self.workflows[res]
        
        (self.accepted if res == 'A' else self.rejected).append(part)
    
    def run(self):
        exhaust(self.process, self.parts)
        return sum(p.value for p in self.accepted)



@dataclass
class Workflow:
    name: str
    rules: list[Rule]

    @classmethod
    def from_str(cls, s: str) -> Workflow:
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



def part1(fname: str):
    machine =Machine.from_str(read_file(fname, do_split=False))  # type:ignore
    return machine.run()


def part2(fname: str):
    ...


if __name__ == "__main__":
    print(part1("19.txt"))
    print(part2("19.txt.test"))
