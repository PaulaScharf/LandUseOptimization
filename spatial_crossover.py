import numpy as np
import random
from pymoo.model.crossover import Crossover

class SpatialOnePointCrossover(Crossover):

    def __init__(self, n_points, **kwargs):
        super().__init__(2, 2, 1.0)  # (n_parents,n_offsprings,probability)
        self.n_points = n_points

    def _do(self, problem, X, **kwargs):

        #TODO: is this right?
        n_matings = len(X)

        # child land use maps
        child_mining1 = []
        child_mining2 = []

        for _ in range(n_matings):
            genome_parent1 = X[0]
            genome_parent2 = X[1]

            # define number of cuts
            num_crossover_points = self.n_points
            num_cuts = min(len(genome_parent1) - 1, num_crossover_points)

            # select random places to cut genome
            cut_points = random.sample(range(1, min(len(genome_parent1),
                                                    len(genome_parent2))), num_cuts)
            cut_points.sort()

            # define initial genome of children (np.array(list(...)) is used to create a copy)
            genome_child1 = np.array(list(genome_parent1))
            genome_child2 = np.array(list(genome_parent2))

            # get parts of genome from parents to children
            # used 2 as placeholder, because 0 wouldnt work if we use 0 and 1 for mining = true / false
            j = 0
            for i in range(0, min(len(genome_parent1), len(genome_parent2))):
                if j < len(cut_points):
                    if i >= cut_points[j]:
                        j = j + 1
                # alternating parent 1 and 0
                if (j % 2) != 0:
                    genome_child1[i][0] = '2'
                # alternating 0 and parent 2
                if (j % 2) == 0:
                    genome_child2[i][0] = '2'

            child1_filled = np.where(genome_child1 == '2', genome_parent2, genome_child1)
            child2_filled = np.where(genome_child2 == '2', genome_parent1, genome_child2)

            child_mining1.append(child1_filled)
            child_mining2.append(child2_filled)
        return np.array([np.array(child_mining1),
                         np.array(child_mining2)])

############# use following lines for testing #############
#import sys
#sys.path.insert(0, 'input_data/test_sample')
#from test_parents_crossover import *
#test = SpatialOnePointCrossover(2)
#Sprint(test._do(1,population))
