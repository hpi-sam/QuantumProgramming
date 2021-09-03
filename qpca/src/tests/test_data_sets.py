import cirq
import numpy as np


class BaseDataSet(object):
    def __init__(self):
        self._expected = None

    @property
    def expected(self):
        return self._expected


class BaseExampleDataSetQPE(BaseDataSet):
    def __init__(self, len_count, len_eigen, operation, eigenstate, expected):
        super().__init__()
        self._len_count_reg = len_count
        self._len_eigenstate_reg = len_eigen
        self._count_reg = cirq.LineQubit.range(0, self._len_count_reg)
        self._eigenstate_reg = cirq.LineQubit.range(self._len_count_reg, self._len_count_reg + self._len_eigenstate_reg)
        self._operation = operation
        self._str_diagram = ""
        self._eigenstate = eigenstate
        self._expected = expected

    def get_all_registers(self):
        return [self._count_reg, self._eigenstate_reg]

    @property
    def count_register(self):
        return self._count_reg

    @property
    def eigenstate_register(self):
        return self._eigenstate_reg

    @property
    def operation(self):
        return self._operation

    @property
    def eigenstate(self):
        return self._eigenstate

    def get_str_diagram(self):
        return self._str_diagram

    def get_test_data_array(self):
        return [self._len_count_reg, self._len_eigenstate_reg, self._operation, self._str_diagram]


class ExampleDataSetRef19(BaseExampleDataSetQPE):
    def __init__(self):
        x = np.array([4, 3, 4, 4, 3, 3, 3, 3, 4, 4, 4, 5, 4, 3, 4])
        y = np.array([3028, 1365, 2726, 2538, 1318, 1693, 1412, 1632, 2875, 3564, 4412, 4444, 4278, 3064, 3857]) / 1000
        self._matrix = np.array([x, y])
        self._sigma = np.cov(self._matrix)
        self._normed_covariance = self._sigma / np.trace(self._sigma)
        self._purity = np.trace(np.matmul(self._normed_covariance, self._normed_covariance))
        self._e1 = 1.57286
        self._e2 = 0.105029

        super().__init__(4, 2, None, None, 1 / 3)
        self._eigenstate = self._compute_eigenstate()
        self._operation = self._compute_operation()
        self._expected = [self._e1, self._e2]
        self._str_diagram = ""

    def _compute_eigenstate(self):
        U, S, V = np.linalg.svd([self._normed_covariance])
        # print(U)
        # print(S)
        # print(V)
        # U, S, V = np.linalg.svd(self._density_matrix)
        # B = 1/np.sqrt(S[0]**2 + S[1]**2) * np.array([S[0], S[1]])
        B = np.sqrt(S)
        B = (np.sqrt(S) * np.identity(2))
        # print(B, np.identity(2))
        theta = 2 * np.arccos(S[0])
        print(U, np.linalg.inv(U))
        # print(B, np.matmul(B, np.linalg.inv(B)))
        # print(V, V[0][0]**2 + V[1][1]**2)
        circuit = cirq.Circuit()
        # circuit.append(cirq.MatrixGate(np.linalg.inv(U))(self._eigenstate_reg[0]))
        circuit.append(cirq.CNOT(self._eigenstate_reg[0], self._eigenstate_reg[1]))
        circuit.append(cirq.MatrixGate(U)(self._eigenstate_reg[0]))
        circuit.append(cirq.MatrixGate(V)(self._eigenstate_reg[1]))
        # print(circuit)
        return circuit

    def _compute_operation(self):
        U, S, V = np.linalg.svd(self._matrix)
        matrix = np.matmul(np.array([[1, 0], [0, np.exp(2j * S[0])]]), np.array([[1, 0], [0, np.exp(2j * S[1])]]))
        return cirq.MatrixGate(matrix)

    def get_features(self):
        return self._matrix[0], self._matrix[1]

    def get_sigma(self):
        return self._sigma

    def get_purity(self):
        return self._purity


