import numpy as np

from pymoo.model.crossover import Crossover
from pymoo.operators.crossover.util import crossover_mask

def crossover_mask(X, M):
    # convert input to output by flatting along the first axis
    _X = np.copy(X)
    _X[0][M] = X[1][M]
    _X[1][M] = X[0][M]

    return _X

class CustomUniformCrossover(Crossover):

    def __init__(self, **kwargs):
        super().__init__(2, 2, **kwargs)

    def _do(self, problem, X, **kwargs):
        print(X["mining"])
        _, n_matings, n_var = X.shape
        M = np.random.random((n_matings, n_var)) < 0.5
        _X = crossover_mask(X, M)
        return _X
