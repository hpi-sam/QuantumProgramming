import unittest
import numpy as np
from src.classical_processing.post_processing import compute_e1, compute_e2


class ExampleDataSetRef19(object):
    def __init__(self):
        self._sigma = np.array([[0.380952, 0.573476], [0.573476, 1.29693]])
        normed_covariance = self._sigma / np.trace(self._sigma)
        self._purity = np.trace(np.matmul(normed_covariance, normed_covariance))

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
        print(self._purity)

    def get_sigma(self):
        return self._sigma

    def get_purity(self):
        return self._purity

    def get_expected_e1(self):
        return 2

    def get_expected_e2(self):
        return 1


class ComputeE1TestCase(unittest.TestCase):
    def runTest(self):
        self.test_compute_data_set_ref19()
        self.test_compute_data_set_main()

    def test_compute_data_set_ref19(self):
        test_data = ExampleDataSetRef19()

        expected = test_data.get_expected_e1()
        actual = compute_e1(test_data.get_sigma(), test_data.get_purity())
        self.assertAlmostEqual(expected, actual, delta=0.00001)

    def test_compute_data_set_main(self):
        test_data = ExampleDataSetMain()

        expected = test_data.get_expected_e1()
        actual = compute_e1(test_data.get_sigma(), test_data.get_purity())
        self.assertAlmostEqual(expected, actual, delta=0.00001)


class ComputeE2TestCase(unittest.TestCase):
    def runTest(self):
        self.test_compute_data_set_ref19()
        self.test_compute_data_set_main()

    def test_compute_data_set_ref19(self):
        test_data = ExampleDataSetRef19()

        expected = test_data.get_expected_e2()
        actual = compute_e2(test_data.get_sigma(), test_data.get_purity())
        self.assertAlmostEqual(expected, actual, delta=0.00001)

    def test_compute_data_set_main(self):
        test_data = ExampleDataSetMain()

        expected = test_data.get_expected_e2()
        actual = compute_e2(test_data.get_sigma(), test_data.get_purity())
        self.assertAlmostEqual(expected, actual, delta=0.00001)


if __name__ == '__main__':
    unittest.main()
