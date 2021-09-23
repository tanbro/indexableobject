import unittest

from indexableobject import *


class NamesTestCase(unittest.TestCase):

    MAPPINGS = [
        {
            'boo': 'foo',
            'bar': 'far',
        },
        {
            ' boo': 'foo',
            ' bar': 'far',
        },
        {
            'boo ': 'foo',
            'bar ': 'far',
        },
        {
            '_boo': 'foo',
            '_bar': 'far',
        },
        {
            'boo_': 'foo',
            'bar_': 'far',
        },
        {
            '_boo_': 'foo',
            '_bar_': 'far',
        },
        {
            '1_2_3': object(),
            '1-2-3': object(),
            '1.2.3': object(),
        },
        {
            '你好': '世界',
            '再见': '宇宙',
        },
        {
            '_': object(),
            '_ _': object(),
            '__': object(),
            '__ ': object(),
            ' __': object(),
            ' __ ': object(),
            ' __x__': object(),
            '__x__ ': object(),
        }
    ]

    def test_names_and_values(self):
        for d in self.MAPPINGS:
            ac = IndexableObject(d)

            self.assertEqual(len(ac), len(d))
            self.assertEqual(sorted(ac), sorted(d.keys()))

            for k in d.keys():
                self.assertIn(k, ac)

            for k, v in d.items():
                if k.isidentifier():
                    self.assertEqual(v, getattr(ac, k))

            for k, v in d.items():
                self.assertEqual(v, ac[k])

            for k, v in d.items():
                self.assertEqual(v, ac(k))

    def test_non_indentity_names(self):
        ds = [
            {' __x__': object},
            {'123': object},
            {'a-b-c': object},
            {' abc': object},
            {'abc ': object},
            {'': object},
            {' ': object},
            {' \n ': object}
        ]
        for d in ds:
            ac = IndexableObject(d)
            for k in d:
                with self.assertRaises(AttributeError):
                    getattr(ac, k)
                self.assertEqual(ac[k], d[k])

    def test_wrong_name_types(self):
        ds = [
            {1: object()},
            {0: object()},
            {True: object()},
            {False: object()},
            {None: object()},
            {object(): object()},
            {object: object()},
            {(1, 2, 3): object()},
        ]
        for d in ds:
            ac = IndexableObject(d)
            for k in d:
                with self.assertRaises(TypeError):
                    getattr(ac, k)
                self.assertEqual(ac[k], d[k])