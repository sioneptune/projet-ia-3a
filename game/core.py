#####
# File containing the game infrastructure
#####
from math import pow
from population.individual import *
import numpy as np


class Arena:
    """This class defines the arena where things will fight"""
    MAX_FIGHTERS = 4
    FIGHTER_RADIUS_HEALTH_RATE = 4
    UP_SIDE = 0
    RIGHT_SIDE = 1
    DOWN_SIDE = 2
    LEFT_SIDE = 3

    KILL_SCORE = 50

    def __init__(self):
        self.size = 700
        self.fighters = []
        self.bullets = []

    def is_fighter(self, pos, offset=0, circle=False):
        if circle:
            for fighter in self.fighters:
                a = pow(pos[0] - fighter.position[0], 2)
                b = pow(pos[1] - fighter.position[1], 2)
                c = pow(fighter.size/4, 2)
                if a + b < c:
                    return fighter
            return None

        for fighter in self.fighters:
            cond_up_left = pos[0] + offset >= fighter.position[0] - fighter.size and pos[1] + offset >= fighter.position[1] - fighter.size
            cond_down_left = pos[0] + offset >= fighter.position[0] - fighter.size and pos[1] - offset <= fighter.position[1] + fighter.size
            cond_up_right = pos[0] - offset <= fighter.position[0] + fighter.size and pos[1] + offset >= fighter.position[1] - fighter.size
            cond_down_right = pos[0] - offset <= fighter.position[0] + fighter.size and pos[1] - offset <= fighter.position[1] + fighter.size
            if cond_down_left or cond_up_left or cond_up_right or cond_down_right:
                return fighter
        return None

    def populate(self, fighter_list=None):
        """Generates the fighters, places fighters from list, then adds more until reaches MAX_FIGHTERS"""
        if fighter_list:
            self.fighters = [fighter for fighter in fighter_list]
        positions_at_angles = [(100, 100), (600, 100), (600, 600), (100, 600)]
        for i in range(len(self.fighters), Arena.MAX_FIGHTERS):
            for position in positions_at_angles:
                if not self.is_fighter(position, offset=100):
                    self.fighters.append(NaiveBot(position=position, arena=self))

    def add_fighter(self, fighter):
        if not self.is_fighter(fighter.position, offset=100) and len(self.fighters) < Arena.MAX_FIGHTERS:
            fighter.arena = self
            self.fighters.append(fighter)

    def fighter_hit(self, fighter, bullet)   :
        """Manages when a bullet hits the fighter. Removes health, and if h<0, calls fighter_down"""
        if bullet.damage * Fighter.SHOT_HEALTH_RATE >= fighter.health:
            # print("a fighter should be down")
            self.fighter_down(fighter, bullet.scmf)
        else:
            fighter.shot(bullet)
            bullet.scmf.health += 2*bullet.damage
        bullet.scmf.shot_bullet = None
        self.bullets.remove(bullet)
        del bullet

    def fighter_down(self, fighter, killer):
        """Manages a death. Removes fighter from list, gives health to the killer (fighter obj)"""
        killer.heal(Arena.KILL_SCORE)
        fighter.health = 0
        self.fighters.remove(fighter)
        # print(self.fighters)
        del fighter

    def run(self):
        """Queries the fighters for their action, makes movements for 1 frame"""
        for fighter in self.fighters:
            if fighter.take_shoot_decision():
                fighter.shoot()
            if isinstance(fighter, NaiveBot):
                fighter.take_move_decision()
                fighter.turn(fighter.move_decision)
            if isinstance(fighter, CleverBot):
                fighter.take_decisions(fighter.look()+[1/fighter.health])
                fighter.take_move_decision()
                fighter.turn(fighter.move_decision)
                fighter.take_shoot_decision()
                fighter.take_dash_decision()
            fighter.move()
            # Manages cases where the fighter is out of the arena
            self.fighter_out_of_arena(fighter)
            # Manages fighter collision
            self.fighter_collision()
        for bullet in self.bullets:
            bullet.move()
            if not (self.size >= bullet.position[0] >= 0 and self.size >= bullet.position[1] >= 0):
                self.bullets.remove(bullet)
                bullet.scmf.shot_bullet = None
                del bullet
            else:
                fighter = self.is_fighter(bullet.position, circle=True)
                if fighter:
                    if fighter != bullet.scmf:
                        self.fighter_hit(fighter, bullet)
                        bullet.scmf.successful_hits += 1

    def fighter_out_of_arena(self, fighter):
        """ Checks if the fighter is out of arena, calls replace_fighter_in_arena if so"""
        if fighter.position[0] + fighter.size/4 >= self.size:
            self.replace_fighter_in_arena(fighter, Arena.RIGHT_SIDE)
        if fighter.position[0] - fighter.size/4 <= 0:
            self.replace_fighter_in_arena(fighter, Arena.LEFT_SIDE)
        if fighter.position[1] + fighter.size/4 >= self.size:
            self.replace_fighter_in_arena(fighter, Arena.DOWN_SIDE)
        if fighter.position[1] - fighter.size/4 <= 0:
            self.replace_fighter_in_arena(fighter, Arena.UP_SIDE)

    def replace_fighter_in_arena(self, fighter, side):
        """ Replaces the given fighter in the arena (against a wall) """
        if side == Arena.RIGHT_SIDE:
            fighter.position[0] += self.size - (fighter.position[0] + fighter.size/4)
        if side == Arena.LEFT_SIDE:
            fighter.position[0] += 0 - (fighter.position[0] - fighter.size/4)
        if side == Arena.DOWN_SIDE:
            fighter.position[1] += self.size - (fighter.position[1] + fighter.size / 4)
        if side == Arena.UP_SIDE:
            fighter.position[1] += 0 - (fighter.position[1] - fighter.size/4)

    def fighter_collision(self):
        """ Manages collision between fighters """
        for fighter1 in self.fighters:
            for fighter2 in self.fighters:
                if fighter1 != fighter2:
                    pos1 = np.array(fighter1.position)
                    pos2 = np.array(fighter2.position)

                    dist_center = sqrt(np.dot(pos1-pos2, pos1-pos2))
                    dist_side = fighter2.size/4 + fighter1.size/4  # Side to side distance

                    if dist_center < dist_side:
                        moving_distance = (dist_side-dist_center)/2
                        orientation = (fighter1.position[0] - fighter2.position[0], fighter1.position[1] - fighter2.position[1])
                        norm = sqrt(pow(orientation[0], 2) + pow(orientation[1], 2))
                        orientation = (orientation[0]/norm, orientation[1]/norm)
                        # Gotta move fighter2 of dist_side-dist_center/2 following the orientation. Same for fighter1 but in the opposite direction
                        fighter2.position[0] -= orientation[0] * moving_distance
                        fighter2.position[1] -= orientation[1] * moving_distance
                        fighter1.position[0] += (orientation[0] * moving_distance)
                        fighter1.position[1] += (orientation[1] * moving_distance)
