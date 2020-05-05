import math
import random
import numpy as np
# import matplotlib.pyplot as plt
from matplotlib import pyplot as plt

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
        survival_chance = (self.survivial_params[0]*math.sqrt(resources/self.survivial_params[1])+self.survivial_params[2])
        if survival_chance >=1:
            survival_chance = 1
        return survival_chance

    def get_value(self, resources):
        survival_chance = self.get_survival_rate(resources)
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
    res (list) = The resources allocated to each animal
    names (lsit) = The names of each animal in the order their resource allocations
                    appear in res

    '''
    anm_count = len(animalList)

    init_val = 0
    for animal in animalList:
        init_val += animal.get_value(0)

    ## Biodiversity is the product of all the animal's survival rates
    biodiversity = 1
    for animal in animalList:
        biodiversity *= animal.get_survival_rate(0)

    ## ecosys is DP matrix stores ecosystem value
    ecosys = np.zeros((resources+1, anm_count))
    ecosystem_value = init_val * biodiversity     #resources-less eco val
    for j in range(anm_count):
        ecosys[0][j] = ecosystem_value

    ##Tracks Tval used in best solution in the last round of resource allocation
    last_round_Tval = init_val

    for i in range(1,resources+1):
        where_dat_resource = 0      #Tracks where each additional resource is allocated
        a = animalList[0]           #Each animal option

        ## Update first column assuming resouce allocation
        temp_Tval = last_round_Tval + (a.get_value(a.resources+1)-a.get_value(a.resources))

        ## Calculate new biodiversity and then ecosystem value
        temp_biodiversity = (biodiversity/a.get_survival_rate(a.resources)) * a.get_survival_rate(a.resources+1)
        ecosys[i][0] = temp_Tval * temp_biodiversity

        #Each potential 'remaining' resources
        for j in range(1, anm_count):
            a = animalList[j]

            # Potential total, biodiversity and ecosystem value with resource allocated to this animal
            pot_Tvalue = last_round_Tval + (a.get_value(a.resources+1)-a.get_value(a.resources))
            pot_bio = (biodiversity/a.get_survival_rate(a.resources)) * a.get_survival_rate(a.resources+1)
            pot_eco_val = pot_Tvalue * pot_bio

            # Potential better than last best?
            ecosys[i][j] = max(ecosys[i][j-1], pot_eco_val)

            ## Save updated Tvalue for best solution so far this round
            if ecosys[i][j-1] < ecosys[i][j]:
                best_sofar_Tval = pot_Tvalue
                where_dat_resource = j          #Track resource allocation location


        ### variables updated
        last_round_Tval = best_sofar_Tval
        lucky_duck = animalList[where_dat_resource]     #Animal given resource
        biodiversity = (biodiversity/lucky_duck.get_survival_rate(lucky_duck.resources)) * lucky_duck.get_survival_rate(lucky_duck.resources+1)
        lucky_duck.resources += 1


    res = []
    names = []
    for animal in animalList:
        names.append("%s: %.2f" % (animal.name, animal.get_survival_rate(animal.resources)))
        res.append(animal.resources)

    return res, names

def plot_results(res, names):
    """
    Makes a bar plot of how many resources each animal gets
    """
    print("Plot results function running")
    plt.bar(range(len(res)), res, tick_label = names)
    plt.xlabel("Animal and Chance of Survival")
    plt.ylabel("Resources Allocated")
    plt.title("Animals vs Resources Allocated")
    plt.show()

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

if __name__ == "__main__":
    res, names = resource_allocation(testList,100)
    plot_results(res, names)
