# from tutorial
# 9.1
from pymoo import factory
from pymoo.model.crossover import Crossover
import spatial_extension_pymoo as sep

# add spatial functions to pymoo lib
factory.get_sampling_options = sep._new_get_sampling_options
factory.get_crossover_options = sep._new_get_crossover_options
factory.get_mutation_options = sep._new_get_mutation_options
Crossover.do = sep._new_crossover_do

# 9.2
import numpy as np
# import pickle
# import matplotlib.pyplot as plt 
# from matplotlib.colors import ListedColormap
from pymoo.util.misc import stack
from pymoo.model.problem import Problem 
from calc_obj import calc_mine_yield, calc_mine_biomass

from pymoo.algorithms.nsga2 import NSGA2 
from pymoo.factory import get_sampling, get_crossover, get_mutation
from pymoo.factory import get_termination
from pymoo.optimize import minimize

# dir = ./

# read input, yield maps are read -> dont have any

# 9.3
class MyProblem(Problem):

    # define nr or variables etc.
    def __init__(self):
        super().__init__(n_var = 100,
                        n_obj = 2,
                        n_constr = 0,
                        xl = 0.0,
                        xu = 1.0)

    def _evaluate(self, X, out, *args, **kwargs):
        # f1 = 
        # f2 = 

        out["F"] = np.column_stack([f1, f2])

# algorithms = ...