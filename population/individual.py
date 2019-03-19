#####
# Representation of an individual playing the game
#####
from game.core import Fighter
from random import randint
from math import cos, sin
import numpy as np


class NaiveBot(Fighter):
    def __init__(self, position=(350, 350), arena=None):
        Fighter.__init__(position, arena)
        self.direction = randint(0, 1)
        self.previous_distance_from_enemy = 9000
        self.previous_distance_from_wall = 9000

    def take_shoot_decision(self):
        """Shoots if enemy is less than 100 [distance unit] away"""
        dst_from_target = self.look()
        if dst_from_target[0] and dst_from_target[1] < 100:
            return True
        return False

    def look(self):
        """ looks ahead, returns true and the distance from the nearest enemy if there is an enemy,
        returns false and the distance from the wall if no enemy was found"""
        # Partner's disapproval : 6666666666666666666666666666666666666666666666666666666666666666 / 20
        Trou = True
        cur_pos = self.position
        distance = 0
        while self.arena.size > cur_pos[0] > 0 and self.arena.size > cur_pos[1] > 0:
            cur_pos[0] += cos(self.direction)
            cur_pos[1] += sin(self.direction)
            distance += 1
            if self.arena.is_fighter(cur_pos, circle=True) != self:
                return [Trou, distance]
        return [False, distance]

    def take_move_decision(self):
        """Tries to get closer to enemies and further from walls"""
        dst = self.look()
        if dst[0] and dst[1] > self.previous_distance_from_enemy:
            self.direction = not self.direction
            self.previous_distance_from_enemy = dst[1]
        elif not dst[0] and dst[1] < self.previous_distance_from_wall:
            self.direction = not self.direction
            self.previous_distance_from_wall = dst[1]


class Humanbot(Fighter):
    """An implementation of fighter controlled by human inputs"""
    def __init__(self, position=(350, 350), arena=None):
        Fighter.__init__(self,position=position, arena=arena)
        self.human = True

    def turn(self, side):
        if side:
            self.direction -= 5
        else:
            self.direction += 5

    def move(self):

        self.position = (self.position[0] + cos(self.direction), self.position[1] + sin(self.direction))


class CleverBot(Fighter):
    def __init__(self, sizes, position=(350, 350), arena=None):
        Fighter.__init__(self,position=position, arena=arena)
        self.brain = NeuralNetwork(sizes)
        # Format: [move, shoot]
        self.decisions = [0, 0]

    def take_decisions(self, inputs):
        """ This function will be changed to use the neural network instead of using parameters"""
        self.decisions = self.brain.take_decision(inputs)

    def take_move_decision(self):
        turn = self.decisions[0]
        if turn == 0:
            self.change_dir_bool = False
        else:
            self.change_dir_bool = True
            self.direction = 0 if turn == -1 else 1

    def take_shoot_decision(self):
        return self.decisions[1]

    def look(self):
        pass

class NeuralNetwork:
    """ Codes a rally basic neural network with numpy"""
    def __init__(self, sizes):
        """ The list sizes contains the number of neuron in each layer, sizes[0] being the input layer and sizes[-1] the output layer"""
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = np.array([np.random.randn(y, 1) for y in self.sizes[1:]])
        self.weights = np.array([np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])])

    def feed_forward(self, inputs):
        """ Returns the output of the neural network at the given input. Returns a list corresponding to the output layer
        output format: [move_left, move_right, shoot]"""
        output = inputs
        for bias, weight in zip(self.biases, self.weights):
            output = sigmoid(np.dot(weight, output) + bias[0])
        return output

    def take_decision(self, inputs):
        """ Returns a tuple: (shoot<bool>, move<-1,0,1>)"""
        result = self.feed_forward(inputs)
        move_left = result[0]
        move_right = result[1]
        shoot = result[2]
        decisions = [0, 0]
        if move_left >= 0.5 or move_right >= 0.5:
                decisions[0] = -1 if move_left > move_right else 1
        decisions[1] = 1 if shoot >= 0.5 else 0
        return decisions

def sigmoid(z):
    """RTFT"""
    return 1.0/(1.0+np.exp(-z))
