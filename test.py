import numpy as np
from pymoo.util.misc import stack
from pymoo.model.problem import Problem
import spatial_extension_pymoo as sep
from pymoo import factory

# 9.3
class MyProblem(Problem):

    # define nr of variables etc.
    def __init__(self):
        super().__init__(n_var = 288,
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

factory.get_sampling_options = sep._new_get_sampling_options
from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation

algorithm = NSGA2(
    pop_size=40,
    n_offsprings=10,
    sampling=get_sampling("spatial", default_dir = default_directory),
    crossover=get_crossover("real_sbx", prob=0.9, eta=15),
    mutation=get_mutation("real_pm", eta=20),
    eliminate_duplicates=True
)

from pymoo.factory import get_termination

termination = get_termination("n_gen", 40)

from pymoo.optimize import minimize

res = minimize(problem,
               algorithm,
               termination,
               seed=1,
               save_history=True,
               verbose=True)

f1, (ax1a, ax1b, ax1c) = plt.subplots(1, 3, figsize=(15, 5))
ax1a.scatter(-res.F[:, 0], -res.F[:, 1]) #, s=30, fc='none', ec='k')
ax1a.set_title('objective space / pareto front')
ax1a.set_xlabel('Total yield [€]')
ax1a.set_ylabel('Biomass loss [tonnes]')
ax1b.scatter(-res.F[:, 1], -res.F[:, 2]) #, s=30, fc='none', ec='k')
ax1b.set_title('objective space / pareto front')
ax1b.set_xlabel('Biomass loss [tonnes]')
ax1b.set_ylabel('Average distance to protected area [km]')
ax1c.scatter(-res.F[:, 0], -res.F[:, 2]) #, s=30, fc='none', ec='k')
ax1c.set_title('objective space / pareto front')
ax1c.set_xlabel('Total yield [€]')
ax1c.set_ylabel('Average distance to protected area [km]')
plt.savefig(default_directory + "/figures/objective_space.png")
# plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(-res.F[:, 0], -res.F[:, 1], -res.F[:, 2])
ax.set_xlabel('Total yield [€]')
ax.set_ylabel('Biomass loss [tonnes]')
ax.set_zlabel('Average distance to protected area [km]')
plt.savefig(default_directory + "/figures/objective_space_3d.png")
plt.savefig(default_directory + "/figures/objective_space_3d.svg")
# plt.show()
