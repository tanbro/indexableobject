import unittest

from indexableobject import *


class ToDictTestCase(unittest.TestCase):

    def test_simple(self):
        d0 = {'foo': 'bar'}
        x = from_dict(d0)

        d1 = to_dict(x)

        self.assertDictEqual(d0, d1)

    def test_list(self):
        d0 = [{'foo': 'bar1'}, {'foo': 'bar2'}, {'foo': 'bar3'}, {'foo': 'bar4'}]
        x = from_dict(d0)

        d1 = to_dict(x)

        for i, m in enumerate(d0):
            self.assertDictEqual(m, d1[i])
