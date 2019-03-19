#####
# File containing the game infrastructure
#####
from math import cos, sin, pow


class Arena:
    """This class defines the arena where things will fight"""
    MAX_FIGHTERS = 4

    def __init__(self):
        self.size = 700
        self.fighters = []
        self.bullets = []

    def is_fighter(self, pos, offset=0, circle=False):
        # Note du programmeur adjoint: je suis éthiquement opposé à la ligne suivante
        if circle:
            for fighter in self.fighters:
                if pow(pos[0] - fighter.position[0], 2) + pow(pos[1] - fighter.position[1], 2) < pow(fighter.health, 2):
                    return fighter
            return None

        for fighter in self.fighters:
            cond_up_left = pos[0] + offset >= fighter.position[0] - fighter.health and pos[1] + offset >= fighter.position[1] - fighter.health
            cond_down_left = pos[0] + offset >= fighter.position[0] - fighter.health and pos[1] - offset <= fighter.position[1] + fighter.health
            cond_up_right = pos[0] - offset <= fighter.position[0] + fighter.health and pos[1] + offset >= fighter.position[1] - fighter.health
            cond_down_right = pos[0] - offset <= fighter.position[0] + fighter.health and pos[1] - offset <= fighter.position[1] + fighter.health
            if cond_down_left or cond_up_left or cond_up_right or cond_down_right:
                return fighter
        return None

    def populate(self, fighterlist=None):
        """Generates the fighters, places fighters from list, then adds more until reaches MAX_FIGHTERS"""
        self.fighters = [fighter for fighter in fighterlist]
        positions_at_angles = [(100, 100), (600, 100), (600, 600), (100, 600)]
        for i in range(len(self.fighters), Arena.MAX_FIGHTERS):
            for position in positions_at_angles:
                if not self.is_fighter(position, offset=100):
                    self.fighters.append(Fighter(position=position, arena=self))

    def add_fighter(self, fighter):
        if not self.is_fighter(fighter.position, offset=100) and len(self.fighters) < Arena.MAX_FIGHTERS:
            self.fighters.append(fighter)

    def fighter_hit(self, fighter, bullet):
        """Manages when a bullet hits the fighter. Removes health, and if h<0, calls fighter_down"""
        if bullet.damage >= fighter.health:
            self.fighter_down(fighter, bullet.scmf, fighter.health)
        else:
            fighter.shot(bullet)
        bullet.scmf.shot_bullet = None
        self.bullets.remove(bullet)
        del bullet

    def fighter_down(self, fighter, killer, health):
        """Manages a death. Removes fighter from list, gives health to the killer (fighter obj)"""
        killer.health += health
        self.fighters.remove(fighter)
        del fighter

    def run(self):
        """Queries the fighters for their action, makes movements for 1 frame"""
        for fighter in self.fighters:
            if fighter.take_shoot_decision():
                fighter.shoot()
            fighter.take_move_decision()
            fighter.move()
        for bullet in self.bullets:
            bullet.move()
            if not (self.size >= bullet.position[0] >= 0 and self.size >= bullet.position[1] >= 0):
                self.bullets.remove(bullet)
                del bullet
            else:
                fighter = self.is_fighter(bullet.position, circle=True)
                if fighter:
                    self.fighter_hit(fighter, bullet)


class Fighter:
    """This class defines the fighters"""
    FORWARD_SPEED = 5
    ROTATE_SPEED = 0.1
    DAMAGE_FACTOR = 0.05
    ROTATE_LEFT = 0
    ROTATE_RIGHT = 1

    def __init__(self, position=(350, 350), arena=None):
        self.arena = arena
        self.health = 100
        self.position = position
        self.direction = 0  # angle
        self.shot_bullet = None
        self.change_dir_bool = True

    def shoot(self):
        """Shoots a bullet in the same direction as the fighter. Returns the said bullet/adds it to arena bullet list.
            Only shoots if no shot bullet is currently alive (eg shotbullet==None)"""
        if not self.shot_bullet:
            self.shot_bullet = Bullet(self.direction, Fighter.DAMAGE_FACTOR * self.health, self)
            self.arena.bullets.append(self.shot_bullet)

    # Moves towards current direction
    def move(self):
        """RTFT"""
        self.position[0] += Fighter.FORWARD_SPEED * cos(self.direction)
        self.position[1] += Fighter.FORWARD_SPEED * sin(self.direction)

    # Changes direction
    def turn(self, side):
        """Takes in a 'side' (boolean)"""
        if self.change_dir_bool:
            if side == Fighter.ROTATE_LEFT:
                self.direction += Fighter.ROTATE_SPEED
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
        self.health -= bullet.damage


class Bullet:
    """This class might not be necessary, but it defines the type of ammunition used"""

    SPEED = 20

    def __init__(self, direction, damage, scmf):
        self.dx = cos(direction) * Bullet.SPEED
        self.dy = sin(direction) * Bullet.SPEED
        self.damage = damage
        self.position = scmf.position
        self.scmf = scmf  # The stone-cold motherfucker who done fired this bullet

    def move(self):
        """Manages the bullet's displacement"""
        self.position[0] += self.dx
        self.position[1] += self.dy
