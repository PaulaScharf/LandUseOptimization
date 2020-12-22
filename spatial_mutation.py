import numpy as np
import random
from pymoo.model.mutation import Mutation

# function to randomly change a certain patch
def random_reset_mutation(genome_in, point_mutation_prob):
    genome = np.array(list(genome_in))
    for i in range(1, len(genome)):
        if np.random.uniform(0, 1) < point_mutation_prob:
            #bool(random.getrandbits(1)) returns true or false at random
            genome[i][0] = bool(random.getrandbits(1))
    return genome

# class that performs the mutation
class SpatialNPointMutation(Mutation):

    def __init__(self, prob=None,point_mutation_probability=0.01):
        super().__init__()
        self.prob = prob
        self.point_mutation_probability = point_mutation_probability

    def _do(self, problem, X, **kwargs):
        offspring = []
        # loop over individuals in population
        for i in X:
            # performe mutation with certain probability
            if np.random.uniform(0, 1) < self.prob:
                # perform mutation on i (genome)
                mutated_genome = random_reset_mutation(i,self.point_mutation_probability)

                offspring.append(mutated_genome)
            # if no mutation
            else:
                offspring.append(i)
        offspring = np.array(offspring)
        return offspring

############# use following lines for testing #############
import sys
sys.path.insert(0, 'input_data/test_sample')
from test_parents_crossover import *
test = SpatialNPointMutation(0.8, 0.6)
print(test._do(1,population))
