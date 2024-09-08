from deutsch import deutsch
from sympy.physics.quantum.qubit import Qubit, matrix_to_qubit
from sympy import sqrt
from sympy.physics.quantum import TensorProduct
from sympy.physics.quantum.represent import represent

def test_const_0():
    print()

    def f(x):
        return 0

    r = deutsch(f)
    print(f'\nResult const zero function: {r}')

    truth = TensorProduct(Qubit(0), ((Qubit(0) - Qubit(1)) / sqrt(2)))
    truth = matrix_to_qubit(represent(truth))
    assert truth == r


def test_const_1():
    print()

    def f(x):
        return 1

    r = deutsch(f)
    print(f'\nResult const one function: {r}')

    truth = TensorProduct(-Qubit(0), ((Qubit(0) - Qubit(1)) / sqrt(2)))
    truth = matrix_to_qubit(represent(truth))
    assert truth == r


def test_f_balanced_0():
    print()

    def f(x):
        if x[0] == 0:
            return 1
        else:
            return 0

    r = deutsch(f)
    print(f'\nResult balanced zero function: {r}')

    truth = TensorProduct(-Qubit(1), ((Qubit(0) - Qubit(1)) / sqrt(2)))
    truth = matrix_to_qubit(represent(truth))
    assert truth == r


def test_f_balanced_1():
    print()

    def f(x):
        if x[0] == 0:
            return 0
        else:
            return 1

    r = deutsch(f)
    print(f'\nResult balanced one function: {r}')

    truth = TensorProduct(Qubit(1), ((Qubit(0) - Qubit(1)) / sqrt(2)))
    truth = matrix_to_qubit(represent(truth))
    assert truth == r
