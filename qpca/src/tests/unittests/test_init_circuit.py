import unittest
import cirq
from src.circuit.simple_qpca import SimpleSwapTestQPCA
from src.operation.swap_test import swap_test


class GetQubitsTestCase(unittest.TestCase):
    def runTest(self):
        pass

    def test_get_qubits_anchilla(self):
        test_instance = SimpleSwapTestQPCA()
        expected = [test_instance._anchilla]
        actual = test_instance.get_qubits('anchilla')
        self.assertEqual(expected, actual)

    def test_get_qubits_register_a(self):
        test_instance = SimpleSwapTestQPCA()
        expected = test_instance._register_a
        actual = test_instance.get_qubits('register_a')
        self.assertEqual(expected, actual)

    def test_get_qubits_register_b(self):
        test_instance = SimpleSwapTestQPCA()
        expected = test_instance._register_b
        actual = test_instance.get_qubits('register_b')
        self.assertEqual(expected, actual)

    def test_get_qubits_all(self):
        test_instance = SimpleSwapTestQPCA()
        expected = [test_instance._anchilla] + test_instance._register_a + test_instance._register_b
        actual = test_instance.get_qubits()
        self.assertEqual(expected, actual)


class InitCircuitTestCase(unittest.TestCase):
    def runTest(self):
        pass

    def test_all_qubits_have_different_qid(self):
        test_instance = SimpleSwapTestQPCA()
        expected = [0, 1, 2, 3, 4]
        actual = []
        qubits = test_instance.get_qubits()
        for qubit in qubits:
            actual.append(qubit.x)
        self.assertEqual(expected, actual)

    def test_both_registers_initialized_with_given_u_prep(self):
        parameters = [cirq.CNOT, cirq.SWAP]

        for p in parameters:
            with self.subTest(i=p):
                expected = cirq.Circuit(
                    p(cirq.LineQubit(1), cirq.LineQubit(2)), p(cirq.LineQubit(3), cirq.LineQubit(4))
                )
                test_instance = SimpleSwapTestQPCA(prep_operation=p)
                actual = test_instance[0:1]
                cirq.testing.assert_same_circuits(actual, expected)

    def test_has_diagram(self):
        circuit = SimpleSwapTestQPCA(prep_operation=cirq.SWAP)
        cirq.testing.assert_has_diagram(
            circuit,
            """
0: ───────SwapTest───
          │
1: ───×───#2─────────
      │   │
2: ───×───┼──────────
          │
3: ───×───#3─────────
      │
4: ───×────────────── 
            """,
        )

    def test_same_circuit(self):
        parameters = [cirq.CNOT, cirq.SWAP]

        for p in parameters:
            with self.subTest(i=p):
                expected = cirq.Circuit(
                    p(cirq.LineQubit(1), cirq.LineQubit(2)), p(cirq.LineQubit(3), cirq.LineQubit(4)),
                    swap_test(cirq.LineQubit(0), cirq.LineQubit(1), cirq.LineQubit(3))
                )

                actual = cirq.Circuit() + SimpleSwapTestQPCA(prep_operation=p)
                cirq.testing.assert_same_circuits(actual, expected)


if __name__ == '__main__':
    unittest.main()
