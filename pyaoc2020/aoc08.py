from pyaoc2019.utils import read_file, timer

__author__ = 'acushner'

data = [(inst, int(val)) for inst, val in map(str.split, read_file(8, 2020))]


class Interpreter:
    def __init__(self, insts):
        self._insts = insts
        self._acc = 0
        self._pc = 0
        self._seen = set()

    def run(self):
        while self._pc not in self._seen:
            self._seen.add(self._pc)
            inst, val = self._insts[self._pc]
            getattr(self, inst)(val)
            self._pc += 1
        return self._acc

    def acc(self, val):
        self._acc += val

    def jmp(self, val):
        self._pc += val - 1

    def nop(self, _):
        pass


def part1():
    return Interpreter(data).run()


def part2():
    sub = dict(jmp='nop', nop='jmp')
    for i, (inst, val) in enumerate(data):
        if inst in sub:
            d = data.copy()
            d[i] = sub[inst], val
            inter = Interpreter(d)
            try:
                inter.run()
            except IndexError:
                return inter._acc


@timer
def __main():
    print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
