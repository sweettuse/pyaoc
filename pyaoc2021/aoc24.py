from __future__ import annotations
from concurrent.futures import ProcessPoolExecutor, wait
from functools import reduce
from itertools import chain
from operator import or_
import random


from pyaoc2019.utils import Pickle, read_file, mapt, timer, chunks, exhaust
from typing import Iterable, NamedTuple, Union

__author__ = 'acushner'


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'
    return list(filter(bool, read_file(filename, 2021)))


class ALU:
    def __init__(self, model_num: str | Iterable[str], *, debug=False) -> None:
        self._vals = dict.fromkeys('wxyz', 0)
        self._inputs = enumerate(map(int, model_num), 1)
        self._model_num = ''.join(model_num)
        self._debug = debug

    def __setitem__(self, key, value):
        self._vals[key] = value

    def __getitem__(self, key):
        return self._vals[key]

    def get(self, key) -> int:
        if key in self._vals:
            return self._vals[key]
        return int(key)

    def inp(self, a: str):
        idx, val = next(self._inputs)
        if self._debug:
            print(f'{idx:-^12}')
        self[a] = val

    def add(self, a: str, b: str):
        self[a] += self.get(b)

    def mul(self, a: str, b: str):
        self[a] *= self.get(b)

    def div(self, a: str, b: str):
        self[a] //= self.get(b)

    def mod(self, a: str, b: str):
        self[a] %= self.get(b)

    def eql(self, a: str, b: str):
        self[a] = int(self[a] == self.get(b))

    def ass(self, a: str, b: str):
        self[a] = self.get(b)

    def __repr__(self):
        return f'ALU({self._model_num}, {self._vals})'

    def execute_one(self, inst: str):
        cmd, *rest = inst.split()
        getattr(self, cmd)(*rest)
        if self._debug:
            print(self)

    def execute(self, inst: Union[str, list[str]]):
        if isinstance(inst, str):
            return self.execute_one(inst)
        for i in inst:
            self.execute_one(i)


class Hardcoded:
    def __init__(self, num: str | int) -> None:
        self.num = str(num)

    def run(self):
        num_iter = iter(self.num)
        x, y, z = self.num01(next(num_iter))
        x, y, z = self.num02(next(num_iter), z)

    @staticmethod
    def num01(w):
        x = 1
        z = y = w + 1
        return x, y, z

    @staticmethod
    def num02(w, z):
        x = 1
        z *= 26
        y = (w + 11) * x
        z += y
        return x, y, z

    @staticmethod
    def num03(w, z):
        x = 1
        pass


def play():
    alu = ALU('38')
    alu.execute('inp z')
    alu.execute('inp x')
    alu.execute('mul z 3')
    alu.execute('eql z x')
    print(alu)


def part1_play():
    instructions = parse_data()
    start = 2
    offset = 4
    num = base_num = [str(start)] * 12 + list('01')
    for i in range(15):
        cur = ''.join(num)
        alu = ALU(cur)
        alu.execute(instructions)
        print(cur, alu)
        if i < 14:
            num = base_num.copy()
            num[i] = str(start + offset)


def _mp_helper(nums: list[int]) -> list[dict[str, int]]:
    res = {}
    instructions = parse_data(debug=True)
    for num in nums:
        alu = ALU(str(num))
        alu.execute(instructions)
        res[num] = alu._vals | dict(num=int(num))
    return list(res.values())


@timer
def random_explore_mp(n=1_000):
    options = '123456789'
    num_procs = 8
    start = '9999'
    end = ''

    def _gen_nums():
        seen: set[int] = set()
        while len(seen) < n:
            _num = start + ''.join(random.choices(options, k=14 - len(start) - len(end))) + end
            seen.add(int(_num))
        return seen

    futures = []
    nums = _gen_nums()
    pool = ProcessPoolExecutor(num_procs)

    for c in chunks(nums, len(nums) // num_procs + 1):
        futures.append(pool.submit(_mp_helper, c))
    Pickle.write(alu_newest=list(chain.from_iterable(f.result() for f in futures)))


    
@timer
def random_explore(n=1_000):
    instructions = parse_data(debug=True)
    res = {}
    options = '123456789'

    def get_num():
        while True:
            start = ''
            end = ''
            _num = start + ''.join(random.choices(options, k=14 - len(start) - len(end))) + end
            # assert len(_num) == 14
            if _num not in res:
                return int(_num)

    for _ in range(n):
        num = get_num()
        alu = ALU(str(num))
        alu.execute(instructions)
        res[num] = alu._vals | dict(num=int(num))
    Pickle.write(alu=list(res.values()))


def test():
    instructions = parse_data(debug=True)
    alu = ALU(14 * '2', debug=True)
    print('==================')
    alu.execute(instructions)
    print('==================')
    assert alu['z'] == 41645335

    num = 14 * '3'
    # num[5] = '5'
    alu = ALU(num, debug=True)
    print('==================')
    alu.execute(instructions)
    print('==================')
    assert alu['z'] == 54001966, alu['z']


@timer
def time_test(n, instructions):
    for _ in range(n):
        alu = ALU(14 * '9')
        alu.execute(instructions)


def part1():
    # NOTE: highest max so far = 92647271386892
    test()
    # return time_test(100_000, parse_data(debug=True))
    return random_explore_mp(100_000_000)
    # return time_test()
    return part1_play()
    instructions = parse_data()
    # num = int(12 * '1' + '99')
    # num = '13579246899999'
    first = 7
    last = 14 - first
    for i in range(1, 10):
        num = int(first * f'{i}' + (last - 1) * '8' + '8')
        alu = ALU(str(num))
        for inst in instructions:
            alu.execute(inst)
        print(num, alu)


def __main():
    part1()


if __name__ == '__main__':
    __main()
