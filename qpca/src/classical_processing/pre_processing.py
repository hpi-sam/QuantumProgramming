# calculate sigma
# calculate normalized covariance
# purify state
# calculate unitary prep
import numpy as np


def compute_sigma(feature_x, feature_y):
    matrix = np.array([feature_x, feature_y])
    return np.cov(matrix)


def compute_density_matrix(sigma):
    return 1/np.trace(sigma) * sigma
