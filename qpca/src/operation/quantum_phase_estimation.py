from typing import Tuple, Sequence, Union
import cirq
from cirq.ops import raw_types
from cirq.ops.raw_types import TSelf


class QPE(raw_types.Operation):
    def __init__(self, count_register: Sequence['cirq.Qid'], eigenstate_register: Sequence['cirq.Qid'],
                 unitary_operation: Union['cirq.Gate', 'cirq.Operation']):
        unitary_operation.validate_args(eigenstate_register)
        self._validate_register_length(count_register)
        self._validate_register_length(eigenstate_register)
        self._operation = unitary_operation
        self._count_register = tuple(count_register)
        self._eigenstate_register = tuple(eigenstate_register)

    def with_qubits(self: TSelf, *new_qubits: 'cirq.Qid') -> TSelf:
        raise NotImplementedError

    @property
    def qubits(self) -> Tuple['cirq.Qid', ...]:
        return self._count_register + self._eigenstate_register

    @property
    def unitary_operation(self) -> 'cirq.Operation':
        return self._operation

    def _validate_register_length(self, qubits: Sequence['cirq.Qid']):
        if len(qubits) <= 0:
            raise ValueError

    def _decompose_(self):
        yield self._apply_superposition()
        yield self._apply_unitary_operation()
        yield self._apply_inverse_qft()

    def _apply_superposition(self):
        for qubit in self._count_register:
            yield cirq.H(qubit)

    def _apply_unitary_operation(self):
        repetitions = 1
        for qubit in self._count_register:
            for j in range(repetitions):
                yield self._operation.on(*self._eigenstate_register).controlled_by(qubit)
            repetitions *= 2

    def _apply_inverse_qft(self):
        yield cirq.inverse(cirq.qft(*self._count_register, without_reverse=True))
