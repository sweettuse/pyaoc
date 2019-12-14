from collections import defaultdict
import asyncio
from itertools import count
from operator import itemgetter

import uvloop

import utils as U

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
    tasks = [asyncio.create_task(calc_orbits(orbital_map, n_parents + 1, p)) for p in orbital_map[current_body]]
    return n_parents + sum(await asyncio.gather(*tasks))


def _get_parents(orbital_map, name):
    res = {}
    c = count()
    while True:
        name = orbital_map.get(name)
        if not name:
            break
        res[name] = next(c)
    return res


def calc_num_transfers(orbital_map):
    sp, mp = _get_parents(orbital_map, 'SAN'), _get_parents(orbital_map, 'YOU')
    shared_ancestors = set(sp) & mp.keys()
    closest_parent, s_dist = min(((k, sp[k]) for k in shared_ancestors), key=itemgetter(1))
    return s_dist + mp[closest_parent]


def __main():
    print(parse_file('06.test'))
    with U.localtimer():
        print(asyncio.run(calc_orbits(parse_file('06')[0])))
        print(calc_num_transfers(parse_file('06')[1]))


if __name__ == '__main__':
    __main()
