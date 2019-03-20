#####
# File containing the game infrastructure
#####
from math import cos, sin, pow, radians


class Arena:
    """This class defines the arena where things will fight"""
    MAX_FIGHTERS = 4
    FIGHTER_RADIUS_HEALTH_RATE = 4
    UP_SIDE = 0
    RIGHT_SIDE = 1
    DOWN_SIDE = 2
    LEFT_SIDE = 3

    def __init__(self):
        self.size = 700
        self.fighters = []
        self.bullets = []

    def is_fighter(self, pos, offset=0, circle=False):
        if circle:
            for fighter in self.fighters:
                a = pow(pos[0] - fighter.position[0], 2)
                b = pow(pos[1] - fighter.position[1], 2)
                c = pow(fighter.health/4, 2)
                if a + b < c:
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
        if bullet.damage * Fighter.SHOT_HEALTH_RATE >= fighter.health:
            print("a fighter should be down")
            self.fighter_down(fighter, bullet.scmf, fighter.health)
        else:
            fighter.shot(bullet)
        bullet.scmf.shot_bullet = None
        self.bullets.remove(bullet)
        del bullet

    def fighter_down(self, fighter, killer, health):
        """Manages a death. Removes fighter from list, gives health to the killer (fighter obj)"""
        killer.health += health
        fighter.health = 0
        self.fighters.remove(fighter)
        del fighter

    def run(self):
        """Queries the fighters for their action, makes movements for 1 frame"""
        for fighter in self.fighters:
            if fighter.take_shoot_decision():
                fighter.shoot()
            fighter.move()
            # Manages cases where the fighter is out of the arena
            self.fighter_out_of_arena(fighter)
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

    def fighter_out_of_arena(self, fighter):
        """ Checks if the fighter is out of arena, calls replace_fighter_in_arena if so"""
        if fighter.position[0] + fighter.health/4 >= self.size:
            self.replace_fighter_in_arena(fighter, Arena.RIGHT_SIDE)
        if fighter.position[0] - fighter.health/4 <= 0:
            self.replace_fighter_in_arena(fighter, Arena.LEFT_SIDE)
        if fighter.position[1] + fighter.health/4 >= self.size:
            self.replace_fighter_in_arena(fighter, Arena.DOWN_SIDE)
        if fighter.position[1] - fighter.health/4 <= 0:
            self.replace_fighter_in_arena(fighter, Arena.UP_SIDE)

    def replace_fighter_in_arena(self, fighter, side):
        """ Replaces the given fighter in the arena (against a wall) """
        if side == Arena.RIGHT_SIDE:
            fighter.position[0] += self.size - (fighter.position[0] + fighter.health/4)
        if side == Arena.LEFT_SIDE:
            fighter.position[0] += 0 - (fighter.position[0] - fighter.health/4)
        if side == Arena.DOWN_SIDE:
            fighter.position[1] += self.size - (fighter.position[1] + fighter.health / 4)
        if side == Arena.UP_SIDE:
            fighter.position[1] += 0 - (fighter.position[1] - fighter.health/4)


class Fighter:
    """This class defines the fighters"""
    FORWARD_SPEED = 5
    ROTATE_SPEED = 5
    DAMAGE_FACTOR = 0.05
    ROTATE_LEFT = 0
    ROTATE_RIGHT = 1
    SHOT_HEALTH_RATE = 5

    def __init__(self, position, arena=None):
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
