#####
# Representation of an individual playing the game
#####
from math import cos, sin, tan, atan, sqrt, radians, degrees
import numpy as np


class Bullet:
    """This class might not be necessary, but it defines the type of ammunition used"""

    SPEED = 20
    MIN_DAMAGE = 5

    def __init__(self, direction, damage, scmf):
        self.dx = cos(radians(direction)) * Bullet.SPEED
        self.dy = sin(radians(direction)) * Bullet.SPEED
        self.damage = damage if damage > Bullet.MIN_DAMAGE else Bullet.MIN_DAMAGE
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
    MIN_HEALTH = 20
    MIN_SIZE = 20
    DASH_COOLDOWN = 20
    DASH_POWER = 50

    def __init__(self, position, direction=0, arena=None):
        self.arena = arena
        self.health = 100
        self.size = 100
        self.position = position
        self.direction = direction  # angle
        self.shot_bullet = None
        self.change_dir_bool = True
        self.kills = 0
        self.dash_cooldown = 0

    def shoot(self):
        """Shoots a bullet in the same direction as the fighter. Returns the said bullet/adds it to arena bullet list.
            Only shoots if no shot bullet is currently alive (eg shotbullet==None)"""
        if not self.shot_bullet and self.health > Fighter.MIN_HEALTH:
            self.shot_bullet = Bullet(self.direction, Fighter.DAMAGE_FACTOR * self.health, self)
            self.arena.bullets.append(self.shot_bullet)
            self.health -= Fighter.DAMAGE_FACTOR * self.health
            self.size = self.health if self.health > Fighter.MIN_SIZE else Fighter.MIN_SIZE

    def heal(self, health):
        self.health += health
        self.size = self.health if self.health > Fighter.MIN_SIZE else Fighter.MIN_SIZE

    def remove_health_manually(self, amount):
        self.health -= amount
        self.size = self.health if self.health > Fighter.MIN_SIZE else Fighter.MIN_SIZE

    # Moves towards current direction
    def move(self):
        """RTFT"""
        self.position[0] += Fighter.FORWARD_SPEED * cos(radians(self.direction))
        self.position[1] += Fighter.FORWARD_SPEED * sin(radians(self.direction))
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

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
        self.size = self.health if self.health > Fighter.MIN_SIZE else Fighter.MIN_SIZE

    def dash(self):
        if self.dash_cooldown == 0:
            self.position[0] += Fighter.FORWARD_SPEED * cos(radians(self.direction)) * Fighter.DASH_POWER
            self.position[1] += Fighter.FORWARD_SPEED * sin(radians(self.direction)) * Fighter.DASH_POWER
            self.dash_cooldown = Fighter.DASH_COOLDOWN


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
        if dst_from_target[0] and 0 < dst_from_target[1] < 600:
            return True
        return False

    def look(self):
        """ looks ahead, returns true and the distance from the nearest enemy if there is an enemy,
        returns false and the distance from the wall if no enemy was found"""
        # Partner's disapproval : 66666666666666666666666666666666size66666666666666666666666666666666 / 20
        Trou = True
        for fighter in self.arena.fighters:
            if fighter != self:
                try:
                    link_angle = (degrees(atan((fighter.position[1] - self.position[1]) / (fighter.position[0] - self.position[0]))) + 360) % 180
                except ZeroDivisionError:
                    link_angle = 90 if fighter.position[0] > self.position[0] else -90
                dist = distance(self.position, fighter.position)
                margin = degrees(atan(0.5 * fighter.size / dist))
                angle = self.direction % 360
                dir_vect = [cos(radians(self.direction)), sin(radians(self.direction))]
                vect_fighters = [fighter.position[0] - self.position[0], fighter.position[1] - self.position[1]]
                if abs(angle - link_angle) < abs(margin) and (np.dot(dir_vect, vect_fighters)) > 0:
                    return [Trou, dist]
        # Compute the line equation
        slope = tan(radians(self.direction))
        y_intercept = self.position[1] - slope*self.position[0]
        if abs(self.direction) < 90:
            x_lim = self.arena.size
        else:
            x_lim = 0
        ordinate = slope * x_lim + y_intercept
        if 0 <= ordinate <= self.arena.size:
            """Si on intercepte les murs verticaux, on regarde à quelle ordonnée on croise"""
            dist = distance(self.position, (self.arena.size, ordinate))
            return [False, dist]
        else:
            """Sinon ça veut dire qu'on coupe les murs horizontaux, on va donc calculer à quelle abscisse"""
            if self.direction < 0:
                """ The upper wall"""
                ordinate = self.arena.size
            else:
                ordinate = 0
            absciss = (ordinate - y_intercept)/slope
            return [False, distance(self.position, (absciss, ordinate))]

    def take_move_decision(self):
        """Tries to get closer to enemies and further from walls"""
        if self.move_decision_cooldown == 0:
            dst = self.look()
            if dst[0]:
                if dst[1] > self.previous_distance_from_enemy:
                    self.move_decision = Fighter.ROTATE_RIGHT if self.move_decision == Fighter.ROTATE_LEFT else Fighter.ROTATE_LEFT
                self.previous_distance_from_enemy = dst[1]
            else:
                if dst[1] < self.previous_distance_from_wall and dst[1] < 200:
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
    def __init__(self, sizes, position=(350, 350), direction=0, arena=None):
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
    """ Codes a really basic neural network with numpy
    - Inputs: probably distance from each obstacle in 4 directions (obstacle being wall and  enemy)
    - Outputs: [turn_left, turn_right, dash, shoot]"""
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
        dash = result[3]
        decisions = [0, 0, 0]
        if move_left >= 0.5 or move_right >= 0.5:
                decisions[0] = -1 if move_left > move_right else 1
        decisions[1] = 1 if shoot >= 0.5 else 0
        decisions[2] = dash if dash > 0.5 else 0
        return decisions


def sigmoid(z):
    """RTFT"""
    return 1.0/(1.0+np.exp(-z))


def distance(p1, p2):
    return sqrt(pow(p1[0]-p2[0], 2) + pow(p1[1]-p2[1], 2))
