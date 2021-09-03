import unittest
import cirq
from cirq.ops import raw_types
from src.operation.quantum_phase_estimation import QPE
from src.tests.test_data_sets import ExampleDataSetQiskitTextbookTGate3CountQubits, \
    ExampleDataSetQiskitTextbookPGate5CountQubits


class QPEInitTestCase(unittest.TestCase):
    def runTest(self):
        pass

    def test_is_operation(self):
        test_instance = QPE(cirq.LineQubit.range(0, 1), cirq.LineQubit.range(1, 2), cirq.X)
        self.assertIsInstance(test_instance, raw_types.Operation)

    def test_detect_wrong_number_of_eigenstate_qubits(self):
        parameters = [[2, 2, cirq.X], [3, 1, cirq.SWAP]]
        for p in parameters:
            with self.subTest(i=p):
                register_1 = cirq.LineQubit.range(0, p[0])
                register_2 = cirq.LineQubit.range(p[0], p[0] + p[1])
                self.assertRaises(ValueError, QPE, register_1, register_2, p[2])

    def test_detects_empty_register(self):
        parameters = [[0, 0, cirq.X], [-1, 1, cirq.X]]
        for p in parameters:
            with self.subTest(i=p):
                register_1 = cirq.LineQubit.range(0, p[0])
                register_2 = cirq.LineQubit.range(p[0], p[0] + p[1])
                self.assertRaises(ValueError, QPE, register_1, register_2, p[2])


class QPEDecomposeTestCase(unittest.TestCase):
    def test_init_count_qubits_in_superposition(self):
        parameters = [[1, 2, cirq.SWAP], [3, 2, cirq.SWAP]]
        for p in parameters:
            with self.subTest(i=p):
                test_instance = QPE(cirq.LineQubit.range(0, p[0]), cirq.LineQubit.range(p[0], p[0] + p[1]), p[2])
                expected = cirq.Circuit()
                for i in range(0, p[0]):
                    expected.append(cirq.H(cirq.LineQubit(i)))
                actual = cirq.Circuit(cirq.decompose_once(test_instance))[:1]
                cirq.testing.assert_same_circuits(actual, expected)

    def test_has_diagram(self):
        parameter = [ExampleDataSetQiskitTextbookTGate3CountQubits, ExampleDataSetQiskitTextbookPGate5CountQubits]

        for p in parameter:
            with self.subTest(i=p):
                dataset = p()
                circuit = dataset.eigenstate
                circuit.append(cirq.decompose_once(
                    QPE(dataset.count_register, dataset.eigenstate_register, dataset.operation)
                    )
                )
                cirq.testing.assert_has_diagram(circuit, dataset.get_str_diagram())


class QPEQubitTestCase(unittest.TestCase):
    def runTest(self):
        pass

    def test_get_qubits(self):
        parameters = [[2, 1, cirq.X], [1, 2, cirq.SWAP]]
        for p in parameters:
            with self.subTest(i=p):
                register_1 = cirq.LineQubit.range(0, p[0])
                register_2 = cirq.LineQubit.range(p[0], p[0] + p[1])
                expected = tuple(register_1 + register_2)
                test_instance = QPE(register_1, register_2, p[2])
                actual = test_instance.qubits
                self.assertEqual(expected, actual)


class QPEUnitaryOperationTestCase(unittest.TestCase):
    def runTest(self):
        pass

    def test_get_operation(self):
        parameters = [[1, 1, cirq.T], [2, 2, cirq.SWAP]]
        for p in parameters:
            with self.subTest(i=p):
                register_1 = cirq.LineQubit.range(0, p[0])
                register_2 = cirq.LineQubit.range(p[0], p[0] + p[1])
                expected = tuple(register_1 + register_2)
                test_instance = QPE(register_1, register_2, p[2])
                actual = test_instance.qubits
                self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
