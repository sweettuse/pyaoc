from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, field
from math import prod
from typing import Literal, TypeAlias

from pyaoc2019.utils import exhaust, read_file



class SendList(list):
    def send(self, v):
        self.append(v)
class Factory:
    def __init__(self):
        self.outputs = defaultdict(SendList)
        self.bots = {}

    @classmethod
    def from_insts(cls, insts: list[str]) -> Factory:
        """
        'value 23 goes to bot 208'
        'bot 125 gives low to bot 58 and high to output 57'
        """
        res = cls()
        def parse_input(s: str):
            _, val, *_, target = s.split()
            res.bots[int(target)].send(int(val))
            
        inputs = []
        for inst in insts:
            if inst.startswith('value'):
                inputs.append(inst)
            else:
                res.create_bot(inst)

        exhaust(parse_input, inputs)
        return res

    @property
    def bot(self):
        return self.bots

    @property
    def output(self):
        return self.outputs


    def create_bot(self, s: str):
        """ 'bot 48 gives low to bot 111 and high to bot 102' """
        fields = s.split()
        idxs = 1, 5, 6, 10, 11
        bot_id, low_type, low_id, high_type, high_id = (fields[i] for i in idxs)
        bot_id, low_id, high_id = map(int, (bot_id, low_id, high_id))

        def bot_task():
            while True:
                v1 = yield
                v2 = yield
                low, high = sorted((v1, v2))
                if (low, high) == (17, 61):
                    print('part1:', bot_id)
                getattr(self, low_type)[low_id].send(low)
                getattr(self, high_type)[high_id].send(high)
        
        bt = bot_task()
        next(bt)
        self.bots[bot_id] = bt
        

    def part2(self):
        print('part2:', prod(self.output[i][0] for i in range(3)))

def __main():
    insts = read_file(10, 2016)
    f = Factory.from_insts(insts)
    f.part2()


if __name__ == '__main__':
    __main()
