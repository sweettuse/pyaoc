from collections import defaultdict
import asyncio
from itertools import count
from operator import itemgetter

import uvloop

import pyaoc2019.utils as U

uvloop.install()

__author__ = 'acushner'


def parse_file(name):
    res_pc, res_cp = defaultdict(set), {}
    for l in U.read_file(name):
        parent, child = l.split(')')
        res_pc[parent].add(child)
        res_cp[child] = parent
    return res_pc, res_cp


async def calc_orbits(orbital_map, n_parents=0, current_body='COM'):
    tasks = (asyncio.create_task(calc_orbits(orbital_map, n_parents + 1, p)) for p in orbital_map[current_body])
    return n_parents + sum(await asyncio.gather(*tasks))


def _get_parents(orbital_map, name):
    res, c = {}, count()
    while name := orbital_map.get(name):
        res[name] = next(c)
    return res


def calc_num_transfers(orbital_map):
    santa_fam, my_fam = _get_parents(orbital_map, 'SAN'), _get_parents(orbital_map, 'YOU')
    shared_ancestors = set(santa_fam) & my_fam.keys()
    closest_parent, s_dist = min(((k, santa_fam[k]) for k in shared_ancestors), key=itemgetter(1))
    return s_dist + my_fam[closest_parent]


def __main():
    with U.localtimer():
        parent_child_map, child_parent_map = parse_file('06')
        print(asyncio.run(calc_orbits(parent_child_map)))
        print(calc_num_transfers(child_parent_map))


if __name__ == '__main__':
    __main()
