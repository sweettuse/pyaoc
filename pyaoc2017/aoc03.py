__author__ = 'acushner'

from itertools import count

data = 312051


def get_closest_odd_square(data):
    for i in count(1, 2):
        if i ** 2 > data:
            return i - 1


def __main():
    closest = get_closest_odd_square(data)
    perim_start = closest ** 2 + 1
    print(closest, perim_start, data - perim_start)


if __name__ == '__main__':
    __main()
