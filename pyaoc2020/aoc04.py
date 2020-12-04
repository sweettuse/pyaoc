from contextlib import suppress
import string
from math import prod

from pyaoc2019.colors.tile_utils import RC
from pyaoc2019.utils import read_file, timer

__author__ = 'acushner'


def is_num(v, v_min, v_max, v_len):
    if len(v) != v_len:
        return False
    with suppress(TypeError):
        v = int(v)
        return v_min <= v <= v_max


def hgt(v):
    unit = v[-2:]
    v = v[:-2]
    if unit == 'in':
        return is_num(v, 59, 76, 2)
    elif unit == 'cm':
        return is_num(v, 150, 193, 3)


def hcl(v):
    return len(v) == 7 and v.startswith('#') and all(d in '0123456789abcdef' for d in v[1:])


def ecl(v):
    return v in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}


def pid(v):
    return len(v) == 9 and v.isdigit()


req_fields = {'byr': lambda v: is_num(v, 1920, 2002, 4),
              'iyr': lambda v: is_num(v, 2010, 2020, 4),
              'eyr': lambda v: is_num(v, 2020, 2030, 4),
              'hgt': hgt,
              'hcl': hcl,
              'ecl': ecl,
              'pid': pid}
optional = {'cid'}


def parse_data():
    res = []
    cur = {}
    for line in read_file(4, 2020):
        if not line:
            res.append(cur)
            cur = {}
        for field in line.split():
            k, v = field.split(':')
            cur[k] = v
    if cur:
        res.append(cur)
    return res


passports = parse_data()


def _get_passports_with_valid_fields():
    return [p for p in passports if len(p.keys() & req_fields) == len(req_fields)]


def part1():
    return len(_get_passports_with_valid_fields())


def part2():
    def _validate_passport(p):
        return all(req_fields.get(field, lambda _: True)(value) for field, value in p.items())

    return sum(map(_validate_passport, _get_passports_with_valid_fields()))


@timer
def __main():
    print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
