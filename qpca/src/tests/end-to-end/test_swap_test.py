import unittest

import cirq

from src.operation.swap_test import swap_test, compute_swap_test_probability
from src.simulation.simulation import simulate


class EqualStatesTestCase(unittest.TestCase):
    def runTest(self):
        self.test_on_single_qubits()

    def test_on_single_qubits(self):
        repetitions = 1000
        expected = repetitions
        parameters = [0, 1]

        for p in parameters:
            with self.subTest(i=p):
                circuit = cirq.Circuit()
                qubits = cirq.LineQubit.range(3)

                if 1 == p:
                    circuit.append(cirq.X(qubits[1]))
                    circuit.append(cirq.X(qubits[2]))
                circuit.append(swap_test(*qubits))
                circuit.append(cirq.measure(qubits[0], key='results'))

                sample_results = simulate(circuit, repetitions, 'results')
                self.assertEqual(expected, sample_results[0])


class OrthogonalStatesTestCase(unittest.TestCase):
    def runTest(self):
        self.test_on_single_qubits()

    def test_on_single_qubits(self):
        repetitions = 1000
        expected = repetitions * 1/2
        parameters = [[0, 1], [1, 0]]

        for p in parameters:
            with self.subTest(i=p):
                circuit = cirq.Circuit()
                qubits = cirq.LineQubit.range(3)

                for p_index in range(0, len(p)):
                    if 1 == p[p_index]:
                        circuit.append(cirq.X(qubits[1 + p_index]))
                circuit.append(swap_test(*qubits))
                circuit.append(cirq.measure(qubits[0], key='results'))

                sample_results = simulate(circuit, repetitions, 'results')
                self.assertAlmostEqual(expected, sample_results[0], delta=expected * 0.06)


class ComputeProbabilityTestCase(unittest.TestCase):
    def runTes(self):
        self.test_compute_probability_orthogonal_states_on_single_qubits()

    def test_compute_probability_orthogonal_states_on_single_qubits(self):
        repetitions = 1000
        expected = 1 - 1/repetitions * (500 * 0 + 500 * 1)

        circuit = cirq.Circuit()
        qubits = cirq.LineQubit.range(3)

        circuit.append(cirq.X(qubits[1]))
        circuit.append(swap_test(*qubits))
        circuit.append(cirq.measure(qubits[0], key='results'))

        sample_results = simulate(circuit, repetitions, 'results')
        actual = compute_swap_test_probability(repetitions, sample_results)
        self.assertAlmostEqual(expected, actual, delta=expected * 0.06)


if __name__ == '__main__':
    unittest.main()
