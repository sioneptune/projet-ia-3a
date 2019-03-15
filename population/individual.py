#####
# Representation of an individual playing the game
#####

from game.core import Fighter
from math import cos, sin



class Humanbot(Fighter):
    """An implementation of fighter controlled by human inputs"""

    def __init__(self):
        self.human = True

    def turn(self, side):
        if side:
            self.direction -= 5
        else:
            self.direction += 5

    def move(self):

        self.position = (self.position[0] + cos(self.direction), self.position[1] + sin(self.direction))

