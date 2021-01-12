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
import matplotlib.pyplot as plt
# from matplotlib.colors import ListedColormap
from pymoo.util.misc import stack
from pymoo.model.problem import Problem 
from calc_obj import calc_mine_yield, calc_mine_biomass, calc_protected_distance

from pymoo.algorithms.nsga2 import NSGA2 
from pymoo.factory import get_sampling, get_crossover, get_mutation
from pymoo.factory import get_termination
from pymoo.optimize import minimize

default_directory = "./"

# read input, yield maps are read -> dont have any

# 9.3
class MyProblem(Problem):

    # define nr of variables etc.
    def __init__(self):
        super().__init__(n_var = 129,
                        n_obj = 2,
                        n_constr = 0,
                        xl = 0.0,
                        xu = 1.0)

    def _evaluate(self, X, out, *args, **kwargs):
        f1 = -calc_mine_yield(X[:]) # calculates mining yield, needs to be maximized
        f2 = calc_mine_biomass(X[:]) # calculates lost biomass, needs to be minimized
        f3 = -calc_protected_distance(X[:]) # calculates average distance to protected areas, needs to be maximized


        out["F"] = np.column_stack([f1, f2, f3])


problem = MyProblem()

# run the algo
algorithm = NSGA2(
    # TODO: automatically get pop_size from init_pop
    pop_size = 129,
    n_offsprings = 5,
    sampling = get_sampling("spatial", default_dir = default_directory),
    crossover = get_crossover("spatial_one_point_crossover", n_points = 5),
    mutation = get_mutation("spatial_n_point_mutation", prob = 0.05,
                            point_mutation_probability = 0.015),
    eliminate_duplicates = False
)

termination = get_termination("n_gen", 500)

res = minimize(
    problem,
    algorithm,
    termination,
    seed=1,
    save_history=True,
    verbose=True
)


print(res)
print("response X")
print(res.X)
print("response F")
print(res.F)


f1, ax1 = plt.subplots(1)
im1 = plt.scatter(-res.F[:, 0], -res.F[:, 1]) #, s=30, fc='none', ec='k')
ax1.set_title('objective space / pareto front')
ax1.set_xlabel('Total yield [tonnes]')
ax1.set_ylabel('Above ground biomass [tonnes]')
plt.show()
#f1.savefig('objective_space.png')

f6, ax6 = plt.subplots(1)
im6 = plt.scatter(-res.F[:, 1], -res.F[:, 2]) #, s=30, fc='none', ec='k')
ax6.set_title('objective space / pareto front')
ax6.set_xlabel('Total biomass [tonnes]')
ax6.set_ylabel('Distance ')
plt.show()

# TODO Create design space (as it is different to tutorial through the vector data)


#############################
### Convergence tests

# create an empty list to save objective values per generation
f = []
# iterate over the generations
for generation in res.history:
    # retrieve the optima for all objectives from the generation
    opt = generation.opt
    this_f = opt.get("F")
    f.append(this_f)

n_gen = np.array(range(1, len(f) + 1))
# print(n_gen)
# print(f)

# get maximum (extremes) of each generation for both objectives
obj_1 = []
obj_2 = []
for i in f:
    max_obj_1 = min(i[:, 0])
    max_obj_2 = min(i[:, 1])

    obj_1.append(max_obj_1)
    obj_2.append(max_obj_2)

# visualize the maxima against the generation number
f3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(9, 5))
ax3a.plot(n_gen, -np.array(obj_1))
ax3a.set_xlabel("Generation")
ax3a.set_ylabel("Maximum total yield [tonnes]")
ax3b.plot(n_gen, -np.array(obj_2))
ax3b.set_xlabel("Generation")
ax3b.set_ylabel("Above ground biomass [tonnes]")
plt.savefig(default_directory + "/figures/objectives_over_generations.png")
plt.show()

# add here the generations you want to see in the plot
generations2plot = [10, 25, 50, 100, 200, 500]#, 750, 1000]#, 1500, 2000]

# make the plot
fig4, ax4 = plt.subplots(1)
# i - 1, because generation 1 has index 0
for i in generations2plot:
    plt.scatter(-f[i - 1][:, 0], -f[i - 1][:, 1])
ax4.set_xlabel('Total yield [tonnes]')
ax4.set_ylabel('Above ground biomass [tonnes]')
plt.legend(list(map(str, generations2plot)))
plt.savefig(default_directory + "/figures/pareto_front_over_generations.png")
plt.show()

from pymoo.performance_indicator.hv import Hypervolume

# make an array of the generation numbers
n_gen = np.array(range(1, len(f) + 1))
# set reference point
ref_point = np.array([0.0, 0.0])
# create the performance indicator object with reference point
metric = Hypervolume(ref_point=ref_point, normalize=False)
# calculate for each generation the HV metric
hv = [metric.calc(i) for i in f]

# visualze the convergence curve
fig5, ax5 = plt.subplots(1)
ax5.plot(n_gen, hv, '-o', markersize=4, linewidth=2)
ax5.set_xlabel("Generation")
ax5.set_ylabel("Hypervolume")
plt.savefig(default_directory + "/figures/hypervolume.png")
plt.show()
