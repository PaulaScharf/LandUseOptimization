import numpy as np

from pymoo.model.mutation import Mutation
from pymoo.operators.repair.to_bound import set_to_bounds_if_outside_by_problem


class CustomPolynomialMutation(Mutation):
    def __init__(self, eta, prob=None):
        super().__init__()
        self.eta = float(eta)

        if prob is not None:
            self.prob = float(prob)
        else:
            self.prob = None

    def _do(self, problem, X, **kwargs):
        result=[]
        for i in X:
            #X = X.astype(np.float)
            Y = np.full(i.shape, np.inf)

            if self.prob is None:
                self.prob = 1.0 / problem.n_var

            do_mutation = np.random.random(i.shape) < self.prob
            Y = i
            #xl = np.repeat(problem.xl[None, :], i.shape[0], axis=0)[do_mutation]
            xl = problem.xl[do_mutation]
            #xu = np.repeat(problem.xu[None, :], i.shape[0], axis=0)[do_mutation]
            xu = problem.xu[do_mutation]
            i = i[do_mutation]

            delta1 = (i['mining'].astype(int) - xl) / (xu - xl)
            delta2 = (xu - i['mining'].astype(int)) / (xu - xl)

            mut_pow = 1.0 / (self.eta + 1.0)

            rand = np.random.random(i.shape)
            mask = rand <= 0.5
            mask_not = np.logical_not(mask)

            deltaq = np.zeros(i.shape)

            xy = 1.0 - delta1
            val = 2.0 * rand + (1.0 - 2.0 * rand) * (np.power(xy, (self.eta + 1.0)))
            d = np.power(val, mut_pow) - 1.0
            deltaq[mask] = d[mask]

            xy = 1.0 - delta2
            val = 2.0 * (1.0 - rand) + 2.0 * (rand - 0.5) * (np.power(xy, (self.eta + 1.0)))
            d = 1.0 - (np.power(val, mut_pow))
            deltaq[mask_not] = d[mask_not]
            deltaq = deltaq * (xu - xl)
            deltaq[deltaq<0] = -1
            deltaq[deltaq>0] = 1

            # mutated values
            _Y = i['mining'].astype(int) + deltaq

            # back in bounds if necessary (floating point issues)
            _Y[_Y < xl] = xl[_Y < xl]
            _Y[_Y > xu] = xu[_Y > xu]

            # set the values for output
            print(Y[do_mutation]["mining"])
            Y[do_mutation]["mining"] = _Y
            print(Y[do_mutation]["mining"])

            result.append(Y)
            # in case out of bounds repair (very unlikely)
            #Y = set_to_bounds_if_outside_by_problem(problem, Y)

        return result
