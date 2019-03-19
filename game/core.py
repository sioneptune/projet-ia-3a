#####
# File containing the game infrastructure
#####
from math import cos, sin, radians


class Arena:
    """This class defines the arena where things will fight"""
    MAX_FIGHTERS = 4

    def __init__(self):
        self.size = 700
        self.fighters = []
        self.bullets = []

    def populate(self, fighterlist=None):
        """Generates the fighters, places fighters from list, then adds more until reaches MAX_FIGHTERS"""
        # TODO
        pass

    def add_fighter(self, fighter):
        # TODO
        pass

    def fighter_hit(self, fighter, bullet):
        """Manages when a bullet hits the fighter. Removes health, and if h<0, calls fighter_down"""
        # TODO
        pass

    def fighter_down(self, fighter, killer):
        """Manages a death. Removes fighter from list, gives health to the killer (fighter obj)"""
        # TODO
        pass

    def run(self):
        """Queries the fighters for their action, makes movements for 1 frame"""


class Fighter:
    """This class defines the fighters"""
    FORWARD_SPEED = 5
    ROTATE_SPEED = 0.1
    DAMAGE_FACTOR = 0.05
    ROTATE_LEFT = 0
    ROTATE_RIGHT = 1

    def __init__(self, position=(350.0, 350.0), arena=None):
        self.arena = arena
        self.health = 100
        self.position = position
        self.direction = 0  # angle
        self.shot_bullet = None

    def shoot(self):
        """Shoots a bullet in the same direction as the fighter. Returns the said bullet/adds it to arena bullet list.
            Only shoots if no shot bullet is currently alive (eg shotbullet==None)"""
        b = Bullet((self.position[0], self.position[1]), self.direction, 10, self)
        self.shot_bullet = b
        self.arena.bullets.append(b)

    # Moves towards current direction
    def move(self):
        """RTFT"""
        x = self.position[0] + cos(radians(self.direction))
        y = self.position[1] + sin(radians(self.direction))
        self.position = (x, y)

    # Changes direction
    def turn(self, side):
        """Takes in a 'side' (boolean), true = right"""
        if side:
            self.direction += 5
        else:
            self.direction -= 5

    def look(self):
        """Will look in a "cone" for enemies and bullets. If sees things, either adds them to NN or does shitty AI"""
        # TODO

    def shot(self, bullet):
        """Manages when the fighter gets shot by a bullet"""
        pass


class Bullet:
    """This class might not be necessary, but it defines the type of ammunition used"""

    SPEED = 20

    def __init__(self, position, direction, damage, scmf):
        self.dx = cos(radians(direction)) * Bullet.SPEED
        self.dy = sin(radians(direction)) * Bullet.SPEED
        self.damage = damage
        self.position = position
        self.scmf = scmf  # The stone-cold motherfucker who done fired this bullet

    def move(self):
        """Manages the bullet's displacement"""
        x = self.position[0] + self.dx
        y = self.position[1] + self.dy
        self.position = (x, y)
