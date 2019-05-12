#####
# Does all the global stuff
#####
import game.view as view
import sys
from population.individual import CleverBot, from_list

COEFF_SIZES = [25, 10, 4]

if __name__ == '__main__':
    filename = sys.argv[1]
    f = open(filename, "r")
    l = f.readlines()
    line = l[0]
    c = CleverBot(COEFF_SIZES, position=[600, 600], direction=-135)
    c.brain = from_list(COEFF_SIZES, [float(x) for x in line.split(":")[1].split(",")])
    view.run(c)
