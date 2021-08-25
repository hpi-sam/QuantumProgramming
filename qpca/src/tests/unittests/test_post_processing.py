import unittest
from src.classical_processing.post_processing import compute_e1, compute_e2
from src.tests.test_data_sets import ExampleDataSetRef19, ExampleDataSetMain


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
        self.skipTest('know issue: function does not work with this data set')

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
        self.skipTest('know issue: function does not work with this data set')

        test_data = ExampleDataSetMain()

        expected = test_data.get_expected_e2()
        actual = compute_e2(test_data.get_sigma(), test_data.get_purity())
        self.assertAlmostEqual(expected, actual, delta=0.00001)


if __name__ == '__main__':
    unittest.main()
