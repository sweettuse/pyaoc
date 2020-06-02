__author__ = 'acushner'

import re
from typing import NamedTuple, List, Set

from cytoolz import comp

from pyaoc2019.utils import read_file


class IPV7(NamedTuple):
    addresses: List[str]
    hypernets: List[str]

    @classmethod
    def from_str(cls, s: str):
        r = '|'
        s = s.replace('[', r).replace(']', r)
        fields = s.split(r)
        return cls(fields[::2], fields[1::2])

    @property
    def supports_tls(self):
        return any(map(_contains_abba, self.addresses)) and not any(map(_contains_abba, self.hypernets))

    @property
    def supports_ssl(self):
        a_babs = set().union(*map(comp(_create_corresponding_babs, _get_babs), self.addresses))
        h_babs = set().union(*map(_get_babs, self.hypernets))
        return bool(a_babs & h_babs)


def _contains_abba(s: str):
    for i in range(len(s) - 3):
        cur = s[i: i + 4]
        if cur[:2] == cur[:-3:-1] and len(set(cur)) != 1:
            return True
    return False


def aoc07_a(ips: List[IPV7]):
    """determine if ipv7 address supports TLS (transport-layer snooping)"""
    return sum(ip.supports_tls for ip in ips)


def _is_bab(s):
    return s[0] == s[-1] and len(set(s)) > 1


def _get_babs(s: str):
    return {cur for i in range(len(s) - 2) if _is_bab(cur := s[i: i + 3])}


def _create_corresponding_babs(s: Set[str]):
    return {f'{w[1:]}{w[1]}' for w in s}


def aoc07_b(ips: List[IPV7]):
    """determine if ipv7 address supports TLS (transport-layer snooping)"""
    return sum(ip.supports_ssl for ip in ips)


def __main():
    ips = [IPV7.from_str(s) for s in read_file(7, 2016)]
    print(aoc07_a(ips))
    print(aoc07_b(ips))


if __name__ == '__main__':
    __main()
