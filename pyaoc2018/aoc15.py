import heapq
from collections import defaultdict
from itertools import count
from queue import Queue

from more_itertools import last, first

from pyaoc2019.colors.tile_utils import RC as OrigRC
from pyaoc2019.utils import read_file, localtimer

__author__ = 'acushner'


class RC(OrigRC):
    def __lt__(self, other):
        return tuple.__lt__(self, other)

    @property
    def manhattan(self):
        return abs(self.r) + abs(self.c)


dirs = dict(
    up=RC(-1, 0),
    left=RC(0, -1),
    right=RC(0, 1),
    down=RC(1, 0),
)

extra_h = dict(
    up=-2,
    left=-1,
    right=1,
    down=2,
)


# extra_h = defaultdict(int)


class Combatant(str):
    def __init__(self, name, attack_power=3, hp=200):
        self.name = name
        self.attack_power = attack_power
        self.hp = hp

    @property
    def is_alive(self):
        return self.hp > 0

    def __str__(self):
        return self.name

    __repr__ = __str__


class PriorityQueue(list):
    def put(self, item, priority):
        heapq.heappush(self, (priority, item))

    def get(self):
        return heapq.heappop(self)[1]


class Map:
    def __init__(self, fname=15, elf_attack_power=3):
        fname = fname or 15
        self._shape, self._maze_coords = self._init_maze_coords(fname, elf_attack_power)
        self._predecessors = {}

    @staticmethod
    def _init_maze_coords(fname, elf_attack_power):
        groups = {}
        for r_num, row in enumerate(read_file(fname, 2018)):
            for c_num, v in enumerate(row):
                if v in set('EG'):
                    v = Combatant(v)
                if v == 'E':
                    v.attack_power = elf_attack_power
                groups[RC(r_num, c_num)] = v
        return RC(r_num + 1, c_num + 1), groups

    @property
    def _maze(self):
        res = [[None] * self._shape.c for _ in range(self._shape.r)]
        for (r, c), terrain in self._maze_coords.items():
            res[r][c] = terrain

        return res

    def _calc_a_star(self, start, goal):
        g_scores = {start: 0}
        pq = PriorityQueue()
        pq.put(start, 0)
        predecessors = {start: None}

        while pq:
            cur = pq.get()
            new_g = g_scores[cur] + 1
            for dir_name, offset in dirs.items():
                if (neighbor := cur + offset) == goal:
                    return self._get_path(predecessors, start, cur)

                if self._is_valid_pos(neighbor) and neighbor not in g_scores:
                    g_scores[neighbor] = new_g
                    pq.put(neighbor, new_g + (goal - neighbor).manhattan + extra_h[dir_name])
                    predecessors[neighbor] = cur

    def _calc_bfs(self, start, goal):
        q = Queue()
        q.put(start)
        predecessors = {start: None}

        while not q.empty():
            cur = q.get()

            for offset in dirs.values():
                if (neighbor := cur + offset) == goal:
                    return self._get_path(predecessors, start, cur)

                if self._is_valid_pos(neighbor) and neighbor not in predecessors:
                    predecessors[neighbor] = cur
                    q.put(neighbor)

    @staticmethod
    def _get_path(predecessors, start, goal):
        n = goal
        res = []

        while n != start:
            res.append(n)
            n = predecessors[n]
        res.append(start)

        return list(reversed(res))

    def _move(self, rc, cmb, combatants_copy, cnt):
        cur_paths = []
        for other_rc, other_cmb in combatants_copy.items():
            if cmb.name != other_cmb.name:
                # TODO: actually try to use goal squares of near targets, not the targets themselves
                path = self._calc_a_star(rc, other_rc)
                # path = self._calc_bfs(rc, other_rc)
                if not path:
                    continue
                cur_paths.append((len(path), next(cnt), path))

        if cur_paths:
            _, _, path = min(cur_paths)
            if len(path) > 1:
                self._maze_coords[rc] = '.'
                self._maze_coords[path[1]] = cmb
                combatants_copy.pop(rc)
                combatants_copy[path[1]] = cmb
                rc = path[1]
        return rc

    def _attack(self, rc, cmb, combatants_copy):
        enemies = []
        for offset in dirs.values():
            if (isinstance(other_cmb := self._maze_coords[(other_pos := rc + offset)], Combatant)
                    and other_cmb.name != cmb.name):
                enemies.append((other_cmb.hp, other_pos, other_cmb))

        if enemies:
            _, enemy_pos, enemy_cmb = min(enemies)
            enemy_cmb.hp -= cmb.attack_power
            if not enemy_cmb.is_alive:
                self._maze_coords[enemy_pos] = '.'
                combatants_copy.pop(enemy_pos)

    def tick(self):
        elves = [cmb for cmb in self._maze_coords.values() if cmb == 'E']
        for rnd in count():
            combatants = sorted((rc, cmb) for rc, cmb in self._maze_coords.items() if isinstance(cmb, Combatant))
            combatants = dict(combatants)

            combatants_copy = combatants.copy()
            cnt = count()
            # print(rnd, [(cmb.name, cmb.hp) for cmb in combatants_copy.values()])

            if not all(cmb.is_alive for cmb in elves):
                raise Exception(rnd)

            for rc, cmb in combatants.items():
                if cmb.is_alive:
                    new_rc = self._move(rc, cmb, combatants_copy, cnt)
                    self._attack(new_rc, cmb, combatants_copy)

            if len({cmb.name for cmb in combatants_copy.values()}) == 1:
                # print(rnd, [(cmb.name, cmb.hp) for cmb in combatants_copy.values()])
                break

            yield

        remaining_hp = sum(cmb.hp for cmb in combatants_copy.values())
        yield rnd, remaining_hp

    def _is_valid_pos(self, rc):
        return self._maze_coords[rc] == '.'

    def display(self):
        for r in self._maze:
            cur = []
            cmbs = []
            for tile in r:
                if isinstance(tile, Combatant):
                    cmbs.append(tile)
                cur.append(tile)
            cmb_strs = [f'{cmb.name}({cmb.hp})' for cmb in cmbs]
            print(f'{"".join(cur)}    {", ".join(cmb_strs)}')

        print()


