from collections import defaultdict, Counter
from itertools import chain
from typing import NamedTuple, Optional, List, Tuple, Dict
import arrow

from pyaoc2019.utils import read_file

__author__ = 'acushner'


class LogEntry(NamedTuple):
    dt: arrow.Arrow
    text: str

    @classmethod
    def from_str(cls, s):
        dt, text = s.split('] ')
        return cls(arrow.get(dt[1:]), text)

    @property
    def guard_id(self) -> Optional[int]:
        if 'begins' in self.text:
            return int(self.text.split()[1][1:])

    @property
    def asleep(self):
        return 'falls' in self.text


class StartEnd(NamedTuple):
    start: arrow.Arrow
    end: arrow.Arrow

    @property
    def time(self):
        return int((self.end - self.start).total_seconds() // 60)

    @property
    def minutes(self):
        return [dt.minute for dt in arrow.Arrow.range('minute', self.start, self.end)][:-1]


def _get_sleep_habits(data) -> Dict[int, List[StartEnd]]:
    guard_id = None
    res = defaultdict(list)
    for le in map(LogEntry.from_str, data):
        if gid := le.guard_id:
            guard_id = gid
        elif le.asleep:
            start = le.dt
        else:
            res[guard_id].append(StartEnd(start, le.dt))
    return res


def part1(sleep_times):
    gid = max((sum(se.time for se in v), k) for k, v in sleep_times.items())[1]
    pop_min = Counter(m for se in sleep_times[gid] for m in se.minutes).most_common(1)[0][0]
    print(gid, pop_min)
    return gid * pop_min


def part2(sleep_times):
    res = {gid: Counter(m for se in starts_ends for m in se.minutes) for gid, starts_ends in sleep_times.items()}
    gid = max((max(minutes.values()), gid) for gid, minutes in res.items())[1]

    return gid * res[gid].most_common(1)[0][0]


def __main():
    data = sorted(read_file(4, 2018))
    sleep_times = _get_sleep_habits(data)
    print(part1(sleep_times))
    print(part2(sleep_times))


if __name__ == '__main__':
    __main()
