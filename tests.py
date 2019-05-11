import unittest
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
        naive = NaiveBot(position=(600, 200), direction=0)
        bull = Bullet(0, 5, naive)
        bull.position = [400, 350]
        arena.bullets = [bull]
        results = clever.look()
        expected = [0, 1/350, 1/50, 0, 2/(arena.size*sqrt(2)), 0,
                    0, 1/350, 0, 0, 2/(arena.size*sqrt(2)), 0,
                    0, 1/350, 0, 0, 2/(arena.size*sqrt(2)), 0,
                    0, 1/350, 0, 0, 2/(arena.size*sqrt(2)), 0]
        self.assertEqual(len(results), 24)
        for i in range(0, 24):
            self.assertAlmostEqual(results[i], expected[i], delta=0.0005)


class NeuronTest(unittest.TestCase):

    def test_to_list(self):
        net = NeuralNetwork([3, 2, 3], zero=True)
        liste = net.to_list()
        self.assertEqual(liste, [0, 1, 2, 0, 1, 2, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2])

    def test_from_list(self):
        net = NeuralNetwork([3, 2, 3])
        liste = net.to_list()

        other_net = from_list([3, 2, 3], liste)

        self.assertEqual(net.biases, other_net.biases)
        self.assertEqual(net.weights, other_net.weights)


if __name__ == '__main__':
    unittest.main()
