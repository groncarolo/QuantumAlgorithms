from sympy.physics.quantum.qapply import qapply
from sympy.physics.quantum.qubit import Qubit, matrix_to_qubit
from sympy import sqrt, simplify
from sympy.physics.quantum import TensorProduct
from sympy.physics.quantum.gate import HadamardGate
from sympy.physics.quantum.represent import represent

from oracles.oracle import oracle


# Introduction to classical and quantum computing
# Exercise 7.3

def test_7_3():
    # consider a superposed state
    x = sqrt(3) / 2 * Qubit(0) + 1 / 2 * Qubit(1)
    print(f"|x>={x}")

    y = qapply(HadamardGate(0) * Qubit(1))
    print(f"|y>={y}")

    xy = TensorProduct(x, y)
    xy = matrix_to_qubit(represent(xy))
    print("|xy>={xy}".format(xy=xy))

    def f0(x, *args):
        return 0

    r = simplify(oracle(x, y, f0))
    print(f'Result for constant zero function: r={r}')
    solution = simplify(
        sqrt(3) / (2 * sqrt(2)) * (Qubit('00') - Qubit('01')) + 1 / (2 * sqrt(2)) * (Qubit('10') - Qubit('11')))
    assert simplify(r - solution) == 0

    def f1(x, *args):
        return 1

    r = oracle(x, y, f1)
    print(f'Result for constant one function: r={r}')
    solution = simplify(
        sqrt(3) / (2 * sqrt(2)) * (Qubit('01') - Qubit('00')) + 1 / (2 * sqrt(2)) * (Qubit('11') - Qubit('10')))
    assert simplify(r - solution) == 0


def test_phase():
    x = Qubit(0)
    print(f"|x>={x}")

    y = qapply(HadamardGate(0) * Qubit(1))
    print(f"|y>={y}")

    def f0(x, *args):
        return 0

    r = oracle(x, y, f0)
    print(r)

    truth = (-1) ** (f0(x)) * TensorProduct(x, y)
    truth = matrix_to_qubit(represent(truth))
    assert truth == r

    def f1(x, *args):
        return 1

    r = oracle(x, y, f1)
    print(r)

    truth = (-1) ** (f1(x)) * TensorProduct(x, y)
    truth = matrix_to_qubit(represent(truth))
    assert truth == r


def test_find_f0_f_const_0():
    # consider a superposed state
    x = Qubit(0)
    print(f"|x>={x}")

    y = Qubit(0)
    print(f"|y>={y}")

    def f(x, *args):
        return 0

    r = oracle(x, y, f)
    print(r)

    truth = TensorProduct(x, Qubit(f(0)))
    truth = matrix_to_qubit(represent(truth))
    assert truth == r

def test_find_f1_f_const_0():
    # consider a superposed state
    x = Qubit(1)
    print(f"|x>={x}")

    y = Qubit(0)
    print(f"|y>={y}")

    def f(x, *args):
        return 0

    r = oracle(x, y, f)
    print(r)

    truth = TensorProduct(x, Qubit(f(1)))
    truth = matrix_to_qubit(represent(truth))
    assert truth == r



def test_find_f0_f_const_1():
    # consider a superposed state
    x = Qubit(0)
    print(f"|x>={x}")

    y = Qubit(0)
    print(f"|y>={y}")

    def f(x, *args):
        return 1

    r = oracle(x, y, f)
    print(r)

    truth = TensorProduct(x, Qubit(f(0)))
    truth = matrix_to_qubit(represent(truth))
    assert truth == r

def test_find_f1_f_const_1():
    # consider a superposed state
    x = Qubit(1)
    print(f"|x>={x}")

    y = Qubit(0)
    print(f"|y>={y}")

    def f(x, *args):
        return 1

    r = oracle(x, y, f)
    print(r)

    truth = TensorProduct(x, Qubit(f(1)))
    truth = matrix_to_qubit(represent(truth))
    assert truth == r


def test_unitary_1():
    # consider a superposed state
    x = Qubit(1)
    print(f"|x>={x}")

    y = Qubit(0)
    print(f"|y>={y}")

    def f(x, *args):
        return 1

    r = oracle(x, y, f)
    print(r)

    truth = TensorProduct(x, Qubit(f(1)))
    truth = matrix_to_qubit(represent(truth))
    assert truth == r

    r = oracle(x, Qubit(f(1)), f)
    print(r)
    truth = TensorProduct(x, y)
    truth = matrix_to_qubit(represent(truth))
    assert truth == r

def test_unitary_2():
    # consider a superposed state
    x = Qubit(0)
    print(f"|x>={x}")

    y = qapply(HadamardGate(0) * Qubit(1))
    print(f"|y>={y}")

    def f(x, *args):
        return 1

    r = oracle(x, y, f)
    print(r)

    truth = TensorProduct((-1)**(f(x))*x, y)
    truth = matrix_to_qubit(represent(truth))
    assert truth == r

    r = oracle((-1)**(f(x))*x, y, f)
    print(r)
    truth = TensorProduct(x, y)
    truth = matrix_to_qubit(represent(truth))
    assert truth == r
