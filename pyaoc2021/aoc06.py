from more_itertools import first

from pyaoc2019.utils import read_file, mapt

__author__ = 'acushner'


def parse_data(*, debug=False):
    if debug:
        data = read_file('06.test', 2021)
    else:
        data = read_file(6, 2021)

    return mapt(int, first(data).split(','))


def part1and2(data, num_days):
    buckets = dict.fromkeys(range(7), 0)
    for n in data:
        buckets[n] += 1

    num_8s = 0
    num_7s = 0
    mod7 = lambda n: n % 7
    for day in map(mod7, range(num_days)):
        to_add = num_7s
        num_7s = num_8s
        num_8s = buckets[day]
        buckets[day] += to_add

    return sum(buckets.values()) + num_7s + num_8s


def __main():
    data = parse_data(debug=False)
    print(part1and2(data, 80))
    print(part1and2(data, 256))


if __name__ == '__main__':
    __main()
