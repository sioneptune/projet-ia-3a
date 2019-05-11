import cma
from random import random
from game.core import *
from statistics import mean
from math import pow
from os import system
from multiprocessing import Process, Queue

POPSIZE = 10
COEFF_SIZES = [25, 10, 4]
nb_coeffs = 100


def play_process(individual_list, queue):
    scores = []
    for fighter in individual_list:
        game = Arena()
        fighter.arena = game
        game.populate([fighter, NaiveBot([600, 100], arena=game, direction=135),
                       NaiveBot([100, 100], arena=game, direction=45), NaiveBot([600, 600], arena=game, direction=225)])
        time = 0
        print("Health:", fighter.health)
        while fighter.health > 0 and len(game.fighters) != 1 and time < 5000:
            game.run()
            time += 1
        scores.append(
            [heur([fighter.kills, time / 10000, fighter.hits_taken, fighter.successful_hits, len(game.fighters),
                   fighter.num_of_shots]),
             fighter])
    queue.put(scores)


def heur(item):
    """return the heuristic for an item of the form [kill_nb, time_alive, hits_taken, hits_scored, final_pos]"""
    kill_nb = item[0]
    time_alive = item[1]
    hits_taken = item[2]
    hits_scored = item[3]
    final_pos = item[4]
    num_shots = item[5]
    print(time_alive, hits_taken, hits_scored)
    res = num_shots/hits_scored - 1 if hits_scored != 0 else 50
    return res


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

    print(scores)
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
            c = CleverBot(COEFF_SIZES, position=[100, 600], direction=-45)
            c.brain = from_list(COEFF_SIZES, [float(x) for x in line.split(":")[1].split(",")])
            gen.append(c)
    else:
        for i in range(POPSIZE):
            gen.append(CleverBot(COEFF_SIZES, position=[100, 600]))

    es = cma.CMAEvolutionStrategy([0]*len(gen[0].brain.to_list()), 0.5)

    while True:
        gen = []
        newpop = es.ask()
        for l in newpop:
            c = CleverBot(COEFF_SIZES, position=[100, 600])
            c.brain = from_list(COEFF_SIZES, l)
            gen.append(c)
        gennum +=1
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
