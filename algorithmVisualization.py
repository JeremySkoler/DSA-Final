import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
        self.resource_hist = [0]
        self.SC_hist = [self.get_survival_rate(0)]
        self.TV_hist = [self.get_value(0)]

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

    ## Biodiversity is the product of all the animal's survival rates
    biodiversity = 1
    for animal in animalList:
        biodiversity *= animal.get_survival_rate(0)

    ## ecosys is DP matrix stores ecosystem value
    ecosys = np.zeros((resources+1, anm_count))
    ecosystem_value = totalValue * biodiversity     #resources-less eco val
    for j in range(anm_count):
        ecosys[0][j] = ecosystem_value



    for i in range(1,resources+1):
        where_dat_resource = 0      #Tracks where each additional resource is allocated
        a = animalList[0]           #Each animal option

        ## Update first column assuming resouce allocation
        dp[i][0] = dp[i-1][-1] + (a.get_value(a.resources+1)-a.get_value(a.resources))

        ## Calculate new biodiversity and then ecosystem value
        temp_biodiversity = (biodiversity/a.get_survival_rate(a.resources)) * a.get_survival_rate(a.resources+1)
        ecosys[i][0] = dp[i][0] * temp_biodiversity

        #Each potential 'remaining' resources
        for j in range(1, anm_count):
            a = animalList[j]

            # Potential total, biodiversity and ecosystem value with resource allocated to this animal
            pot_Tvalue = dp[i-1][-1] + (a.get_value(a.resources+1)-a.get_value(a.resources))
            pot_bio = (biodiversity/a.get_survival_rate(a.resources)) * a.get_survival_rate(a.resources+1)
            pot_eco_val = pot_Tvalue * pot_bio

            # Potential better than last best?
            ecosys[i][j] = max(ecosys[i][j-1], pot_eco_val)

            ## Notice ecosys determines the value stored in dp
            ## dp now just data storage matrix (probably could replace with variable)
            if ecosys[i][j-1] < ecosys[i][j]:
                dp[i][j] = pot_Tvalue
                where_dat_resource = j          #Track resource allocation location
            else:
                dp[i][j] = dp[i][j-1]

        ### variables updated
        lucky_duck = animalList[where_dat_resource]     #Animal given resource
        biodiversity = (biodiversity/lucky_duck.get_survival_rate(lucky_duck.resources)) * lucky_duck.get_survival_rate(lucky_duck.resources+1)
        lucky_duck.resources += 1

        for animal in animalList:
            animal.resource_hist.append(animal.resources)
            animal.SC_hist.append(animal.get_survival_rate(animal.resources))
            animal.TV_hist.append(animal.get_value(animal.resources))

    res = []
    names = []
    for animal in animalList:
        names.append("%s: %.2f" % (animal.name, animal.get_survival_rate(animal.resources)))
        res.append(animal.resources)
    #plt.bar(range(len(animalList)), res, tick_label = names)
    #plt.show()

    return res



# Arbitrary animals
pBear = Animal ('Polar Bear', [0.5, 20, 0.2], 8)
sHorse = Animal ('Seahorse', [0.2, 10, 0.7], 4)
raccoon = Animal ('Raccoon', [0.3, 20, 0.4], 7)
elephant = Animal ('Elephant', [0.4, 30, 0.5], 3)
sMonkey = Animal('Spider Monkey', [1, 20, 0.3], 2)
bDragon = Animal('Bearded Dragon', [0.5, 10, 0.4], 4)
leech = Animal('Leech', [0.6, 40, 0.2], 5)

testList = [pBear, sHorse, raccoon, elephant, sMonkey, bDragon, leech]

## Animals start thriving when the # of total resources is a factor
## of 10 bigger than the animals' approximate survival_params[1]
resource_allocation(testList,200)





#
#
#
#
# elephantX = eRes
# dragonX = dRes
# elephantY = []
# dragonY = []
# for x in elephantX:
#     temp = 0.5*math.sqrt(x/30)+0.1
#     elephantY.append(temp)
# for x in dragonX:
#     temp = 0.5*math.sqrt(x/10)+0.4
#     dragonY.append(temp)
# # elephantY = 0.5*math.sqrt(elephantX/30)+0.1
# # dragonY = 0.5*math.sqrt(dragonX/10)+0.4
#
# x1 = np.linspace(0, 10, 100)
# y1 = np.cos(x)


fig, ax = plt.subplots()
lines = []
Xs = []
Ys = []
legend = []
colors = ['b','g','r','c','m','k','y']
i = 0
for animal in testList:
    Xs.append(animal.resource_hist)
    Ys.append(animal.SC_hist)
    line, = ax.plot(animal.resource_hist, animal.SC_hist, colors[i])
    lines.append(line)
    legend.append(animal.name)
    i += 1

# line, = ax.plot(elephantX, elephantY, color='k')
# line1, = ax.plot(dragonX, dragonY, color='b')


def update(num, Xs, Ys, lines):
    for i in range(len(Xs)):
        lines[i].set_data(Xs[i][:num], Ys[i][:num])
        lines[i].axes.axis([0, 60, 0, 1.1])
    return lines

ani = animation.FuncAnimation(fig, update, fargs=[Xs, Ys, lines],
                              interval=45, blit=True)
plt.plot([-5,65],[1,1],'-.r')
plt.title('Survival chance as resources are allocated')
plt.ylabel('Survivial Chance')
plt.xlabel('Resources')
plt.legend(legend, loc = 'lower right')
plt.show()


# def update(num, elephantX, elephantY, line, dragonX, dragonY, line1):
#     line.set_data(elephantX[:num], elephantY[:num])
#     line.axes.axis([0, 10, 0, 1])
#     line1.set_data(dragonX[:num], dragonY[:num])
#     line1.axes.axis([0, 10, 0, 1])
#     return line, line1,
#
# plt.show()
