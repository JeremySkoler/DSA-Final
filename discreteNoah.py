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

    def get_value(self, resource):
        val = self.value_constant*(self.survivial_params[0]*math.sqrt(resource/self.survivial_params[1])+self.survivial_params[2])
        if val <=1:
            return val
        else:
            return 1



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

    print(totalValue)

    for j in range(anm_count):
        dp[0][j] = totalValue

    where_dat_resource = 0

    for i in range(1,resources+1):               #Each potential 'remaining' resources
        for j in range(anm_count):
            a = animalList[j]               #Each animal option
            if j == 0:
                ## For first column, otherwise index out of range
                dp[i][j] = dp[i-1][anm_count-1] + (a.get_value(a.resources+1)-a.get_value(a.resources))
            else:
                ## Take max of totalValue with/without resource for this animal
                dp[i][j] = max(dp[i][j-1], dp[i-1][anm_count-1] + (a.get_value(a.resources+1)-a.get_value(a.resources)))
                if dp[i][j] != dp[i][j-1]:
                    where_dat_resource = j

        ## This keeps track of where the resource was assigned
        animalList[where_dat_resource].resources += 1


    ## This works through the final dp matrix looking for animals that are in
    ## the ideal subset and adding their names to a list
    # animalsIncluded = []
    # aniTracker = items              #Track i (column) position in table
    # weightTracker = weight          #Tracks w (row) position in table
    # while aniTracker > 0:
    #     ## If the value is greater than the previous value without the current
    #     ## animal it means that the current animal was used in the final solution
    #     if dp[weightTracker][aniTracker] > dp[weightTracker][aniTracker-1]:
    #         currentAnimal = animalList[aniTracker-1]
    #         animalsIncluded.append(currentAnimal.name)
    #         weightTracker -= currentAnimal.weight     #Account for added animal's weight
    #     aniTracker -= 1
    res = []
    names = []
    for animal in animalList:
        names.append(animal.name)
        res.append(animal.resources)



    plt.bar(range(len(animalList)), res, tick_label = names)
    plt.show()


    return (dp[resources][anm_count-1])


# Arbitrary animals
cow = Animal ('cow', [0.5, 2, 0.5], 4)
cat = Animal ('cat', [0.1, 1, 0.7], 1)
mouse = Animal ('mouse', [0.3, 2, 0.4], 3)
elephant = Animal ('elephant', [0.5, 3, 0.1], 8)
horse = Animal('horse', [1, 2, 0.3], 5)
beardedDragon = Animal('bearded dragon', [0.5, 1, 0.4], 6)

testList = [cow, cat, mouse, elephant, horse, beardedDragon]

print(resource_allocation(testList,7))            #Arbitrary weight
