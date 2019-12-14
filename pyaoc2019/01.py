import utils as U

__author__ = 'acushner'

data = U.read_file('01')


def calc_fuel(mass):
    return max(0, (mass // 3) - 2)


def calc_fuel2(mass):
    mass = calc_fuel(mass)
    return mass + (calc_fuel2(mass) if mass else 0)


def aoc(f):
    return sum(f(m) for m in map(int, data))


def aoc_2():
    pass


def __main():
    print(aoc(calc_fuel))
    print(aoc(calc_fuel2))


if __name__ == '__main__':
    __main()