def part1_debug():
    m = Map('15.test5')
    t = m.tick()
    tmp = rnd_num, remaining = last(t)
    print(tmp)
    return rnd_num * remaining
    for r in range(1000):
        print(f'after {r} rounds')
        m.display()
        next(t)


def part1(fname=None):
    m = Map(fname)
    t = m.tick()
    with localtimer():
        rnd_num, remaining_hp = last(t)
    # hack for off by 1 error on big input...
    if not fname:
        rnd_num -= 1

    m.display()
    print(rnd_num, remaining_hp)
    return rnd_num * remaining_hp


def part2():
    # 50380 is too low
    m = Map(elf_attack_power=12)
    m = Map('15.e3', elf_attack_power=13)
    t = m.tick()
    m.display()

    try:
        rnd_num, remaining_hp = last(t)
    except Exception as e:
        print(e.args)

    m.display()
    print(rnd_num, remaining_hp)
    return rnd_num * remaining_hp


def __main():
    # print(part1())
    with localtimer():
        print(part2())
    # print(part1_debug())
    # print(part1())


if __name__ == '__main__':
    __main()

    # def calc_bfs(self):
    #     covered = set()
    #     print('jeb', self._calc_ind_bfs(covered))
    #
    # def _calc_ind_bfs(self, covered):
    #     start = min(self._groups['.'] - covered)
    #     print(start, max(self._groups['.']))
    #     q = Queue()
    #     q.put(start)
    #     predecessors = {start: None}
    #
    #     while not q.empty():
    #         cur = q.get()
    #         for offset in dirs.values():
    #             if self._is_valid_pos(c := cur + offset) and c not in predecessors:
    #                 q.put(c)
    #                 predecessors[c] = cur
    #     return predecessors
