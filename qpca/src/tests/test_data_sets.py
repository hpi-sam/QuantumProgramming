import numpy as np


class ExampleDataSetRef19(object):
    def __init__(self):
        x = np.array([4, 3, 4, 4, 3, 3, 3, 3, 4, 4, 4, 5, 4, 3, 4])
        y = np.array([3028, 1365, 2726, 2538, 1318, 1693, 1412, 1632, 2875, 3564, 4412, 4444, 4278, 3064, 3857]) / 1000
        self._matrix = np.array([x, y])
        self._sigma = np.cov(self._matrix)
        normed_covariance = self._sigma / np.trace(self._sigma)
        self._purity = np.trace(np.matmul(normed_covariance, normed_covariance))

    def get_features(self):
        return self._matrix[0], self._matrix[1]

    def get_sigma(self):
        return self._sigma

    def get_purity(self):
        return self._purity

    def get_expected_e1(self):
        return 1.57286

    def get_expected_e2(self):
        return 0.105029


class ExampleDataSetMain(object):
    def __init__(self):
        self._matrix = np.array([[1.5, 0.5], [0.5, 1.5]])
        self._sigma = np.cov(self._matrix)
        normed_covariance = self._sigma / np.trace(self._sigma)
        self._purity = np.trace(np.matmul(normed_covariance, normed_covariance))

    def get_features(self):
        return self._matrix[0], self._matrix[1]

    def get_sigma(self):
        return self._sigma

    def get_purity(self):
        return self._purity

    def get_expected_e1(self):
        return 2

    def get_expected_e2(self):
        return 1