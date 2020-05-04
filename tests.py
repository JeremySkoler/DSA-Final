import math
import random
import numpy as np
import matplotlib.pyplot as plt
from discreteNoahWithBiodiversity import *


def test_optimality(animals, res, n):
    """ does several random simulations of which animals live and die
    animals = list of animals objects
    res = result list of money allocated
    n = number of random iterations
    """
    value = 0
    for i in range(len(animals)):
        a = animals[i]
        prob = a.get_survival_rate(res[i]) # find probability each animal will survive
        # print(prob)
        for j in range(n):
            animal_survives = random.random() <= prob # find out if animal survivies (random)
            if animal_survives:
                value += a.value_constant # add animal's value to total value
    return value/n

# Arbitrary animals
cow = Animal ('cow', [0.5, 20, 0.5], 8)
cat = Animal ('cat', [0.1, 10, 0.7], 5)
mouse = Animal ('mouse', [0.3, 20, 0.4], 7)
elephant = Animal ('elephant', [0.5, 30, 0.1], 4)
horse = Animal('horse', [1, 20, 0.3], 2)
beardedDragon = Animal('bDragon', [0.5, 10, 0.4], 2)

testList = [cow, cat, mouse, elephant, horse, beardedDragon]

## Animals start thriving when the # of total resources is a factor
## of 10 bigger than the animals' approximate survival_params[1]

resource_allocation(testList,100)
