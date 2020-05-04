import math
import random
import numpy as np
import matplotlib.pyplot as plt

class Animal:
    ''' Creates an animal'''

    def __init__(self, name, survival_params, value_constant):
        '''
        name (str) = animal name
        weight (int or float) = animal's weight or cost
        value = (int or float) = animal's diversity value
        '''

        self.name = name
        self.survivial_params = survival_params # [0.5 (0-1), 2, 0.2 (starting survival probability, between 0-1)]
        self.value_constant = value_constant
        self.resources = 0

    def get_survival_rate(self, resources):
        # survival_chance = (self.survivial_params[0]*math.sqrt(resources/self.survivial_params[1])+self.survivial_params[2])
        a = self.survivial_params[0]
        b = self.survivial_params[1]
        survival_chance = a/(1+((resources*b)+0.5)**2)+1
        return survival_chance

    def get_value(self, resources):
        survival_chance = self.get_survival_rate(resources)
        if survival_chance >=1:
            survival_chance = 1
        #val = self.value_constant*(1+0.3*survival_chance)
        val = self.value_constant*survival_chance
        return val




def resource_allocation(animalList, resources):
    ''' Find optimal subset of animals to maximize the total value while remaining
     within the resources limit
    Args
    -----------
    animalList (list) = List of animal objects to evaluate
    resources (int or float) = Maximum resources any subset's resourcess can sum to
    Returns
    -----------
    animalsIncluded (list) = List of animal names included in optimal subset
    dp[resources][item] (float) = The maximized value achieved by optimal subset
    '''
    anm_count = len(animalList)
    dp = np.zeros((resources+1, anm_count))          #Matrix to hold subset values

    totalValue = 0
    for animal in animalList:
        totalValue += animal.get_value(0)


    for j in range(anm_count):
        dp[0][j] = totalValue

    where_dat_resource = 0

    for i in range(1,resources+1):
        a = animalList[0]
        dp[i][0] = dp[i-1][anm_count-1] + (a.get_value(a.resources+1)-a.get_value(a.resources))
            #Each potential 'remaining' resources
        for j in range(1, anm_count):
            a = animalList[j]               #Each animal option
            ## Take max of totalValue with/without resource for this animal
            dp[i][j] = max(dp[i][j-1], dp[i-1][anm_count-1] + (a.get_value(a.resources+1)-a.get_value(a.resources)))

            if dp[i][j] != dp[i][j-1]:
                where_dat_resource = j


        ## This keeps track of where the resource was assigned
        animalList[where_dat_resource].resources += 1


    res = []
    names = []
    for animal in animalList:
        names.append("%s: %.2f" % (animal.name, animal.get_value(animal.resources)))
        res.append(animal.resources)


    plt.bar(range(len(animalList)), res, tick_label = names)
    plt.show()

    return res


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
            animal_survives = random.random() < prob # find out if animal survivies (random)
            if animal_survives:
                # print(a.name)
                value += a.value_constant # add animal's value to total value
    return value/n

# Arbitrary animals
cow = Animal ('cow', [0.9, -1.25], 4)
cat = Animal ('cat', [0.3, -1.25], 1)
mouse = Animal ('mouse', [0.3, -0.6], 1) # should not be given much money
elephant = Animal ('elephant', [0.3, -1.25], 5)
horse = Animal('horse', [0.6, -0.1], 2)
beardedDragon = Animal('dragon', [0.6, -0.6], 4)

testList = [cow, cat, mouse, elephant, horse, beardedDragon]

res, value = resource_allocation(testList,7)
print(res, value)            #Arbitrary weight

print("Average Value test:", test_optimality(testList, res, 10))
