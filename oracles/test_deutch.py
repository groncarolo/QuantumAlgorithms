from deutch import deutch
from sympy.physics.quantum.qubit import Qubit, matrix_to_qubit
from sympy import sqrt
from sympy.physics.quantum import TensorProduct
from sympy.physics.quantum.represent import represent

def test_const_0():
    print()

    def f(x, *args):
        return 0

    r = deutch(f)
    print('\nResult const zero function: {r}'.format(r=r))

    truth = TensorProduct(Qubit(0), ((Qubit(0) - Qubit(1)) / sqrt(2)))
    truth = matrix_to_qubit(represent(truth))
    assert truth == r


def test_const_1():
    print()

    def f(x, *args):
        return 1

    r = deutch(f)
    print('\nResult const one function: {r}'.format(r=r))

    truth = TensorProduct(-Qubit(0), ((Qubit(0) - Qubit(1)) / sqrt(2)))
    truth = matrix_to_qubit(represent(truth))
    assert truth == r


def test_f_balanced_0():
    print()

    def f(x, *args):
        if x[0] == 0:
            return 1
        else:
            return 0

    r = deutch(f)
    print('\nResult balanced zero function: {r}'.format(r=r))

    truth = TensorProduct(-Qubit(1), ((Qubit(0) - Qubit(1)) / sqrt(2)))
    truth = matrix_to_qubit(represent(truth))
    assert truth == r


def test_f_balanced_1():
    print()

    def f(x, *args):
        if x[0] == 0:
            return 0
        else:
            return 1

    r = deutch(f)
    print('\nResult balanced one function: {r}'.format(r=r))

    truth = TensorProduct(Qubit(1), ((Qubit(0) - Qubit(1)) / sqrt(2)))
    truth = matrix_to_qubit(represent(truth))
    assert truth == r
