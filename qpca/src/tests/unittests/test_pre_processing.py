import unittest

import numpy as np

from src.classical_processing.pre_processing import compute_sigma
from src.tests.test_data_sets import ExampleDataSetRef19, ExampleDataSetMain


class ComputeSigmaTestCase(unittest.TestCase):
    def test_with_data_set_main(self):
        test_data = ExampleDataSetMain()
        feature_x, feature_y = test_data.get_features()
        expected = test_data.get_sigma()
        actual = compute_sigma(feature_x, feature_y)
        self.assertEqual(expected.all(), actual.all())

    def test_with_data_set_ref19(self):
        test_data = ExampleDataSetRef19()
        feature_x, feature_y = test_data.get_features()
        expected = test_data.get_sigma()
        actual = compute_sigma(feature_x, feature_y)
        self.assertEqual(expected.all(), actual.all())


class ComputePTestCase(unittest.TestCase):
    def runTest(self):
        pass

    def test_with_data_set_main(self):
        test_data = ExampleDataSetMain()
        sigma = test_data.get_sigma()
        expected = 1/np.trace(sigma) * sigma


if __name__ == '__main__':
    unittest.main()
