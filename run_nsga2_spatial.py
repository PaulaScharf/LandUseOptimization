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

# 9.2
import numpy as np
# import pickle
import matplotlib.pyplot as plt
# import plotly.graph_objects as go
import plotly.express as px

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
        super().__init__(n_var = 273, # study2 = 288, study2_noUrban = 273
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
    pop_size = 288,
    n_offsprings = 5,
    sampling = get_sampling("spatial", default_dir = default_directory),
    crossover = get_crossover("spatial_one_point_crossover", n_points = 5),
    mutation = get_mutation("spatial_n_point_mutation", prob = 0.05,
                            point_mutation_probability = 0.08),
    eliminate_duplicates = False
)

termination = get_termination("n_gen", 2000)

res = minimize(
    problem,
    algorithm,
    termination,
    seed=1,
    save_history=True,
    verbose=True
)


#print(res)
print("response X")
print(res.X)
print("response F")
print(res.F)


# export best fits
pd.DataFrame(res.X[np.argmax(-res.F[:,0], axis = 0)]).to_csv("./results/result_F1_yield.csv")
pd.DataFrame(res.X[np.argmax(-res.F[:,1], axis = 0)]).to_csv("./results/result_F2_biomass.csv")
pd.DataFrame(res.X[np.argmax(-res.F[:,2], axis = 0)]).to_csv("./results/result_F3_dist.csv")

# np.save("./results/resHist.npy", res.history)
np.save("./results/resX.npy", res.X)
np.save("./results/resF.npy", res.F)

f = []
# iterate over the generations
for generation in res.history:
    # retrieve the optima for all objectives from the generation
    opt = generation.opt
    this_f = opt.get("F")
    f.append(this_f)

np.save("./results/f.npy", f)


