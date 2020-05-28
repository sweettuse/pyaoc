# cluegen.py
#
# Classes generated from type clues.
#
#     https://github.com/dabeaz/cluegen
#
# Author: David Beazley (@dabeaz).
#         http://www.dabeaz.com
#
# Copyright (C) 2018-2020.
#
# Permission is granted to use, copy, and modify this code in any
# manner as long as this copyright message and disclaimer remain in
# the source code.  There is no warranty.  Try to use the code for the
# greater good.

import types

# Collect all type clues from a class and base classes.
from functools import partial


def all_clues(cls):
    clues = {}
    for c in reversed(cls.__mro__):
        clues.update(getattr(c, '__annotations__', {}))
    return clues


# Decorator to define methods of a class as a code generator.
def cluegen(func):
    def __get__(self, instance, cls):
        locs = {}
        code = func(cls)
        exec(code, locs)
        meth = locs[func.__name__]
        setattr(cls, func.__name__, meth)
        return meth.__get__(instance, cls)

    def __set_name__(self, cls, name):
        methods = cls.__dict__.get('_methods', list(cls._methods))
        if '_methods' not in cls.__dict__:
            cls._methods = methods
        cls._methods.append((name, self))

    return type(f'ClueGen_{func.__name__}', (), dict(__get__=__get__,
                                                     __set_name__=__set_name__))()


# Base class for defining data structures
class DatumBase:
    __slots__ = ()
    _methods = []

    @classmethod
    def __init_subclass__(cls):
        submethods = []
        for name, val in cls._methods:
            if name not in cls.__dict__:
                setattr(cls, name, val)
                submethods.append((name, val))
            elif val is cls.__dict__[name]:
                submethods.append((name, val))

        if submethods != cls._methods:
            cls._methods = submethods


class Datum(DatumBase):
    __slots__ = ()

    @cluegen
    def __init__(cls):
        clues = all_clues(cls)
        args = ', '.join(f'{name}={getattr(cls, name)!r}'
                         if hasattr(cls, name) and not isinstance(getattr(cls, name),
                                                                  types.MemberDescriptorType) else name
                         for name in clues)
        body = cls._gen_init_body(clues)
        return f'def __init__(self, {args}):\n{body}\n'

    @classmethod
    def _gen_init_body(cls, clues):
        return '\n'.join(f'    self.{name} = {name}' for name in clues)

    @cluegen
    def __repr__(cls):
        clues = all_clues(cls)
        fmt = ', '.join('%s={self.%s!r}' % (name, name) for name in clues)
        return 'def __repr__(self):\n' \
               '    return f"{type(self).__name__}(%s)"' % fmt

    @cluegen
    def __iter__(cls):
        clues = all_clues(cls)
        values = '\n'.join(f'   yield self.{name}' for name in clues)
        return 'def __iter__(self):\n' + values

    @cluegen
    def __eq__(cls):
        clues = all_clues(cls)
        selfvals = ','.join(f'self.{name}' for name in clues)
        othervals = ','.join(f'other.{name}' for name in clues)
        return 'def __eq__(self, other):\n' \
               '    if self.__class__ is other.__class__:\n' \
               f'        return ({selfvals},) == ({othervals},)\n' \
               '    else:\n' \
               '        return NotImplemented\n'

    @cluegen
    def __hash__(cls):
        clues = all_clues(cls)
        if clues:
            self_tuple = '(' + ','.join(f'self.{name}' for name in clues) + ',)'
        else:
            self_tuple = '()'
        return 'def __hash__(self):\n' \
               f'    return hash({self_tuple})\n'


class FrozenDatum(Datum):
    @classmethod
    def _gen_init_body(cls, clues):
        res = ['    def _frozen_error(*_):']
        res.append('        raise AttributeError("can\'t set/del attr on FrozenDatum")')
        res.append('    _frozen_prop = lambda fget: property(fget, _frozen_error, _frozen_error)')
        res.append(f'    cls = type(self)')
        res.extend(f'    cls.{name} = _frozen_prop(lambda _: {name})' for name in clues)
        return '\n'.join(res)


# Example use
if __name__ == '__main__':
    # Start defining classes
    class Coordinates(Datum):
        x: int
        y: int
