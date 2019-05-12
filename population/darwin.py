import cma
from random import random
from game.core import *
from statistics import mean
from math import pow, sqrt, exp
from os import system
import sys
from multiprocessing import Process, Queue
import random

POPSIZE = 30
COEFF_SIZES = [25, 10, 4]
nb_coeffs = 100


def play_process(individual_list, queue):
    scores = []
    for fighter in individual_list:
        game = Arena()
        fighter.arena = game
        game.populate([fighter, NaiveBot([random.randint(50,650), random.randint(50, 650)], arena=game, direction=random.randint(-180, 180)),
                       NaiveBot([random.randint(50, 650), random.randint(50, 650)], arena=game, direction=random.randint(0, 360)),
                       NaiveBot([random.randint(50, 650), random.randint(50, 650)], arena=game, direction=random.randint(-180, 2*90))])
        time = 0
        while fighter.health > 0 and len(game.fighters) != 1 and time < 50000:
            game.run()
            time += 1
        scores.append(
            [heur([fighter.kills, time / 10000, fighter.hits_taken, fighter.successful_hits, len(game.fighters),
                   fighter.num_of_shots, fighter.health]),
             fighter])
    queue.put(scores)


def heur(item):
    """return the heuristic for an item of the form [kill_nb, time_alive, hits_taken, hits_scored, final_pos]"""
    kill_nb = item[0]
    time_alive = item[1]
    hits_taken = item[2] + (1 if item[6] == 0 else 0)
    hits_scored = item[3]
    final_pos = item[4]
    num_shots = item[5]
    health = item[6]
    alive = item[6] > 0
    a = 0.00011 if num_shots == 0 else 0
    b = 1 if hits_taken == 0 else 0
    heur = pow(hits_scored, 2)/(num_shots + a)
    print(item, heur)
    return 1/abs(heur+0.01)


def gen_init(filename=None):
    """createsNaiveBot a generation loaded from the file. If the file does not exist, creates a random one"""
    pop = []
    if filename:
        open(filename, 'r')
    else:
        for i in range(POPSIZE):
            newitem = []
            for j in range(nb_coeffs):
                newitem.append(random())
            pop.append(newitem)

    return pop


def run_one_gen(gen):
    """runs a generation of fighter"""
    queue1 = Queue()
    queue2 = Queue()
    queue3 = Queue()
    queue4 = Queue()

    list1 = [gen[i] for i in range(0, len(gen) // 4)]
    list2 = [gen[i] for i in range(len(gen) // 4, 2 * len(gen) // 4)]
    list3 = [gen[i] for i in range(2 * len(gen) // 4, 3 * len(gen) // 4)]
    list4 = [gen[i] for i in range(3 * len(gen) // 4, len(gen))]

    process1 = Process(target=play_process, args=(list1, queue1))
    process2 = Process(target=play_process, args=(list2, queue2))
    process3 = Process(target=play_process, args=(list3, queue3))
    process4 = Process(target=play_process, args=(list4, queue4))

    process1.start()
    process2.start()
    process3.start()
    process4.start()

    scores = queue1.get()+queue2.get()+queue3.get()+queue4.get()

    process1.join()
    process2.join()
    process3.join()
    process4.join()

    return scores


def makelog(genscores, gennum):
    gennum = str(gennum)
    gennum = "0"*(3-len(gennum)) + gennum
    file = open(f"gen_{gennum}.log", "w+")
    genscores = sorted(genscores, key=lambda x: x[0])
    for score in genscores:
        file.write(str(score[0])+":"+str(score[1].brain.to_list())[1:-1].strip(" ")+"\n")


def run(startnum):
    gennum = startnum
    gen = []

    if gennum != 0:
        f = open(f"gen_{gennum}.log", "r")
        l = f.readlines()
        for line in l:
            c = CleverBot(COEFF_SIZES, position=[350, 350], direction=random.randint(0, 360))
            c.brain = from_list(COEFF_SIZES, [float(x) for x in line.split(":")[1].split(",")])
            gen.append(c)
    else:
        for i in range(POPSIZE):
            gen.append(CleverBot(COEFF_SIZES, position=[100, 600]))

    es = cma.CMAEvolutionStrategy([0]*len(gen[0].brain.to_list()), 10)

    while True:
        gen = []
        newpop = es.ask(number=POPSIZE)
        for l in newpop:
            c = CleverBot(COEFF_SIZES, position=[350, 350], direction=random.randint(0, 360))
            c.brain = from_list(COEFF_SIZES, l)
            gen.append(c)
        gennum += 1
        scores = run_one_gen(gen)
        makelog(scores, gennum)
        poplist = [c.brain.to_list() for c in gen]
        scorelist = [x[0] for x in scores]
        es.tell(poplist, scorelist)
        print(f"Ran generation {gennum}")



def makemean(l):
    return list(map(mean, zip(*l)))

if __name__ == '__main__':

    run(0)
    #gen = [CleverBot(COEFF_SIZES, position=[100, 600]) for i in POPSIZE]
    #es = cma.CMAEvolutionStrategy(gen[0].brain.to_list(), 0.5)
    #scores = run_one_gen(gen)
    #print(scores)
    #makelog(scores,1)


    #es = cma.CMAEvolutionStrategy(8 * [0], 0.5)
    #while not es.stop():
    #    solutions = es.ask()
    #    es.tell(solutions, [cma.ff.rosen(x) for x in solutions])
    #    es.logger.add()
    #    es.disp()
#
    #es.result_pretty()
    #cma.plot()
