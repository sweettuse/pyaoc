from collections import defaultdict
from asyncio import create_task, gather
import asyncio
from itertools import count
from operator import itemgetter
from typing import Set, Dict, Tuple

import uvloop

import pyaoc2019.utils as U

uvloop.install()

__author__ = 'acushner'

ParentChildrenMap = Dict[str, Set[str]]
ChildParentMap = Dict[str, str]


def parse_file(name) -> Tuple[ParentChildrenMap, ChildParentMap]:
    """return {parent: {children}} map and {child: parent} map"""
    res_pc, res_cp = defaultdict(set), {}
    for l in U.read_file(name):
        parent, child = l.split(')')
        res_pc[parent].add(child)
        res_cp[child] = parent
    return res_pc, res_cp


async def calc_orbits(orbital_map: ParentChildrenMap, n_parents=0, current_body='COM') -> int:
    """
    each body directly orbits around one body and indirectly around all that body's parents

    starting from the center of the universe, sum up all of these in a recursive fashion
    """
    orbits = (calc_orbits(orbital_map, n_parents + 1, p) for p in orbital_map[current_body])
    return n_parents + sum(await gather(*map(create_task, orbits)))


def _get_parents(orbital_map: ChildParentMap, name) -> Dict[str, int]:
    """
    for a given orbital body, calc all of its parents/ancestors and its distance to each

    return {parent_name: distance}
    """
    res, c = {}, count()
    while name := orbital_map.get(name):
        res[name] = next(c)
    return res


def calc_num_transfers(orbital_map):
    """
    find all parents, find the closest shared parent based on distance,
    and then calculate the total to travel between them
    """
    santa_fam, my_fam = _get_parents(orbital_map, 'SAN'), _get_parents(orbital_map, 'YOU')
    shared_ancestors = set(santa_fam) & my_fam.keys()
    closest_parent, santa_dist = min(((k, santa_fam[k]) for k in shared_ancestors), key=itemgetter(1))
    return santa_dist + my_fam[closest_parent]


def __main():
    parent_child_map, child_parent_map = parse_file('06')
    print(asyncio.run(calc_orbits(parent_child_map)))
    print(calc_num_transfers(child_parent_map))


if __name__ == '__main__':
    __main()
