from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, NamedTuple, cast
from rich import print

from pyaoc2019.utils import read_file, timer


@dataclass(frozen=True)
class Range:
    start: int
    end: int  # exclusive

    @property
    def spread(self):
        return self.end - self.start

    def __and__(self, other: Range) -> Range:
        """intersect of ranges"""
        return Range(max(self.start, other.start), min(self.end, other.end))

    def __bool__(self):
        return self.spread > 0

    def __lt__(self, other: Range) -> bool:
        return (
            self.start < other.start
            or self.start == other.start
            and self.end < other.end
        )

    def __eq__(self, other: Range) -> bool:
        return self.start == other.start and self.end == other.end

    @classmethod
    def combine(cls, *ranges: Range) -> Iterable[Range]:
        """merge multiple ranges together"""
        rs = iter(sorted(filter(bool, ranges)))

        try:
            cur = next(rs)
        except StopIteration:
            return

        for other in rs:
            if ellided := cur.ellide(other):
                cur = ellided
                continue
            yield cur
            cur = other
        yield cur

    def ellide(self, other: Range) -> Range | None:
        """return the range of self and other combined if they either
        overlap or abut each other
        """
        if (self & other).spread >= 0:
            return Range(min(self.start, other.start), max(self.end, other.end))
        return None


class TransformRes(NamedTuple):
    converted: Range
    unmatched: tuple[Range, ...]


@dataclass
class Transformer:
    from_: Range
    offset: int

    @classmethod
    def from_data(cls, dest: int, source: int, length: int):
        return cls(Range(source, source + length), dest - source)

    def transform(self, input: Range) -> TransformRes:
        if not (matched := input & self.from_):
            return TransformRes(converted=matched, unmatched=(input,))

        return TransformRes(
            converted=Range(matched.start + self.offset, matched.end + self.offset),
            unmatched=(
                Range(input.start, matched.start),
                Range(matched.end, input.end),
            ),
        )


@dataclass
class ResourceConverter:
    from_resource: str
    to_resource: str
    transformers: tuple[Transformer, ...]

    @classmethod
    def from_group(cls, group: str) -> ResourceConverter:
        lines = iter(group.splitlines())
        s, _ = next(lines).split()
        from_resource, _, to_resource = s.split("-")
        return cls(from_resource, to_resource, tuple(map(cls._parse_line, lines)))

    @classmethod
    def _parse_line(cls, line: str) -> Transformer:
        return Transformer.from_data(*map(int, line.split()))

    def convert(self, input: Range) -> list[Range]:
        matched_res = []
        cur_round = [input]
        next_round = []
        for t in self.transformers:
            next_round = []
            for rng in Range.combine(*cur_round):
                matched, unmatched = t.transform(rng)
                if matched:
                    matched_res.append(matched)
                next_round.extend(unmatched)
            cur_round = next_round

        return list(Range.combine(*matched_res, *next_round))


@dataclass
class Almanac:
    seeds: list[int]
    converters: dict[tuple[str, str], ResourceConverter]
    graph: dict[str, str]

    @classmethod
    def from_fname(cls: type[Almanac], fname: str) -> Almanac:
        s = cast(str, read_file(fname, do_split=False))
        groups = iter(s.split("\n\n"))
        _, *seed_strs = next(groups).split()
        seeds = list(map(int, seed_strs))
        converters = {
            (rc.from_resource, rc.to_resource): rc
            for rc in map(ResourceConverter.from_group, groups)
        }
        graph = {rc.from_resource: rc.to_resource for rc in converters.values()}
        return cls(seeds, converters, graph)

    def convert(self, from_: str, to: str, r: Range) -> list[Range]:
        current = [r]
        for pair in self.get_path(from_, to):
            next_ = []
            rc = self.converters[pair]
            for r in current:
                next_.extend(rc.convert(r))
            current = list(Range.combine(*next_))
        return current

    def get_path(self, from_: str, to: str) -> list[tuple[str, str]]:
        res = []
        cur = from_
        while cur != to:
            next_ = self.graph[cur]
            res.append((cur, next_))
            cur = next_
        return res


def part1():
    a = Almanac.from_fname("05.txt")
    seed_ranges = [Range(s, s + 1) for s in a.seeds]
    return _calc(a, seed_ranges)


def part2():
    a = Almanac.from_fname("05.txt")
    chunked = list(zip(a.seeds[::2], a.seeds[1::2]))
    seed_ranges = [Range(a, a + b) for a, b in chunked]
    return _calc(a, seed_ranges)


def _calc(a: Almanac, seed_ranges: list[Range]) -> int:
    converted = list(a.convert("seed", "location", sr) for sr in seed_ranges)
    return min(r.start for l in converted for r in l)


@timer
def main():
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()