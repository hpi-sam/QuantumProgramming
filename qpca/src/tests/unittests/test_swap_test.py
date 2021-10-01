import unittest
import cirq
from cirq.ops import raw_types

from src.operation.swap_test import SwapTestGate, swap_test


class SwapTestGateInitTestCase(unittest.TestCase):
    def runTest(self):
        self.test_is_gate()
        self.test_num_qubits()
        self.test_raises_value_error_on_wrong_number_of_qubits()

    def test_is_gate(self):
        test_instance = SwapTestGate(num_qubits=2)
        self.assertIsInstance(test_instance, raw_types.Gate)

    def test_num_qubits(self):
        parameters = [0, 2, -1]
        for p in parameters:
            with self.subTest(i=p):
                expected = max(0, p)
                test_instance = SwapTestGate(num_qubits=p)
                self.assertEqual(test_instance.num_qubits(), expected)

    def test_raises_value_error_on_wrong_number_of_qubits(self):
        test_instance = SwapTestGate(num_qubits=2)
        self.assertRaises(ValueError, test_instance, *cirq.LineQubit.range(0))


class SwapTestGateDecompositionTestCase(unittest.TestCase):
    def runTest(self):
        self.test_decompose_zero_qubits()
        self.test_decompose_raises_not_implemented_error_on_too_few_qubits()
        self.test_decompose_raises_not_implemented_error_on_states_with_different_register_length()
        self.test_circuit_diagram_three_qubits_circuit()
        self.test_circuit_diagram_five_qubits_circuit()
        self.test_circuit_diagram_five_qubits_circuit_register_length_two()

    def test_decompose_zero_qubits(self):
        test_instance = SwapTestGate(num_qubits=0)
        self.assertEqual(cirq.decompose_once(test_instance(*cirq.LineQubit.range(0))), [])

    def test_decompose_raises_not_implemented_error_on_too_few_qubits(self):
        parameters = [1, 2]
        for p in parameters:
            with self.subTest(i=p):
                test_instance = SwapTestGate(num_qubits=p)
                self.assertRaises(NotImplementedError, cirq.decompose_once, test_instance(*cirq.LineQubit.range(p)))

    def test_decompose_raises_not_implemented_error_on_states_with_different_register_length(self):
        parameters = [4, 6]
        for p in parameters:
            with self.subTest(i=p):
                test_instance = SwapTestGate(num_qubits=p)
                self.assertRaises(NotImplementedError, cirq.decompose_once, test_instance(*cirq.LineQubit.range(p)))

    def test_circuit_diagram_three_qubits_circuit(self):
        p = 3
        test_instance = SwapTestGate(num_qubits=p)
        cirq.testing.assert_has_diagram(
            cirq.Circuit(cirq.decompose_once(test_instance(*cirq.LineQubit.range(p)))),
            """
0: ───H───@───H───
          │
1: ───────×───────
          │
2: ───────×───────
            """,
        )

    def test_circuit_diagram_five_qubits_circuit(self):
        p = 5
        qubits = cirq.LineQubit.range(5)
        circuit = cirq.Circuit()
        for i in range(0, p):
            circuit.append(cirq.X(qubits[i]))

        test_instance = SwapTestGate(num_qubits=3)
        circuit.append(cirq.decompose_once(test_instance(*[qubits[1], qubits[2], qubits[4]])))

        cirq.testing.assert_has_diagram(
            circuit,
            """
0: ───X───────────────

1: ───X───H───@───H───
              │
2: ───X───────×───────
              │
3: ───X───────┼───────
              │
4: ───X───────×───────
            """,
        )

    def test_circuit_diagram_five_qubits_circuit_register_length_two(self):
        p = 5
        qubits = cirq.LineQubit.range(5)
        circuit = cirq.Circuit()
        for i in range(0, p):
            circuit.append(cirq.X(qubits[i]))

        test_instance = SwapTestGate(num_qubits=5)
        circuit.append(cirq.decompose_once(test_instance(*qubits)))

        cirq.testing.assert_has_diagram(
            circuit,
            """
0: ───X───H───@───@───H───
              │   │
1: ───X───────×───┼───────
              │   │
2: ───X───────┼───×───────
              │   │
3: ───X───────×───┼───────
                  │
4: ───X───────────×───────
            """,
        )


class SwapTestOperationTestCase(unittest.TestCase):
    def runTest(self):
        self.test_is_operation()
        self.test_circuit_diagram_on_three_qubits_circuit()
        self.test_circuit_diagram_on_five_qubits_circuit()

    def test_is_operation(self):
        self.assertIsInstance(swap_test(*cirq.LineQubit.range(3)), raw_types.Operation)

    def test_circuit_diagram_on_three_qubits_circuit(self):
        p = 3
        qubits = cirq.LineQubit.range(p)
        circuit = cirq.Circuit()
        circuit.append(cirq.decompose_once(swap_test(*qubits)))
        cirq.testing.assert_has_diagram(
            circuit,
            """
0: ───H───@───H───
          │
1: ───────×───────
          │
2: ───────×───────
            """,
        )

    def test_circuit_diagram_on_five_qubits_circuit(self):
        p = 5
        qubits = cirq.LineQubit.range(5)
        circuit = cirq.Circuit()
        for i in range(0, p):
            circuit.append(cirq.X(qubits[i]))

        circuit.append(cirq.decompose_once(swap_test(*[qubits[1], qubits[2], qubits[4]])))

        cirq.testing.assert_has_diagram(
            circuit,
            """
0: ───X───────────────

1: ───X───H───@───H───
              │
2: ───X───────×───────
              │
3: ───X───────┼───────
              │
4: ───X───────×───────
            """,
        )


class SwapTestGateStringRepresentationTestCase(unittest.TestCase):
    def runTest(self):
        self.test_str()

    def test_str(self):
        self.assertEqual('SwapTest', str(SwapTestGate()))


class SwapTestEquivalenceTestCase(unittest.TestCase):
    def runTest(self):
        pass

    def test_same_circuits(self):
        expected = cirq.Circuit(swap_test(cirq.LineQubit(0), cirq.LineQubit(1), cirq.LineQubit(2)))
        actual = cirq.Circuit(swap_test(cirq.LineQubit(0), cirq.LineQubit(1), cirq.LineQubit(2)))
        cirq.testing.assert_same_circuits(actual, expected)


if __name__ == '__main__':
    unittest.main()
