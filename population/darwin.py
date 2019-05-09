import cma
from random import random
from game.core import *

popsize = 50
nb_coeffs = 100


def heur(item):
    """return the heuristic for an item of the form [kill_nb, time_alive, hits_taken, hits_scored, final_pos, coeffs]"""
    kill_nb = item[0]
    time_alive = item[1]
    hits_taken = item[2]
    hits_scored = item[3]
    final_pos = item[4]
    return (time_alive * final_pos * (hits_scored - hits_taken)) / (1 + final_pos - kill_nb)


def gen_init(filename=None):
    """creates a generation loaded from the file. If the file does not exist, creates a random one"""
    pop = []
    if filename:
        open(filename, 'r')
    else:
        for i in range(popsize):
            newitem = []
            for j in range(nb_coeffs):
                newitem.append(random())
            pop.append(newitem)

    return pop


def do_one_gen(gen, es):
    """runs a generation of fighter, generates the "better" fighters and returns them"""
    game = Arena()
    game.populate([CleverBot()])



if __name__ == '__main__':
    es = cma.CMAEvolutionStrategy(8 * [0], 0.5)
    while not es.stop():
        solutions = es.ask()
        es.tell(solutions, [cma.ff.rosen(x) for x in solutions])
        es.logger.add()
        es.disp()

    es.result_pretty()
    cma.plot()
