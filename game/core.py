#####
# File containing the game infrastructure
#####


class Arena:
    """This class defines the arena where things will fight"""


class Fighter:
    """This class defines the fighters"""
    def __init__(self):
        self.health = 100
        self.position = (0, 0)
        self.direction = (0, 1)

    # Shoots a bullet in the given direction. Returns the said bullet
    def shoot(self, direction):
        # TODO
        pass

    # Moves towards current direction
    def move(self):
        # TODO
        pass

    # Changes direction
    def turn(self, direction):
        # TODO
        pass


class Bullet:
    """This class might not be necessary, but it defines the type of ammunition used"""
    def __init__(self, direction, damage):
        self.direction = direction
        self.damage = damage
