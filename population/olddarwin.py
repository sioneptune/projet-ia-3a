#####
# Manages the lifecycle of a generation
#####
import numpy as np

GEN_SIZE = 25


def makemean(vectorlist):
    """Takes in a list of vectors and outputs their mean"""
    size = len(vectorlist)
    mean = np.array([0]*len(vectorlist[0]))
    for v in vectorlist:
        mean = np.add(mean, (1/size)*v)
    return mean


def makecv(vectorlist):
    """returns the covariance matrix of a list of vectors"""
    m = np.array(vectorlist).T
    return np.cov(m)


def randomMV(mean, cov):
    return np.random.multivariate_normal(mean=mean, cov=cov, size=GEN_SIZE)


def renewPop(generation):
    """Takes in a generation, in the form of an array of arrays [score, [coeffs]]"""
    generation.sort(key=lambda elem: elem[0])
    oldgen = [x[1] for x in generation]
    oldmean = makemean(oldgen)
    oldcv = makecv(oldgen)
    winners = generation[int(len(generation)/2):]
    newmean = makemean(winners)




"""
vl = [np.array([1,2,3]), np.array([5,6,7]), np.array([9,10,11]), np.array([0.5,1,2]), np.array([9,15,16])]
print(makemean(vl))
print(makecv(vl))

vl = [np.array([1, 1, 1]), np.array([3, 3, 2])]

print(makemean(vl))

a = np.matrix([[2, -1, 0], [-1, 2, -1], [0, -1, 2]])
print(a)
l = np.linalg.cholesky(a)
print(l)
aprime = np.matmul(l, l.transpose())
print(aprime)

v = np.array([1,2,3,4])
print(v)
print(v[2])
"""
