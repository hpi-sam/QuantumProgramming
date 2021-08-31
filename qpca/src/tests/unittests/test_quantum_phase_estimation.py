import unittest
import cirq
from cirq.ops import raw_types
from src.operation.quantum_phase_estimation import QPE


def get_test_data_2_times_1_x():
    return [2, 1, cirq.X, """
0: ───H───@───────────qft[norev]^-1───
          │           │
1: ───H───┼───@───@───#2──────────────
          │   │   │
2: ───────X───X───X───────────────────
        """]


def get_test_data_3_times_2_swap():
    return [3, 2, cirq.SWAP, """
0: ───H───@───────────────────────────qft[norev]^-1───
          │                           │
1: ───H───┼───@───@───────────────────#2──────────────
          │   │   │                   │
2: ───H───┼───┼───┼───@───@───@───@───#3──────────────
          │   │   │   │   │   │   │
3: ───────×───×───×───×───×───×───×───────────────────
          │   │   │   │   │   │   │
4: ───────×───×───×───×───×───×───×───────────────────
        """]


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
        parameter = [get_test_data_2_times_1_x, get_test_data_3_times_2_swap]

        for f in parameter:
            with self.subTest(i=f()):
                params = f()
                register_1 = cirq.LineQubit.range(params[0])
                register_2 = cirq.LineQubit.range(params[0], params[0] + params[1])
                circuit = cirq.Circuit()
                circuit.append(cirq.decompose_once(QPE(register_1, register_2, params[2])))
                cirq.testing.assert_has_diagram(circuit, params[3])


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
