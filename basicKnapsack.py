import math
import random
import numpy as np

class Animal:
    ''' Creates an animal'''

    def __init__(self, name, weight, value):
        '''
        name (str) = animal name
        weight (int or float) = animal's weight or cost
        value = (int or float) = animal's diversity value
        '''

        self.name = name
        self.weight = weight
        self.value = value

def knapsack(animalList, weight):
    ''' Find optimal subset of animals to maximize the total value while remaining
     within the weight limit

    Args
    -----------
    animalList (list) = List of animal objects to evaluate
    weight (int or float) = Maximum weight any subset's weights can sum to

    Returns
    -----------
    animalsIncluded (list) = List of animal names included in optimal subset
    dp[weight][item] (float) = The maximized value achieved by optimal subset
    '''
    items = len(animalList)
    dp = np.zeros((weight+1, items+1))          #Matrix to hold subset values

    i = 1
    for animal in animalList:                   #Each animal option
        for w in range(weight+1):               #Each potential 'remaining' weight
            if animal.weight > w:               #Too heavy to fit, take last best value
                dp[w,i] = dp[w,i-1]
            else:                        #Take max of best value with/without animal
                dp[w,i] = max(dp[w,i-1], animal.value + dp[w-animal.weight, i-1])
        i +=1


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
cow = Animal ('cow',4,4)
cat = Animal ('cat',2,1)
mouse = Animal ('mouse',1,3)
elephant = Animal ('elephant', 6, 8)
horse = Animal('horse', 3, 5)
beardedDragon = Animal('bearded dragon', 1, 6)

testList = [cow, cat, mouse, elephant, horse, beardedDragon]
print(knapsack(testList, 7))            #Arbitrary weight
