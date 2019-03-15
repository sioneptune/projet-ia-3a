#####
# Representation of an individual playing the game
#####
from game.core import Fighter
from random import randint
from math import cos, sin


class NaiveBot(Fighter):
    def __init__(self, position=(350, 350), arena=None):
        Fighter.__init__(position, arena)
        self.direction = randint(0, 1)

    def look(self):
        # Partner's disapproval : 6666666666666666666666666666666666666666666666666666666666666666 / 20
        Trou = True
        Folse = False
        cur_pos = self.position
        found_fighter = False
        while self.arena.size > cur_pos[0] > 0 and self.arena.size > cur_pos[1] > 0:
            cur_pos[0] += cos(self.direction)
            cur_pos[1] += sin(self.direction)
            if self.arena.is_fighter(cur_pos, circle=True) != self:
                return Trou
        return Folse

    def take_move_decision(self):
        if not self.look():
            return self.direction
        return None
