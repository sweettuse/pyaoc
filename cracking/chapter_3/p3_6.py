__author__ = 'acushner'

# 3.6 Animal Shelter: An animal shelter, which holds only dogs and cats, operates on a strictly"first in, first
# out" basis. People must adopt either the "oldest" (based on arrival time) of all animals at the shelter,
# or they can select whether they would prefer a dog or a cat (and will receive the oldest animal of
# that type). They cannot select which specific animal they would like. Create the data structures to
# maintain this system and implement operations such as enqueue, dequeueAny, dequeueDog,
# and dequeueCat. You may use the built-in Linked list data structure.
# Hints: #22, #56, #63
from collections import defaultdict
from enum import Enum
from itertools import count
from typing import NamedTuple

from cracking.chapter_3 import Queue


class AnimalType(Enum):
    cat = 'cat'
    dog = 'dog'
    ferret = 'ferret'


class Animal(NamedTuple):
    type: AnimalType
    ts: int

    def __str__(self):
        return f'{self.type.value}_{self.ts}'


class Shelter:

    def __init__(self):
        self._queues = defaultdict(Queue)
        self._time = count()

    def add(self, a_type: AnimalType):
        animal = Animal(a_type, next(self._time))
        self._queues[a_type].add(animal)

    def dequeue(self, a_type: AnimalType = None):
        if a_type:
            return self._queues[a_type].remove()
        res = None
        min_ts = float('inf')
        for q in self._queues.values():
            if q and (animal := q.peek()) and animal.ts < min_ts:
                res = q
                min_ts = animal.ts
        if res:
            return res.remove()


def __main():
    s = Shelter()
    s.add(AnimalType.cat)
    s.add(AnimalType.cat)
    s.add(AnimalType.dog)
    s.add(AnimalType.dog)
    s.add(AnimalType.cat)
    s.add(AnimalType.ferret)
    s.add(AnimalType.cat)
    s.add(AnimalType.cat)
    print(s.dequeue(AnimalType.dog))
    print(s.dequeue())
    print(s.dequeue())
    print(s.dequeue(AnimalType.ferret))
    print(s.dequeue())
    print(s.dequeue())
    print(s.dequeue())
    print(s.dequeue())
    print(s.dequeue())
    print(s.dequeue())


if __name__ == '__main__':
    __main()
