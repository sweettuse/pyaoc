from pyaoc2019.utils import get_file_path


def parse_file(name):
    path = get_file_path(name)
    with open(path) as f:
        chunks = f.read().split('\n\n')
    return [[int(v) for v in chunk.splitlines()] for chunk in chunks]


def part1():
    data = parse_file(1)
    return max(map(sum, data))


def part2():
    data = parse_file(1)
    return sum(sorted(map(sum, data))[-3:])


print(part1())
print(part2())
