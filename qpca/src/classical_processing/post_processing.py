import numpy as np
from cmath import sqrt


def compute_e1(sigma, purity):
    result = np.trace(sigma) * (1 + sqrt(1-2*(1-purity))) / 2
    return result


def compute_e2(sigma, purity):
    result = np.trace(sigma) * (1 - sqrt(1-2*(1-purity)))/2
    return result
