# IndexableObject

IndexableObject is a Python class with both dictionary and attribute style accessing to it's data member.

It's serializable(pickle), iterable, and indexable.

## Basic usage

IndexableObject is an object that allow it's elements to be accessed both as keys and attributes.

We create it from a dictionary or a list of dictionary, and vice versa.

```python
>>> from indexableobject import from_dict, to_dict
>>> a = from_dict({'foo': 'bar'})
>>> a.foo
'bar'
>>> a['foo']
'bar'
to_dict(a)
{'foo': 'bar'}
```

## Valid names

Any variable that:

1. is a `str` object,
1. and is an identifier (see: <https://docs.python.org/3/library/stdtypes.html#str.isidentifier>)
1. and does not both start and end with `"__"`

can be used as both attribute and key name.

Any hash-able object can be used as key, but not attribute name.

```python
>>> from indexableobject import IndexableObject
>>> a = IndexableObject()
>>> a.foo = 'bar'
>>> a.foo
'bar'
>>> a['foo']
'bar'
>>> a['foo'] = 'baz'
>>> a.foo
'baz'
>>> a['foo']
'baz'
>>> a['你好'] = 'Hello'
>>> a.你好
'Hello'
```

## Sequence

The `IndexableObject` can be created from Iterable/Sequence object.

We can access sequence item by it's index number:

```python
>>> from indexableobject import from_dict
>>> a = from_dict([{'a': 'foo'}, {'a': 'bar'}])
>>> a[1].a
'bar'
>>> a[1]['a']
'bar'
```

Since `from_dict` is recursive, we can access items of a sequence inside mappings:

```python
>>> from indexableobject import from_dict
>>> a = from_dict({'value': [{'a': 'foo'}, {'a': 'bar'}]})
>>> a['value']
[<IndexableObject object at 0x7ff7f32f4790 a='foo'>, <IndexableObject object at 0x7ff7f32f4a90 a='bar'>]
>>> a.value[0]
<IndexableObject object at 0x7ff7f32f4790 a='foo'>
>>> a.value[0].a
'foo'
>>> a.value[0]['a']
'foo'
```

Iterable will be converted to sequence:

```python
>>> from indexableobject import from_dict
>>> it = range(10)
>>> a = from_dict({'range': it})
>>> a
<IndexableObject object at 0x7ff7f3bf9100 range=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]>
>>> a.range[9]
9
>>> a['range'][2]
2
```

## Default value

A direct call to a `IndexableObject` object just does that:

```python
>>> a = from_dict({'n': 1})
>>> a.n
1
>>> a['n']
1
>>> a('n')
1
>>> a('n', default=0)
1
>>> a.m
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'IndexableObject' object has no attribute 'm'
>>> a['m']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'IndexableObject' object has no attribute 'm'
>>> a('m')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'IndexableObject' object has no attribute 'm'
>>> a('m', 0)
0
```

## Contains, iter and len

Use `in` operation to check if key or attribute exsisted:

```python
>>> from indexableobject import from_dict
>>> a = from_dict({'x': object()})
>>> 'x' in a
True
>>> 'y' in a
False
>
```

Iterate the object will get it's all keys and attribute names, call `len` get it's length:

```python
>>> from indexableobject import IndexableObject
>>> a = IndexableObject()
>>> a.hello = 'world'
>>> a[1] = 'it is 1'
>>> a
<IndexableObject object at 0x7fcd4330c100 hello='world' 1='it is 1'>
>>> list(a)
['hello', 1]
>>> len(a)
2
```

## Update and merge

There are `merge` and `update` functions in the module:

Usage of `merge`:

```python
from indexableobject import from_dict, merge
>>> a = from_dict({'x': 1})
>>> b = from_dict({'y': 2})
>>> c = merge(a, b)
>>> c
<IndexableObject object at 0x7ff7f3c63a90 x=1 y=2>
>>> a
<IndexableObject object at 0x7ff7f3c63fa0 x=1>
>>> b
<IndexableObject object at 0x7ff7f3bf9100 y=2>
>>>
```

Usage of `update`:

```python
from indexableobject import from_dict, update
>>> update(a, b)
<IndexableObject object at 0x7ff7f3c63fa0 x=1 y=2>
>>> a
<IndexableObject object at 0x7ff7f3c63fa0 x=1 y=2>
>>> b
<IndexableObject object at 0x7ff7f3bf9100 y=2>
```

or you can use `|` , `|=` operator directly:

```python
from indexableobject import from_dict
>>> a = from_dict({'x': 1})
>>> b = from_dict({'y': 2})
>>> a | b
<IndexableObject object at 0x7ff7f3ac7d60 x=1 y=2>
>>> a
<IndexableObject object at 0x7ff7f3ac7400 x=1>
>>> a|=b
>>> a
<IndexableObject object at 0x7ff7f3ac7400 x=1 y=2>
```
