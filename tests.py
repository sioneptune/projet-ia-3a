import unittest
import os
from game.core import *
from math import sqrt


class CleverTest(unittest.TestCase):

    def setUp(self):
        global arena
        arena = Arena()
        global clever
        clever = CleverBot([1, 2, 3], position=(350, 350), direction=0, arena=arena)

    def test_look_one_dir(self):
        naive = NaiveBot(position=(600, 200), direction=0)
        arena.add_fighter(naive)
        clever.position = [500, 200]
        results = clever.look_one_direction(0)
        self.assertEqual(results[0], 1/100)
        self.assertEqual(results[1], 1/200)
        results = clever.look_one_direction(90)
        self.assertEqual(results[0], 0)
        self.assertNotEqual(results[1], 0)

    def test_look(self):
        results = clever.look()
        expected = [0, 1/350, 0, 2/(arena.size*sqrt(2)),
                    0, 1/350, 0, 2/(arena.size*sqrt(2)),
                    0, 1/350, 0, 2/(arena.size*sqrt(2)),
                    0, 1/350, 0, 2/(arena.size*sqrt(2))]
        self.assertEqual(len(results), 16)
        for i in range(0, 16):
            self.assertAlmostEqual(results[i], expected[i], delta=0.0005)


if __name__ == '__main__':
    unittest.main()
