import numpy as np
from pymoo.model.problem import Problem
# from tutorial
# 9.1
from pymoo import factory
from pymoo.model.crossover import Crossover
import spatial_extension_pymoo as sep

import pandas as pd

# add spatial functions to pymoo lib
factory.get_sampling_options = sep._new_get_sampling_options
factory.get_crossover_options = sep._new_get_crossover_options
factory.get_mutation_options = sep._new_get_mutation_options
Crossover.do = sep._new_crossover_do

class MyProblem(Problem):

    def __init__(self):
        super().__init__(n_var=2,
                         n_obj=2,
                         n_constr=2,
                         xl=np.array([-2,-2]),
                         xu=np.array([2,2]))

    def _evaluate(self, X, out, *args, **kwargs):
        f1 = X[:,0]**2 + X[:,1]**2
        f2 = (X[:,0]-1)**2 + X[:,1]**2

        g1 = 2*(X[:, 0]-0.1) * (X[:, 0]-0.9) / 0.18
        g2 = - 20*(X[:, 0]-0.4) * (X[:, 0]-0.6) / 4.8

        out["F"] = np.column_stack([f1, f2])
        out["G"] = np.column_stack([g1, g2])


vectorized_problem = MyProblem()

from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation

algorithm = NSGA2(
    pop_size=40,
    n_offsprings=10,
    sampling=get_sampling("real_random"),
    crossover=get_crossover("real_sbx", prob=0.9, eta=15),
    mutation=get_mutation("custom2_real_pm", eta=20),
    eliminate_duplicates=True
)

from pymoo.factory import get_termination

termination = get_termination("n_gen", 2)

from pymoo.optimize import minimize

res = minimize(vectorized_problem,
               algorithm,
               termination,
               seed=1,
               save_history=True,
               verbose=True)
