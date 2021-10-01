import unittest

import cirq

from src.classical_processing.post_processing import compute_e1
from src.operation.quantum_phase_estimation import QPE
from src.simulation.simulation import simulate
from src.tests.test_data_sets import ExampleDataSetQiskitTextbookTGate3CountQubits, \
    ExampleDataSetQiskitTextbookPGate5CountQubits, ExampleDataSetRef19


class EigenvectorStatesTestCase(unittest.TestCase):
    def runTest(self):
        self.test_single_qubit_states()

    def test_single_qubit_states(self):
        parameters = [ExampleDataSetQiskitTextbookTGate3CountQubits, ExampleDataSetQiskitTextbookPGate5CountQubits]
        for p in parameters:
            with self.subTest(i=p):
                dataset = p()
                repetitions = 2048
                expected = dataset.expected
                circuit = cirq.Circuit() + dataset.eigenstate
                circuit.append(QPE(dataset.count_register, dataset.eigenstate_register, dataset.operation))
                circuit.append(cirq.measure(*dataset.count_register, key="results"))

                sample_results = simulate(circuit, repetitions, 'results')
                measurements = sum(sample_results['samples'].data["results"]) / repetitions
                actual = measurements / 2 ** len(dataset.count_register)
                self.assertAlmostEqual(expected, actual, delta=0.01)

    def test_two_qubits_states(self):
        # self.skipTest('testcase not implemented')
        dataset = ExampleDataSetRef19()
        repetitions = 4096
        expected = dataset.expected
        circuit = cirq.Circuit() + dataset.eigenstate
        # print(circuit)

        circuit.append(QPE(dataset.count_register, [dataset.eigenstate_register[0]], dataset.operation))
        circuit.append(cirq.measure(*dataset.count_register, key="results"))

        sample_results = simulate(circuit, repetitions, 'results')
        print(sample_results['histogram'])
        measurements = sum(sample_results['samples'].data["results"]) / repetitions
        actual = measurements / 2 ** len(dataset.count_register)
        actual1 = 0 / 2 ** len(dataset.count_register)
        actual2 = 15 / 2 ** len(dataset.count_register)
        print(actual1, actual2)
        print(compute_e1(dataset._matrix, actual))
        self.assertAlmostEqual(expected[0], actual, delta=0.01)


if __name__ == '__main__':
    unittest.main()
