import cirq

from src.operation.swap_test import swap_test


class SimpleSwapTestQPCA(cirq.Circuit):
    def __init__(self, *contents: 'cirq.OP_TREE', prep_operation=None):
        super().__init__(*contents)
        self._anchilla = cirq.LineQubit(0)
        self._register_a = cirq.LineQubit.range(1, 3)
        self._register_b = cirq.LineQubit.range(3, 5)
        self._initialize_states(prep_operation)
        self.append(swap_test(self._anchilla, self._register_a[0], self._register_b[0]))

    def _initialize_states(self, prep_operation=None):
        if prep_operation is not None:
            self.append(prep_operation.on(*self._register_a))
            self.append(prep_operation.on(*self._register_b))

    def get_qubits(self, identifier: str = 'all'):
        qubits = []
        if identifier == 'anchilla' or identifier == 'all':
            qubits.append(self._anchilla)

        if identifier == 'register_a' or identifier == 'all':
            qubits += self._register_a

        if identifier == 'register_b' or identifier == 'all':
            qubits += self._register_b

        return qubits
