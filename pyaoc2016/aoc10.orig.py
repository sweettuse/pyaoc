from collections import defaultdict, Counter
from typing import List

__author__ = 'acushner'

from more_itertools import first

from pyaoc2019.utils import read_file, exhaust


def parse_instructions(insts: List[str]):
    val_inst, bot_inst = {}, {}

    def _parse_val_inst():
        val_inst[int(fields[1])] = int(fields[-1])

    def _parse_bot_inst():
        bot_inst[int(fields[1])] = int(fields[6]), int(fields[-1])

    funcs = dict(value=_parse_val_inst, bot=_parse_bot_inst)
    for inst in insts:
        fields = inst.split()
        funcs[fields[0]]()

    return val_inst, bot_inst


class ResExc(Exception):
    pass


class Factory:
    def __init__(self, insts, target=None):
        val_insts, self._bot_insts = parse_instructions(insts)
        self._bots = self._init_bots(val_insts)
        self._target = sorted(target or ())

    @staticmethod
    def _init_bots(val_insts):
        res = defaultdict(list)
        for val, bot_id in val_insts.items():
            res[bot_id].append(val)
        return res

    def _update_bot(self, bot_id):
        ids = l_id, h_id = self._bot_insts[bot_id]
        try:
            pot_target = l, h = sorted(self._bots[bot_id])
            if self._target == pot_target:
                raise ResExc(bot_id)
        except ValueError:
            return
        self._bots[bot_id].clear()
        self._bots[l_id].append(l)
        self._bots[h_id].append(h)
        exhaust(map(self._update_bot, ids))

    def run(self):
        start = first(bot_id for bot_id, vals in self._bots.items() if len(vals) == 2)
        try:
            self._update_bot(start)
        except ResExc as e:
            return first(e.args)


def __main():
    # f = Factory(read_file('10.test', 2016), target=(5, 2))
    f = Factory(read_file(10, 2016), target=(17, 61))
    print(f.run())


if __name__ == '__main__':
    __main()
