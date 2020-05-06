import math
import random
import numpy as np
import matplotlib.pyplot as plt
import pytest
from sepratePlot import *


def run_simulation(animals, res, n):
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
            animal_survives = random.random() <= prob # find out if animal survives (random)
            if animal_survives:
                value += a.value_constant # add animal's value to total value
    return value/n


def test_correctness():
    """
    compares result from algorithm to an optimal solution
    """
    fish = Animal('fish', [0.2, 5, 0.9] , 8)
    penguin = Animal('penguin', [0.4, 20, 0.1] , 3)
    seal = Animal('seal', [0.4, 20, 0.1] , 2)
    list = [fish, penguin, seal]
    # penguin and seal are same except for value, so penguin should get more
    # fish is almost guarenteed to survive without anything, so it should
    # not get any money unless there is a lot of money
    res, names = resource_allocation(list, 3)
    # plot_results(res, names)
    assert res == [0, 2, 1], "Antarctic test failed"
    # fish gets 0, penguin gets 2, seal gets 1

def iterate(animal_list):
    x_vals = [] # resources
    y_vals = [] # resultant simulated values

    for i in range(1, 500, 10):
        for animal in animal_list:
            animal.resources = 0
        x = i
        x_vals.append(x)
        result = resource_allocation(animal_list, x)[0]
        y = run_simulation(animal_list, result, 100)
        y_vals.append(y)

    plt.scatter(x_vals, y_vals)
    plt.xlabel("Number of Resources Allocated")
    plt.ylabel("Total Simulated System Value")
    plt.title("Resources Allocated vs Total System Value")
    plt.show()

# Arbitrary animals
cow = Animal ('cow', [0.5, 20, 0.5], 8)
cat = Animal ('cat', [0.1, 10, 0.7], 5)
mouse = Animal ('mouse', [0.3, 20, 0.4], 7)
elephant = Animal ('elephant', [0.5, 30, 0.1], 4)
horse = Animal('horse', [1, 20, 0.3], 2)
beardedDragon = Animal('bDragon', [0.5, 10, 0.4], 2)

testList = [cow, cat, mouse, elephant, horse, beardedDragon]


if __name__ == "__main__":
    res = resource_allocation(testList, 50)[0]
    print(res)
    print("Simulated value: ", run_simulation(testList, res, 100))
    test_correctness()
    iterate(testList)
