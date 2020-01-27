from collections import ChainMap, defaultdict
from itertools import combinations, count
from typing import Dict, Tuple, NamedTuple, FrozenSet, _alias, KT, VT, List

import typing
from cytoolz import first, memoize, last

import pyaoc2019.utils as U
from string import ascii_lowercase, ascii_uppercase

__author__ = 'acushner'

from pyaoc2019.colors.tile_utils import RC, a_star

MyDict = _alias(dict, (KT, VT), inst=False)


class my_dict(dict):
    def __sub__(self, keys):
        return my_dict((k, self[k]) for k in self.keys() - keys)


class Maze(NamedTuple):
    key_pos: MyDict[str, RC]
    door_pos: MyDict[str, RC]
    walls: FrozenSet[RC]
    start: RC
    shape_lr: RC

    @classmethod
    def from_data(cls, data):
        keys = my_dict((v, rc) for rc, v in data.items() if v in ascii_lowercase)
        doors = my_dict((v, rc) for rc, v in data.items() if v in ascii_uppercase)
        walls = frozenset(rc for rc, v in data.items() if v == '#')
        start = first(rc for rc, v in data.items() if v == '@')
        return cls(keys, doors, walls, start, last(data.keys()))

    @classmethod
    def from_file(cls, filename):
        res = {RC(row, col): t
               for row, l in enumerate(U.read_file(filename))
               for col, t in enumerate(l)}
        return cls.from_data(res)


class PathCache:
    def __init__(self, maze: Maze):
        self._maze = maze
        self._cache = None
        self._cache_map: Dict[FrozenSet[str], typing.ChainMap] = defaultdict(ChainMap)

    def set_cache(self, found_keys: List[str]):
        all_keys = frozenset(found_keys)
        if not (res := self._cache_map.get(all_keys)):
            prev_keys = frozenset(found_keys[:-1])
            res = self._cache_map[all_keys] = self._cache_map[prev_keys].new_child()
        self._cache = res

    def __getitem__(self, rc_pair: Tuple[RC, RC]):
        return self._cache[rc_pair]

    def __setitem__(self, rc_pair: Tuple[RC, RC], distance):
        self._cache[rc_pair] = distance
        self._cache[tuple(reversed(rc_pair))] = distance

    def _cache_path(self, path: List[RC]):
        for (rc1, idx1), (rc2, idx2) in combinations(zip(path, count()), 2):
            self[rc1, rc2] = abs(idx2 - idx1)

    def get_path_lens(self, key_pos: MyDict[str, RC], cur_pos: RC) -> MyDict[str, int]:
        print(len(key_pos))
        impassable = self._maze.walls | {pos for k in key_pos if (pos := self._maze.door_pos.get(k.upper()))}
        res = my_dict()
        for key, rc in key_pos.items():
            try:
                dist = self[cur_pos, rc]
            except KeyError:
                dist = None
                path = a_star(self._maze.shape_lr, cur_pos, rc, impassable)
                if path:
                    self._cache_path(path)
                    dist = self[cur_pos, rc]

            if dist:
                res[key] = dist
        return res


def calc_steps2(maze: Maze):
    path_cache = PathCache(maze)

    @memoize
    def run(found_keys: Tuple[str] = None, cur_pos: RC = None):
        if not cur_pos:
            cur_pos = maze.start

        found_keys = found_keys or ()
        key_pos = maze.key_pos - frozenset(found_keys)
        path_cache.set_cache(found_keys)
        path_lens = path_cache.get_path_lens(key_pos, cur_pos)
        return min((pl + run(found_keys + (k,), key_pos[k]) for k, pl in path_lens.items()), default=0)

    return run()


def calc_steps(maze: Maze):
    @memoize
    def run(found_keys: FrozenSet[str] = frozenset(), cur_pos: RC = None):
        if not cur_pos:
            cur_pos = maze.start

        next_paths = get_paths(maze.key_pos - found_keys, cur_pos)
        return min((len(v) - 1 + run(found_keys | {k}, last(v)) for k, v in next_paths.items()), default=0)

    def get_paths(key_pos, cur_pos):
        print(len(key_pos))
        impassable = maze.walls | {pos for k in key_pos if (pos := maze.door_pos.get(k.upper()))}
        return {k: path
                for k, v in key_pos.items()
                if (path := a_star(maze.shape_lr, cur_pos, v, impassable))}

    return run()


def __main():
    with U.localtimer():
        # print(calc_steps2(Maze.from_file('18.test1')))
        # print(calc_steps2(Maze.from_file('18.test2')))
        print(calc_steps2(Maze.from_file('18.test2')))
        # print(calc_steps(Maze.from_file('18.test3')))
        # print(calc_steps(Maze.from_file('18')))


if __name__ == '__main__':
    __main()
########################
# f.D.E.e.C.b.A.@.a.B.c.#
######################.#
# d.....................#
########################
