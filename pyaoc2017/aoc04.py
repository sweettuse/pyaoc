import pyaoc2019.utils as U

__author__ = 'acushner'

data = U.read_file(4, 2017)
data = [v.split() for v in data]


def valid_1(data):
    return [ws for ws in data if len(set(ws)) == len(ws)]


def valid_2(data):
    data = [[''.join(sorted(w)) for w in words] for words in data]
    return valid_1(data)


def aoc04_a():
    return len(valid_1(data))


def aoc04_b():
    return len(valid_2(valid_1(data)))


def __main():
    print(aoc04_a())
    print(aoc04_b())
    pass


if __name__ == '__main__':
    __main()
