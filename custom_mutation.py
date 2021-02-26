import numpy as np
import random
from pymoo.model.mutation import Mutation

# function to randomly change a certain patch
def random_reset_mutation(genome_in, point_mutation_prob):
    genome = np.array(list(genome_in))
    for i in range(1, len(genome)):
        if np.random.uniform(0, 1) < point_mutation_prob:
            #bool(random.getrandbits(1)) returns true or false at random
            genome[i]["mining"] = bool(random.getrandbits(1))
    return genome

# class that performs the mutation
class CustomNPointMutation(Mutation):

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
### test jan
#
# import init_pop
#
# test_mates = init_pop.initialize_custom(4,"path")
# mates = np.array([np.array(test_mates[0:2]), np.array(test_mates[2:4])])
#
# #print(len(mates))
# #print(mates)
# #print(mates[0][1]['mining'])
# #print(mates[1][1]['mining'])
# #
# mutClass = CustomNPointMutation(0.8,0.6)
# mutated = mutClass._do(problem= test_mates, X=mates)
# #
# # print(crossed)
# #
# # print("parents")
# # print(mates[0][0][:,11])
# # print(mates[1][0][:,11])
# #
# print(mutated[0][1]['mining'])
# print(mutated[1][1]['mining'])
