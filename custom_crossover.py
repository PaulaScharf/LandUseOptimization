import numpy as np
import random
from pymoo.model.crossover import Crossover

class CustomOnePointCrossover(Crossover):

    def __init__(self, n_points, **kwargs):
        super().__init__(2, 2, 1.0)  # (n_parents,n_offsprings,probability)
        self.n_points = n_points

    def _do(self, problem, X, **kwargs):

        n_matings = X.shape[1]

        # child land use maps
        child_mining1 = []
        child_mining2 = []

        for _ in range(n_matings):
            genome_parent1 = X[0][_]['mining']
            genome_parent2 = X[1][_]['mining']

            # define number of cuts
            num_crossover_points = self.n_points
            num_cuts = min(len(genome_parent1) - 1, num_crossover_points)

            # select random places to cut genome
            cut_points = random.sample(range(1, min(len(genome_parent1),
                                                    len(genome_parent2))), num_cuts)
            cut_points.sort()

            # define initial genome of children (np.array(list(...)) is used to create a copy)
            genome_child1 = (list(genome_parent1))
            genome_child2 = (list(genome_parent2))

            # get parts of genome from parents to children
            # used 2 as placeholder, because 0 wouldnt work if we use 0 and 1 for mining = true / false
            j = 0
            for i in range(0, min(len(genome_parent1), len(genome_parent2))):
                if j < len(cut_points):
                    if i >= cut_points[j]:
                        j = j + 1
                # alternating parent 1 and 0
                if (j % 2) != 0:
                    genome_child1[i] = None
                # alternating 0 and parent 2
                if (j % 2) == 0:
                    genome_child2[i] = None

            genome1 = np.array(genome_child1)
            genome2 = np.array(genome_child2)

            child1_filled = np.where(genome1 == None, genome_parent2, genome_parent1)
            child2_filled = np.where(genome2 == None, genome_parent2, genome_parent1)

            child1 = X[0][_]
            child2 = X[1][_]
            child1['mining'] = child1_filled
            child2['mining'] = child2_filled

            child_mining1.append(child1)
            child_mining2.append(child2)
        return np.array([np.array(child_mining1),
                         np.array(child_mining2)])

############# use following lines for testing #############
#import sys
#sys.path.insert(0, 'input_data/test_sample')
#from test_parents_crossover import *
#test = CustomOnePointCrossover(2)
#Sprint(test._do(1,population))


# ### test jan
#
# import init_pop
#
# test_mates = init_pop.initialize_custom(4,"path")
# mates = np.array([np.array(test_mates[0:2]), np.array(test_mates[2:4])])
#
# print(len(mates))
# print(mates)
# print(mates[0][1]['mining'])
# print(mates[1][1]['mining'])
#
# crossClass = CustomOnePointCrossover(2)
# crossed = crossClass._do(problem= test_mates, X=mates)
#
# #print(crossed)
#
# # print("parents")
# # print(mates[0][0][:,11])
# # print(mates[1][0][:,11])
# #
# print(crossed[0][1]['mining'])
# print(crossed[1][1]['mining'])
