import unittest

import cirq

from src.simulation.simulation import simulate


class SimulationTestCase(unittest.TestCase):
    def runTest(self):
        pass

    def test_run_simulation_on_simple_circuit(self):
        expected = {0: 100}
        circuit = cirq.Circuit()
        qubits = cirq.LineQubit.range(0, 1)
        circuit.append(cirq.measure(qubits[0], key='results'))
        actual = simulate(circuit, 100, 'results')
        self.assertDictEqual(expected, actual)

    def test_run_simulation_for_given_repetition(self):
        parameters = {10, 100}
        for p in parameters:
            with self.subTest(i=p):
                expected = {1: p}
                circuit = cirq.Circuit()
                qubits = cirq.LineQubit.range(0, 2)
                circuit.append(cirq.X(qubits[0]))
                circuit.append(cirq.measure(qubits[0], key='results'))
                actual = simulate(circuit, p, 'results')
                self.assertDictEqual(expected, actual)

    def test_run_simulation_for_given_measurement_key(self):
        parameters = {'some', 'key'}
        repetitions = 100
        expected = {1: repetitions}
        for p in parameters:
            with self.subTest(i=p):
                circuit = cirq.Circuit()
                qubits = cirq.LineQubit.range(0, 2)
                circuit.append(cirq.X(qubits[0]))
                circuit.append(cirq.measure(qubits[0], key=p))
                actual = simulate(circuit, repetitions, p)
                self.assertDictEqual(expected, actual)
