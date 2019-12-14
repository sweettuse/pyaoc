import time
from contextlib import contextmanager
from pathlib import Path

__author__ = 'acushner'

path = Path('/Users/acushner/software/pyaoc2019/pyaoc2019/inputs')


def read_file(name):
    with open(path / name) as f:
        return list(map(str.strip, f.readlines()))


@contextmanager
def localtimer():
    start = time.perf_counter()
    yield
    print('func took', time.perf_counter() - start)


def __main():
    pass


if __name__ == '__main__':
    __main()
