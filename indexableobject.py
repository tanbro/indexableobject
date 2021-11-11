import re
from collections import deque
from itertools import chain, count
from typing import Any, Hashable, Iterable, Iterator, Mapping, Union

__all__ = ['IndexableObject', 'to_dict', 'update', 'merge', 'from_dict']


DEFAULT_ARG = object()
INTERNAL_NAME_PAT = re.compile(r'_{2}\S+_{2}')
ITERABLE_SCALAR_TYPES = str, bytes, bytearray, memoryview


class IndexableObject:
    """
    IndexableObject can make an object with both dictionary and attribute style access to it's data member.
    It can be used in `RestrictedPython <http://restrictedpython.readthedocs.io/>`_

    eg::

        >>> obj = IndexableObject()
        >>> obj.a = 'this is a'
        >>> obj['a']
        'this is a'
        >>> obj['b'] = 'this is b'
        >>> obj.b
        'this is b'
        >>> obj('a')
        'this is a'
        >>> obj('c', 'default value when not exists')
        'default value when not exists'
        >>> print(obj('c'))
        None
        >>> 'b' in obj
        True
        >>> list(obj)
        ['a', 'b]
        >>> len(obj)
        2
    """

    def __init__(self, initialdata: Union['IndexableObject', Mapping] = None):
        setattr(self, '__x_attrs__', dict())

        if isinstance(initialdata, Mapping):
            for k, v in initialdata.items():
                self.__setitem__(k, v)
        elif initialdata is not None:
            for k in initialdata:
                self.__setitem__(k, initialdata[k])

    def __getitem__(self, key: Hashable) -> Any:
        if isinstance(key, str) and key.isidentifier() and not re.match(INTERNAL_NAME_PAT, key):
            return getattr(self, key)
        return getattr(self, '__x_attrs__')[key]

    def __setitem__(self, key: Hashable, value: Any):
        if isinstance(key, str) and key.isidentifier() and not re.match(INTERNAL_NAME_PAT, key):
            setattr(self, key, value)
        else:
            getattr(self, '__x_attrs__')[key] = value

    def __delitem__(self, key: Hashable):
        if isinstance(key, str) and key.isidentifier() and not re.match(INTERNAL_NAME_PAT, key):
            delattr(self, key)
        else:
            del getattr(self, '__x_attrs__')[key]

    def __call__(self, key: Hashable, default: Any = DEFAULT_ARG) -> Any:
        if isinstance(key, str) and key.isidentifier() and not re.match(INTERNAL_NAME_PAT, key):
            if default == DEFAULT_ARG:
                return getattr(self, key)
            else:
                return getattr(self, key, default)
        else:
            if default == DEFAULT_ARG:
                return getattr(self, '__x_attrs__')[key]
            else:
                return getattr(self, '__x_attrs__').get(key, default)

    def __contains__(self, key: Hashable) -> bool:
        if isinstance(key, str) and key.isidentifier() and not re.match(INTERNAL_NAME_PAT, key):
            return hasattr(self, key)
        else:
            return key in getattr(self, '__x_attrs__')

    def __iter__(self) -> Iterator[Hashable]:
        return chain(
            (
                name for name in dir(self)
                if name.isidentifier() and not re.match(INTERNAL_NAME_PAT, name)
            ),
            getattr(self, '__x_attrs__'),
        )

    def __len__(self) -> int:
        counter = count()
        deque(zip(self.__iter__(), counter), maxlen=0)
        return next(counter)

    def __str__(self) -> str:
        return '<{} object at 0x{:x}>'.format(
            self.__class__.__name__, id(self)
        )

    def __repr__(self) -> str:
        values_text = ' '.join(
            '{}={!r}'.format(k, self.__getitem__(k))
            for k in self.__iter__()
        )
        return '<{} object at 0x{:x} {}>'.format(
            self.__class__.__qualname__, id(self), values_text
        )

    def __or__(self, other: Union['IndexableObject', Mapping]) -> 'IndexableObject':
        new = IndexableObject(self)
        if isinstance(other, Mapping):
            for k, v in other.items():
                new[k] = v
        else:
            for k in other:
                new[k] = other[k]
        return new

    def __ior__(self, other: Union['IndexableObject', Mapping]) -> 'IndexableObject':
        if isinstance(other, Mapping):
            for k, v in other.items():
                self[k] = v
        else:
            for k in other:
                self[k] = other[k]
        return self

    def __guarded_setitem__(self, key, value):
        self.__setitem__(key, value)

    def __guarded_delitem__(self, key):
        self.__delitem__(key)

    def __guarded_setattr__(self, name, value):
        self.__setattr__(name, value)

    def __guarded_delattr__(self, name):
        self.__delattr__(name)


def update(this: IndexableObject, other: Union[IndexableObject, Mapping]) -> IndexableObject:
    this |= other
    return this


def merge(this: IndexableObject, other: Union[IndexableObject, Mapping]) -> IndexableObject:
    return this | other


def to_dict(obj):
    if isinstance(obj, IndexableObject):
        return {k: to_dict(obj[k]) for k in obj}
    if isinstance(obj, Mapping):
        return {k: to_dict(v) for k, v in obj.items()}
    if isinstance(obj, Iterable) and not isinstance(obj, ITERABLE_SCALAR_TYPES):
        return [to_dict(i) for i in obj]
    return obj


def from_dict(obj):
    if isinstance(obj, IndexableObject):
        return IndexableObject({k: from_dict(obj[k]) for k in obj})
    if isinstance(obj, Mapping):
        return IndexableObject({k: from_dict(v) for k, v in obj.items()})
    if isinstance(obj, Iterable) and not isinstance(obj, ITERABLE_SCALAR_TYPES):
        return [from_dict(i) for i in obj]
    return obj
