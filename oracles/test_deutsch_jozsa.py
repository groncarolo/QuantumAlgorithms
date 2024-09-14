from sympy.physics.quantum.qapply import qapply
from sympy.physics.quantum.qubit import Qubit, IntQubit, matrix_to_qubit, measure_partial
from sympy import sqrt
from sympy.physics.quantum import TensorProduct
from sympy.physics.quantum.represent import represent

from oracle import oracle
from deutsch_jozsa import deutsch_jozsa


def test_const_0():
    print()

    def f(x, *args):
        return 0

    n = 3
    r = deutsch_jozsa(f, n)
    print(f'\nResult const zero function: {r}')

    truth = TensorProduct(Qubit('0' * n), 1 / sqrt(2) * (Qubit(0) - Qubit(1)))
    truth = matrix_to_qubit(represent((truth)))
    assert truth == r


def test_const_1():
    print()

    def f(x, *args):
        return 1

    n = 3
    r = deutsch_jozsa(f, n)
    print(f'\nResult const one function: {r}')

    truth = TensorProduct(-1 * Qubit('0' * n), 1 / sqrt(2) * (Qubit(0) - Qubit(1)))
    truth = matrix_to_qubit(represent(truth))
    assert truth == r


def test_f_balanced():
    print()

    def f(x, *args):
        q = IntQubit(*x)
        if q.as_int() % 2 == 0:
            return 1
        else:
            return 0

    n = 3
    r = deutsch_jozsa(f, n)
    print(f'\nResult balanced zero function: {r}')
    truth_0 = TensorProduct(Qubit('0' * n), 1 / sqrt(2) * (Qubit(0) - Qubit(1)))
    truth_0 = matrix_to_qubit(represent((truth_0)))
    truth_1 = TensorProduct(-1 * Qubit('0' * n), 1 / sqrt(2) * (Qubit(0) - Qubit(1)))
    truth_1 = matrix_to_qubit(represent(truth_1))

    assert r != truth_0 and r != truth_1
