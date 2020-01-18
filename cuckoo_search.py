from TaskPackage.cuckoo_search.data import inputMatrix
from random import uniform
from random import randint
import math

distanceMatrix = inputMatrix


def levy_flight(u):
    return math.pow(u, -1.0 / 3.0)


def calcultate_distance(path):
    index = path[0]
    distance = 0
    for nextIndex in path[1:]:
        distance += distanceMatrix[index][nextIndex]
        index = nextIndex
    return distance + distanceMatrix[path[-1]][path[0]]


def swap(sequence, i, j):
    sequence[i], sequence[j] = sequence[j], sequence[i]


def twoOptMove(nest, a, c):
    nest = nest[0][:]
    swap(nest, a, c)
    return nest, calcultate_distance(nest)


def doubleBridgeMove(nest, a, b, c, d):
    nest = nest[0][:]
    swap(nest, a, b)
    swap(nest, c, d)
    return nest, calcultate_distance(nest)


if __name__ == '__main__':
    numNests = 10
    pa = int(0.2 * numNests)
    pc = int(0.6 * numNests)
    maxGen = 50
    n = len(inputMatrix)
    nests = []

    initPath = list(range(0, n))
    index = 0
    for i in range(numNests):
        if index == n - 1:
            index = 0
        swap(initPath, index, index + 1)
        index += 1
        nests.append((initPath[:], calcultate_distance(initPath)))

    nests.sort(key=lambda tup: tup[1])

    for t in range(maxGen):
        cuckooNest = nests[randint(0, pc)]
        if levy_flight(uniform(0.0001, 0.9999)) > 2:
            cuckooNest = doubleBridgeMove(
                cuckooNest, randint(0, n - 1), randint(0, n - 1),
                randint(0, n - 1), randint(0, n - 1)
            )
        else:
            cuckooNest = twoOptMove(cuckooNest, randint(0, n - 1), randint(0, n - 1))
        randomNestIndex = randint(0, numNests - 1)
        if nests[randomNestIndex][1] > cuckooNest[1]:
            nests[randomNestIndex] = cuckooNest
        for i in range(numNests - pa, numNests):
            nests[i] = twoOptMove(nests[i], randint(0, n - 1), randint(0, n - 1))
        nests.sort(key=lambda tup: tup[1])
        # for nest in nests:
        #     print(nest[1], end=' ')
        # print()
    print(f"CUCKOO's SOLUTION:\t{nests[0]}")
