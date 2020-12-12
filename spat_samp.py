# from tutorial, not sure if or for what we need this
# probably to enforce our own spat samp function instead of pymoo built in funcs

import numpy as np
from pymoo.model.sampling import Sampling
import init_pop

class SpatialSampling(Sampling):
    def __init__(self, var_type=np.float, default_dir=None) -> None:
        super().__init__()
        self.var_type = var_type
        self.default_dir = default_dir
    
    def _do(self, problem, n_samples, **kwargs):
        population_np = init_pop.initialize_spatial(n_samples, self.default_dir)
        return population_np

