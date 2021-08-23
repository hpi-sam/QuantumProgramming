import cirq
from cirq.ops import raw_types


class SwapTestGate(raw_types.Gate):
    def __init__(self, num_qubits=3):
        self._num_qubits = max(0, num_qubits)

    def num_qubits(self) -> int:
        return self._num_qubits

    def _decompose_(self, qubits):
        if len(qubits) == 0:
            return

        if len(qubits) < 3 or (len(qubits) - 1) % 2 != 0:
            raise NotImplementedError

        start_index_first_reqister = 1
        start_index_second_reqister = (len(qubits) + 1) // 2

        yield cirq.H(qubits[0])
        for i in range(start_index_first_reqister, start_index_second_reqister):
            yield cirq.SWAP(qubits[i], qubits[start_index_second_reqister - 1 + i]).controlled_by(qubits[0])
        yield cirq.H(qubits[0])

    def __str__(self) -> str:
        return 'SwapTest'


def swap_test(*qubits: 'cirq.Qid') -> 'cirq.Operation':
    result = SwapTestGate(len(qubits)).on(*qubits)
    return result


def compute_swap_test_probability(repetitions, result_data):
    result = 1 - 1/repetitions * (result_data[0] * 0 + result_data[1] * 1)
    return result
