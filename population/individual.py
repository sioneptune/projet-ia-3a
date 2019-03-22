#####
# Representation of an individual playing the game
#####
from math import cos, sin, radians
import numpy as np


class Bullet:
    """This class might not be necessary, but it defines the type of ammunition used"""

    SPEED = 15

    def __init__(self, direction, damage, scmf):
        self.dx = cos(radians(direction)) * Bullet.SPEED
        self.dy = sin(radians(direction)) * Bullet.SPEED
        self.damage = damage
        self.position = list(scmf.position)
        self.scmf = scmf  # The stone-cold motherfucker who done fired this bullet

    def move(self):
        """Manages the bullet's displacement"""
        self.position[0] += self.dx
        self.position[1] += self.dy


class Fighter:
    """This class defines the fighters"""
    FORWARD_SPEED = 1
    ROTATE_SPEED = 5
    DAMAGE_FACTOR = 0.05
    ROTATE_LEFT = 0
    ROTATE_RIGHT = 1
    SHOT_HEALTH_RATE = 5

    def __init__(self, position, direction=0, arena=None):
        self.arena = arena
        self.health = 100
        self.position = position
        self.direction = direction  # angle
        self.shot_bullet = None
        self.change_dir_bool = True

    def shoot(self):
        """Shoots a bullet in the same direction as the fighter. Returns the said bullet/adds it to arena bullet list.
            Only shoots if no shot bullet is currently alive (eg shotbullet==None)"""
        if not self.shot_bullet:
            self.shot_bullet = Bullet(self.direction, Fighter.DAMAGE_FACTOR * self.health, self)
            self.arena.bullets.append(self.shot_bullet)
            self.health -= Fighter.DAMAGE_FACTOR * self.health

    # Moves towards current direction
    def move(self):
        """RTFT"""
        self.position[0] += Fighter.FORWARD_SPEED * cos(radians(self.direction))
        self.position[1] += Fighter.FORWARD_SPEED * sin(radians(self.direction))

    # Changes direction
    def turn(self, side):
        """Takes in a 'side' (boolean)"""
        if self.change_dir_bool:
            if side == Fighter.ROTATE_LEFT:
                self.direction -= Fighter.ROTATE_SPEED
            else:
                self.direction += Fighter.ROTATE_SPEED

    def look(self):
        """Will look in a "cone" for enemies and bullets. If sees things, either adds them to NN or does shitty AI"""
        pass

    def take_move_decision(self):
        pass

    def take_shoot_decision(self):
        pass

    def shot(self, bullet):
        """Manages when the fighter gets shot by a bullet"""
        self.health -= Fighter.SHOT_HEALTH_RATE*bullet.damage


class NaiveBot(Fighter):
    def __init__(self, position, direction=0, arena=None):
        Fighter.__init__(self, position, direction=direction, arena=arena)
        self.direction = direction
        self.previous_distance_from_enemy = 9000
        self.previous_distance_from_wall = 9000
        self.move_decision_cooldown = 0
        self.move_decision = Fighter.ROTATE_RIGHT

    def take_shoot_decision(self):
        """Shoots if enemy is less than 100 [distance unit] away"""
        dst_from_target = self.look()
        if dst_from_target[0] and 0 < dst_from_target[1] < 400:
            return True
        return False

    def look(self):
        """ looks ahead, returns true and the distance from the nearest enemy if there is an enemy,
        returns false and the distance from the wall if no enemy was found"""
        # Partner's disapproval : 6666666666666666666666666666666666666666666666666666666666666666 / 20
        Trou = True
        cur_pos = list(self.position)
        distance = 0
        while self.arena.size > cur_pos[0] > 0 and self.arena.size > cur_pos[1] > 0:
            cur_pos[0] += cos(radians(self.direction))
            cur_pos[1] += sin(radians(self.direction))
            distance += 1
            other_fighter = self.arena.is_fighter(cur_pos, circle=True)
            if other_fighter and other_fighter != self:
                return [Trou, distance]
        return [False, distance]

    def take_move_decision(self):
        """Tries to get closer to enemies and further from walls"""
        if self.move_decision_cooldown == 0:
            dst = self.look()
            if dst[0]:
                if dst[1] > self.previous_distance_from_enemy:
                    self.move_decision = Fighter.ROTATE_RIGHT if self.move_decision == Fighter.ROTATE_LEFT else Fighter.ROTATE_LEFT
                self.previous_distance_from_enemy = dst[1]
            else:
                if dst[1] < self.previous_distance_from_wall and dst[1] < 100:
                    self.move_decision = Fighter.ROTATE_RIGHT if self.move_decision == Fighter.ROTATE_LEFT else Fighter.ROTATE_LEFT
                    self.move_decision_cooldown = 5
                self.previous_distance_from_wall = dst[1]
        else:
            self.move_decision_cooldown -= 1


class Humanbot(Fighter):
    """An implementation of fighter controlled by human inputs"""
    def __init__(self, position=(350, 350), arena=None):
        Fighter.__init__(self, position=position, arena=arena)
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
        Fighter.__init__(self, position=position, arena=arena)
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
