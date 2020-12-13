import numpy as np
import random
from pymoo.model.crossover import Crossover

class SpatialOnePointCrossover(Crossover):

    def __init__(self, n_points, **kwargs):
        super().__init__(2, 2, 1.0)  # (n_parents,n_offsprings,probability)
        self.n_points = n_points

    def _do(self, problem, X, **kwargs):

        # what is the data structure? Contains X allready the selected 'mates'?
        n_matings = X.shape[1]

        # child land use maps
        child_mining1 = []
        child_mining2 = []

        for _ in range(n_matings):
            # create genome; just the mining column?
            # works like this or first create variables table1 and table2 to access column?
            genome_parent1 = X[0][_]['mining']
            genome_parent2 = X[1][_]['mining']

            # define number of cuts
            num_crossover_points = self.n_points
            num_cuts = min(len(genome_parent1) - 1, num_crossover_points)

            # select random places to cut genome
            cut_points = random.sample(range(1, min(len(genome_parent1),
                                                    len(genome_parent2))), num_cuts)
            cut_points.sort()

            # define initial genome of children
            genome_child1 = list(genome_parent1)
            genome_child2 = list(genome_parent2)

            # get parts of genome from parents to children
            j = 0
            for i in range(0, min(len(genome_parent1), len(genome_parent2))):
                if j < len(cut_points):
                    if i >= cut_points[j]:
                        j = j + 1
                        # alternating parent 1 and 0
                if (j % 2) != 0:
                    genome_child1[i] = 2.
                # alternating 0 and parent 2
                if (j % 2) == 0:
                    genome_child2[i] = 2.

            # dont know if this works with our tables; think we have to add childs as column again..
            child1 = np.where(genome_child1 == 2, genome_parent2, genome_child1)
            child2 = np.where(genome_child2 == 2, genome_parent1, genome_child2)
            child_mining1.append(child1)
            child_mining2.append(child2)

        return np.array([np.array(child_mining1),
                         np.array(child_mining2)])
