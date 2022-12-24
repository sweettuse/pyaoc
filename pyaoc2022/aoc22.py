from __future__ import annotations
from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
from itertools import repeat
import re
from typing import Generator, Literal, NamedTuple, Optional, TypeAlias

from pyaoc2019.utils import RC, get_all_ints, read_file
from rich import print

class MinMax(NamedTuple):
    min: int
    max: int

MinMaxDict: TypeAlias = dict[int, MinMax]


@dataclass
class Map:
    coords: dict[RC, str]
    min_max_row: MinMaxDict
    min_max_col: MinMaxDict
    init_pos: RC

    @classmethod
    def from_str(cls, s) -> Map:
        res = {}
        init_pos = None
        for r, row in enumerate(s.splitlines()):
            for c, val in enumerate(row):
                if val == ' ':
                    continue
                if init_pos is None and val == '.':
                    init_pos = RC(r, c)
                res[RC(r, c)] = val
        min_max_row = cls._calc_min_max_dict(res, 0)
        min_max_col = cls._calc_min_max_dict(res, 1)
        return cls(res, min_max_row, min_max_col, init_pos)

    @classmethod
    def _calc_min_max_dict(cls, coords: dict[RC, str], by: int) -> MinMaxDict:
        other = abs(by - 1)
        res = defaultdict(list)
        for c in coords:
            res[c[by]].append(c[other])
        return {k: MinMax(min(v), max(v)) for k, v in res.items()}

    def move(self, cur_pos: RC, cur_dir: Dir) -> Optional[tuple[RC, Dir]]:
        next_pos = cur_pos + cur_dir.value

        if not (val := self.coords.get(next_pos)):
            next_pos, cur_dir = self._wrap(cur_pos, cur_dir)
            val = self.coords[next_pos]
        if val == '.':
            return next_pos, cur_dir
        # can't move
        return None

    def _wrap(self, cur_pos: RC, cur_dir: Dir) -> tuple[RC, Dir]:
        if cur_dir is Dir.up:
            res = RC(self.min_max_col[cur_pos.c].max, cur_pos.c)
        elif cur_dir is Dir.down:
            res = RC(self.min_max_col[cur_pos.c].min, cur_pos.c)

        elif cur_dir is Dir.left:
            res = RC(cur_pos.r, self.min_max_row[cur_pos.r].max)
        elif cur_dir is Dir.right:
            res = RC(cur_pos.r, self.min_max_row[cur_pos.r].min)
        
        return res, cur_dir
    


@dataclass
class Inst:
    rotation: Literal['r', 'l']
    num: int

    @property
    def dirs(self) -> Generator[Literal['l', 'r', 'f'], None, None]:
        if not self.num:
            return
        yield self.rotation
        yield from repeat('f', self.num)  # type: ignore


class Dir(Enum):
    up = RC(-1, 0)
    right = RC(0, 1)
    down = RC(1, 0)
    left = RC(0, -1)

    def rotate(self, d: Literal['l', 'r', 'f']):
        if d == 'f':
            return self

        v = _rot_left if d == 'l' else _rot_right
        return v[self]


_tmp_dirs = deque(Dir)
_tmp_dirs.rotate(1)
_rot_left = dict(zip(Dir, _tmp_dirs))
_tmp_dirs.rotate(-2)
_rot_right = dict(zip(Dir, _tmp_dirs))
_dir_val_map = dict(zip(Dir, (3, 0, 1, 2)))


def parse_instructions(s):
    ints = list(get_all_ints(s))
    dirs = list(filter(bool, re.split('[-]?\d+', s)))
    dirs.insert(0, 'R')
    return [Inst(d.lower(), i) for d, i in zip(dirs, ints)]


@dataclass
class Tracker:
    jungle: Map
    insts: list[Inst]
    cur_pos: RC
    cur_dir: Dir = Dir.up


    def move(self):
        for inst in self.insts:
            for d in inst.dirs:
                if not self._move_one(d):
                    break
    @property
    def score(self):
        return 1000 * (self.cur_pos.r + 1) + 4 * (self.cur_pos.c + 1) + _dir_val_map[self.cur_dir]

    def _move_one(self, d: Literal['l', 'r', 'f']):
        if d in set('lr'):
            self.cur_dir = self.cur_dir.rotate(d)
            return True

        if not (new_pos_dir := self.jungle.move(self.cur_pos, self.cur_dir)):
            return False
        self.cur_pos, self.cur_dir = new_pos_dir
        return True

class Map2(Map):
    def _wrap(self, cur_pos: RC, cur_dir: Dir) -> tuple[RC, dir]:
        """todo: transform the input into a cube
        
        map open edges to each other both row/col and direction
        """
        return super()._wrap(cur_pos, cur_dir)

def parse_data(name, map_type=Map):
    data = read_file(name, do_split=False)
    jungle, insts = data.split('\n\n')
    jungle = map_type.from_str(jungle)
    return Tracker(jungle, parse_instructions(insts), jungle.init_pos)


def parts1and2(name, map_type=Map):
    tracker = parse_data(name, map_type)
    tracker.move()
    return tracker.score

print(parts1and2(22))
print(parts1and2(22, Map2))