#
# # Plot of 2D pareto fronts
# f1, (ax1a, ax1b, ax1c) = plt.subplots(1, 3, figsize=(15, 5))
# ax1a.scatter(-res.F[:, 0], -res.F[:, 1]) #, s=30, fc='none', ec='k')
# ax1a.set_title('objective space / pareto front')
# ax1a.set_xlabel('Total yield [€]')
# ax1a.set_ylabel('Biomass loss [tonnes]')
# ax1b.scatter(-res.F[:, 1], -res.F[:, 2]) #, s=30, fc='none', ec='k')
# ax1b.set_title('objective space / pareto front')
# ax1b.set_xlabel('Biomass loss [tonnes]')
# ax1b.set_ylabel('Average distance to protected area [km]')
# ax1c.scatter(-res.F[:, 0], -res.F[:, 2]) #, s=30, fc='none', ec='k')
# ax1c.set_title('objective space / pareto front')
# ax1c.set_xlabel('Total yield [€]')
# ax1c.set_ylabel('Average distance to protected area [km]')
# plt.savefig(default_directory + "/figures/objective_space.png")
# # plt.show()
#
# # find maxima and add them for colouring
# leg = []
# percent = 0.1
# max_0 = max(-res.F[:, 0])
# min_0 = min(-res.F[:, 0])
# quant_0 = max_0 - (max_0 - min_0) * percent
# print("min, max, quant")#
# print(max_0, min_0, quant_0)
# max_1 = max(-res.F[:, 1])
# min_1 = min(-res.F[:, 1])
# quant_1 = max_1 - (max_1 - min_1) * percent
# max_2 = max(-res.F[:, 2])
# min_2 = min(-res.F[:, 2])
# quant_2 = max_2 - (max_2 - min_2) * percent
# for i in list(range(0,len(res.F))):
#     if -res.F[i, 0] > quant_0:
#         leg.append("0")
#     elif -res.F[i, 1] > quant_1:
#         leg.append("1")
#     elif -res.F[i, 2] > quant_2:
#         leg.append("2")
#     else:
#         leg.append("x")
#
#
#
# # Plot of 3D pareto front; saved as HTML
# fig = px.scatter_3d(res.F, -res.F[:, 0], -res.F[:, 1], -res.F[:, 2],
#                     labels={'x':'Total yield [€]', 'y':'Biomass loss [tonnes]', 'z':'Average distance to protected area [km]'},
#                     color = leg)
# fig.update_layout(
#     title={
#         'text': "Pareto Front",
#         'x': 0.5,
#         'xanchor': 'center',
#         'font_size': 30
#     }
# )
# fig.write_html(default_directory + "/figures/objective_space_3d.html")
# fig.show()
#
#
#
# # add here the generations you want to see in the plot
# generations2plot = [25, 50, 100, 250, 500, 1000, 1500, 2000]#, 3500, 5000]
#
# # create an empty list to save objective values per generation
#
# n_gen = np.array(range(1, len(f) + 1))
#
# # make the plot
# fig4, (ax4a, ax4b, ax4c) = plt.subplots(1, 3, figsize=(15, 5))
# # i - 1, because generation 1 has index 0
# for i in generations2plot:
#     ax4a.scatter(-f[i - 1][:, 0], -f[i - 1][:, 1])
#     ax4b.scatter(-f[i - 1][:, 1], -f[i - 1][:, 2])
#     ax4c.scatter(-f[i - 1][:, 0], -f[i - 1][:, 2])
# ax4a.set_xlabel('Total yield [€]')
# ax4a.set_ylabel('Biomass loss [tonnes]')
# ax4a.set_xlabel('Biomass loss [tonnes]')
# ax4a.set_ylabel('Average distance to protected area [km]')
# ax4a.set_xlabel('Total yield [€]')
# ax4a.set_ylabel('Average distance to protected area [km]')
# plt.legend(list(map(str, generations2plot)))
# plt.savefig(default_directory + "/figures/pareto_front_over_generations.png")
# # plt.show()
# # f3.show()
#
#
# ### 3D plot of the pareto fronts over generations
# df = []
# for i in generations2plot:
#     gen = f[i-1]
#     for j in list(range(0, len(gen))):
#         x = np.append(gen[j], int(i))
#         x = x.tolist()
#         df.append(x)
# df = np.array(df)
# legend = df[:, 3].astype(int).astype(str)
#
# fig = px.scatter_3d(df, -df[:, 0], -df[:, 1], -df[:, 2],
#                     labels={'x':'Total yield [€]', 'y':'Biomass loss [tonnes]', 'z':'Average distance to protected area [km]'},
#                     color = legend)
# fig.update_layout(
#     legend_title_text = "Generation",
#     legend_title_font_size = 20,
#     title={
#         'text': "Pareto Front over generations",
#         'x': 0.5,
#         'xanchor': 'center',
#         'font_size': 30
#     }
# )
# fig.write_html(default_directory + "/figures/pareto_fronts_3d.html")
# fig.show()
#
#
# #############################
# ### Convergence tests
#
#
# # get maximum (extremes) of each generation for both objectives
# obj_1 = []
# obj_2 = []
# obj_3 = []
# for i in f:
#     max_obj_1 = min(i[:, 0])
#     max_obj_2 = min(i[:, 1])
#     max_obj_3 = min(i[:, 2])
#
#     obj_1.append(max_obj_1)
#     obj_2.append(max_obj_2)
#     obj_3.append(max_obj_3)
#
# # visualize the maxima against the generation number
# f3, (ax3a, ax3b, ax3c) = plt.subplots(1, 3, figsize=(15, 5))
# ax3a.plot(n_gen, -np.array(obj_1))
# ax3a.set_xlabel("Generation")
# ax3a.set_ylabel("Maximum total yield [€]")
# ax3b.plot(n_gen, -np.array(obj_2))
# ax3b.set_xlabel("Generation")
# ax3b.set_ylabel("Above ground biomass [tonnes]")
# ax3c.plot(n_gen, -np.array(obj_3))
# ax3c.set_xlabel("Generation")
# ax3c.set_ylabel("Average distance to protected areas [km]")
# plt.savefig(default_directory + "/figures/objectives_over_generations.png")
# plt.show()
#
#
#
# # TODO: adjust Hypervolume; doesnt work yet
#
# from pymoo.performance_indicator.hv import Hypervolume
#
# # make an array of the generation numbers
# n_gen = np.array(range(1, len(f) + 1))
# # set reference point
# ref_point = np.array([0.0, 0.0])
# # create the performance indicator object with reference point
# metric = Hypervolume(ref_point=ref_point, normalize=False)
# # calculate for each generation the HV metric
# hv = [metric.calc(i) for i in f]
#
# # visualze the convergence curve
# fig5, ax5 = plt.subplots(1)
# ax5.plot(n_gen, hv, '-o', markersize=4, linewidth=2)
# ax5.set_xlabel("Generation")
# ax5.set_ylabel("Hypervolume")
# plt.savefig(default_directory + "/figures/hypervolume.png")
# # plt.show()