class ExampleDataSetMain(BaseExampleDataSetQPE):
    def __init__(self):
        self._matrix = np.array([[1.5, 0.5], [0.5, 1.5]])
        self._sigma = np.cov(self._matrix)
        normed_covariance = self._sigma / np.trace(self._sigma)
        self._purity = np.trace(np.matmul(normed_covariance, normed_covariance))
        self._density_matrix = np.matmul(normed_covariance, normed_covariance)
        self._e1 = 2
        self._e2 = 1

        super().__init__(4, 2, None, None, 1 / 3)
        self._eigenstate = self._compute_eigenstate()
        self._operation = self._compute_operation()
        self._expected = [self._e1, self._e2]
        self._str_diagram = ""

    def _compute_eigenstate(self):
        U, S, V = np.linalg.svd([self._matrix])
        # U, S, V = np.linalg.svd(self._density_matrix)
        # B = 1/np.sqrt(S[0]**2 + S[1]**2) * np.array([S[0], S[1]])
        B = np.diag(S)
        #print(B, np.matmul(B, np.linalg.inv(B)))
        # print(V, V[0][0]**2 + V[1][1]**2)
        circuit = cirq.Circuit()
        circuit.append(cirq.MatrixGate(np.linalg.inv(U))(self._eigenstate_reg[0]))
        circuit.append(cirq.CNOT(self._eigenstate_reg[0], self._eigenstate_reg[1]))
        circuit.append(cirq.MatrixGate(U)(self._eigenstate_reg[0]))
        circuit.append(cirq.MatrixGate(V)(self._eigenstate_reg[1]))
        # print(circuit)
        return circuit

    def _compute_operation(self):
        U, S, V = np.linalg.svd(self._matrix)
        matrix = np.matmul(np.array([[1, 0], [0, np.exp(2j * S[0])]]), np.array([[1, 0], [0, np.exp(2j * S[1])]]))
        return cirq.MatrixGate(matrix)

    def get_features(self):
        return self._matrix[0], self._matrix[1]

    def get_sigma(self):
        return self._sigma

    def get_purity(self):
        return self._purity


class ExampleDataSetQiskitTextbookTGate3CountQubits(BaseExampleDataSetQPE):
    def __init__(self):
        super().__init__(3, 1, cirq.T, None, 1 / 8)
        self._eigenstate = self._compute_eigenstate()
        self._str_diagram = """
0: ───H───@───────────────────────────qft[norev]^-1───
          │                           │
1: ───H───┼───@───@───────────────────#2──────────────
          │   │   │                   │
2: ───H───┼───┼───┼───@───@───@───@───#3──────────────
          │   │   │   │   │   │   │
3: ───X───T───T───T───T───T───T───T───────────────────
        """
        self._expected = 1 / 8

    def _compute_eigenstate(self):
        return cirq.Circuit(cirq.X(*self._eigenstate_reg))


class ExampleDataSetQiskitTextbookPGate5CountQubits(BaseExampleDataSetQPE):
    def __init__(self, angle=2 * np.pi / 3):
        super().__init__(5, 1, self._compute_operation(angle), None, 1 / 3)
        self._eigenstate = self._compute_eigenstate()
        self._str_diagram = """
0: ───H───@───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────qft[norev]^-1───
          │                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   │
1: ───H───┼───────────────────────────@───────────────────────────@───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────#2──────────────
          │                           │                           │                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           │
2: ───H───┼───────────────────────────┼───────────────────────────┼───────────────────────────@───────────────────────────@───────────────────────────@───────────────────────────@───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────#3──────────────
          │                           │                           │                           │                           │                           │                           │                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           │
3: ───H───┼───────────────────────────┼───────────────────────────┼───────────────────────────┼───────────────────────────┼───────────────────────────┼───────────────────────────┼───────────────────────────@───────────────────────────@───────────────────────────@───────────────────────────@───────────────────────────@───────────────────────────@───────────────────────────@───────────────────────────@───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────#4──────────────
          │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           │
4: ───H───┼───────────────────────────┼───────────────────────────┼───────────────────────────┼───────────────────────────┼───────────────────────────┼───────────────────────────┼───────────────────────────┼───────────────────────────┼───────────────────────────┼───────────────────────────┼───────────────────────────┼───────────────────────────┼───────────────────────────┼───────────────────────────┼───────────────────────────@───────────────────────────@───────────────────────────@───────────────────────────@───────────────────────────@───────────────────────────@───────────────────────────@───────────────────────────@───────────────────────────@───────────────────────────@───────────────────────────@───────────────────────────@───────────────────────────@───────────────────────────@───────────────────────────@───────────────────────────@───────────────────────────#5──────────────
          │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │                           │
          ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐   ┌                       ┐
5: ───X───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───│ 1. +0.j     0. +0.j   │───────────────────
          │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│   │ 0. +0.j    -0.5+0.866j│
          └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘   └                       ┘
        """

    def _compute_eigenstate(self):
        return cirq.Circuit(cirq.X(*self._eigenstate_reg))

    def _compute_operation(self, angle):
        matrix = np.array([[1, 0], [0, np.exp(1j * angle)]])
        return cirq.MatrixGate(matrix)


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
