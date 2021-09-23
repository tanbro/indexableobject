import pickle
import unittest

from indexableobject import *


class PickleTestCase(unittest.TestCase):


    def test_simple_data(self):
        d = {
            'boo': 'foo'
        }

        a = IndexableObject(d)
        data = pickle.dumps(a)
        b = pickle.loads(data)

        for k, v in d.items():
            self.assertEqual(v, getattr(b, k))
       
    def test_simple_invalid_key(self):
        d = {
            'invalid-attr-name': 'bar',
            1: 'baz1',
            2.0: 'baz2',
            True: True,
            False: False,
            None: 'none'
        }

        a = IndexableObject(d)
        data = pickle.dumps(a)
        b = pickle.loads(data)

        for k, v in d.items():
            if isinstance(k, str) and k.isidentifier():
                self.assertEqual(v, getattr(b, k))
            self.assertEqual(v, b[k])

    def test_nested_dict(self):
        d = {
            'boo': {
                'foo': [
                    {'bar': 'foobar1'},
                    {'bar': 'foobar2'},
                ]
            }
        }

        a = from_dict(d)
        data = pickle.dumps(a)
        b = pickle.loads(data)

        for i, foo in enumerate(b.boo.foo):
            self.assertEqual(foo.bar, d['boo']['foo'][i]['bar'])
            self.assertEqual(foo['bar'], d['boo']['foo'][i]['bar'])