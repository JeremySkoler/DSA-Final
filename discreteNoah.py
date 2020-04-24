import math
import random
import numpy as np

class Animal:
    ''' Creates an animal'''

    def __init__(self, name, survival_params, value_constant):
        '''
        name (str) = animal name
        weight (int or float) = animal's weight or cost
        value = (int or float) = animal's diversity value
        '''

        self.name = name
        self.survivial_params = self.survivial_params # [0.5, 2, 0.2]
        self.value_constant = self.value_constant

    def get_value(self, money):
        val = self.value_constant*self.survivial_params[0]*sqrt(money/self.survivial_params[1])+self.survivial_params[2]
        if val <=1:
            return val
        else:
            return 1



def knapsack(animalList, resources):
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
    dp = np.zeros((resources+1, anm_count+1))          #Matrix to hold subset values

    totalValue = 0
    for animal in animalList:
        totalValue += animal.get_value(0)

    for i in range(anm_count+1):
        dp[0][j] = totalValue


    for i in range(anm_count+1):                   #Each animal option
        for j in range(resources+1):               #Each potential 'remaining' resources
                                            #Take max of best value with/without animal
            dp[i,j] = max(dp[i,j-1], animalList[i].value + dp[i-animalList[j].weight, j-1])


    ## This works through the final dp matrix looking for animals that are in
    ## the ideal subset and adding their names to a list
    animalsIncluded = []
    aniTracker = items              #Track i (column) position in table
    weightTracker = weight          #Tracks w (row) position in table
    while aniTracker > 0:
        ## If the value is greater than the previous value without the current
        ## animal it means that the current animal was used in the final solution
        if dp[weightTracker][aniTracker] > dp[weightTracker][aniTracker-1]:
            currentAnimal = animalList[aniTracker-1]
            animalsIncluded.append(currentAnimal.name)
            weightTracker -= currentAnimal.weight     #Account for added animal's weight
        aniTracker -= 1


    return (animalsIncluded, dp[weight][items])


# Arbitrary animals
cow = Animal ('cow', [0.5, 2, 0.5], 4)
cat = Animal ('cat', [0.1, 1, 0.7], 1)
mouse = Animal ('mouse', [0.3, 2, 0.4], 3)
elephant = Animal ('elephant', [0.5, 3, 0.1], 8)
horse = Animal('horse', [1, 2, 0.3], 5)
beardedDragon = Animal('bearded dragon', [0.5, 1, 0.4], 6)

testList = [cow, cat, mouse, elephant, horse, beardedDragon]
print(knapsack(testList, 7))            #Arbitrary weight
