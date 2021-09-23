import unittest

from indexableobject import *


class UnionTestCase(unittest.TestCase):

    def test_opt_or(self):
        a = IndexableObject(dict(a='a'))
        b = IndexableObject(dict(b='b'))

        new = a | b
        self.assertEqual(new.a, 'a')
        self.assertEqual(new.b, 'b')
        self.assertNotIn('b', a)
        self.assertNotIn('a', b)

    def test_merge(self):
        a = IndexableObject(dict(a='a'))
        b = dict(b='b')

        new = merge(a, b)
        self.assertEqual(new.a, 'a')
        self.assertEqual(new.b, 'b')
        self.assertNotIn('b', a)
        self.assertNotIn('a', b)

    def test_opt_ior(self):
        a = IndexableObject(dict(a='a'))
        b = IndexableObject(dict(b='b'))

        a |= b
        self.assertEqual(a.a, 'a')
        self.assertEqual(a.b, 'b')
        self.assertNotIn('a', b)

    def test_update(self):
        a = IndexableObject(dict(a='a'))
        b = dict(b='b')

        new = update(a, b)
        self.assertEqual(a.a, 'a')
        self.assertEqual(a.b, 'b')
        self.assertEqual(new, a)
        self.assertNotIn('a', b)