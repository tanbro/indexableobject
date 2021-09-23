import unittest

from indexableobject import *


class CascadeTestCase(unittest.TestCase):

    def test_two_levels_dict(self):
        d = {
            'baz': {
                'baz1': object(),
                'baz2': object(),
            }
        }
        ac = from_dict(d)

        self.assertTrue(hasattr(ac, 'baz'))
        self.assertEqual(ac.baz.baz1, d['baz']['baz1'])
        self.assertEqual(ac.baz.baz2, d['baz']['baz2'])

    def test_dict_in_list(self):
        d = {
            'bar': [
                {'baz': 'baz 1'},
                {'baz': 'baz 2'},
            ]
        }
        ac = from_dict(d)

        self.assertIsInstance(ac.bar, list)

        self.assertEqual(ac.bar[0].baz, d['bar'][0]['baz'])
        self.assertEqual(ac['bar'][0]['baz'], d['bar'][0]['baz'])
        self.assertEqual(ac.bar[1].baz, d['bar'][1]['baz'])
        self.assertEqual(ac['bar'][0]['baz'], d['bar'][0]['baz'])

    def test_top_list(self):
        d = [
            {'baz': 'baz 1'},
            {'baz': 'baz 2'},
        ]
        x = from_dict(d)

        self.assertIsInstance(x, list)

        self.assertEqual(x[0].baz, d[0]['baz'])
        self.assertEqual(x[1].baz, d[1]['baz'])

    def test_2levels_list(self):
        d = [
            [
                {'boo': 'boo 1'},
                {'boo': 'boo 2'},

            ],
            [
                {'foo': 'foo 1'},
                {'foo': 'foo 2'},
            ]
        ]

        x = from_dict(d)

        self.assertIsInstance(x, list)

        boos = x[0]
        self.assertIsInstance(boos, list)
        for i, c in enumerate(boos):
            self.assertEqual(c.boo, d[0][i]['boo'])

        foos = x[1]
        self.assertIsInstance(foos, list)
        for i, c in enumerate(foos):
            self.assertEqual(c.foo, d[1][i]['foo'])
