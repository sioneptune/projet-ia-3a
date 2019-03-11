#####
# File containing the game infrastructure
#####
from math import cos, sin


class Arena:
    """This class defines the arena where things will fight"""
    MAX_FIGHTERS = 4

    def __init__(self):
        self.size = 700
        self.fighters = []
        self.bullets = []

    def populate(self,fighterlist=[]):
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
    SPEED = 5

    def __init__(self):
        self.arena = None
        self.health = 100
        self.position = (0, 0)
        self.direction = 0      # angle
        self.shot_bullet = None

    def shoot(self):
        """Shoots a bullet in the same direction as the fighter. Returns the said bullet/adds it to arena bullet list.
            Only shoots if no shot bullet is currently alive (eg shotbullet==None)"""
        # TODO
        pass

    # Moves towards current direction
    def move(self):
        """RTFT"""
        # TODO
        pass

    # Changes direction
    def turn(self, side):
        """Takes in a 'side' (boolean)"""
        # TODO
        pass

    def look(self):
        """Will look in a "cone" for enemies and bullets. If sees things, either adds them to NN or does shitty AI"""
        # TODO


class Bullet:
    """This class might not be necessary, but it defines the type of ammunition used"""

    SPEED = 20

    def __init__(self, direction, damage, scmf):
        self.dx = cos(direction)*Bullet.SPEED
        self.dy = sin(direction)*Bullet.SPEED
        self.damage = damage
        self.scmf = scmf # The stone-cold motherfucker who done fired this bullet
