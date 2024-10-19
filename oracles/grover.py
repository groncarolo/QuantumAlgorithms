"""This module implements Grover algorithm"""
from sympy import sqrt, Mul
from sympy.physics.quantum.qapply import qapply
from sympy.physics.quantum.qubit import Qubit, matrix_to_qubit, measure_partial
from sympy.physics.quantum import TensorProduct
from sympy.physics.quantum.gate import HadamardGate
from sympy.physics.quantum.represent import represent
from util.util import hn, get_sub_state
from oracles.oracle import oracle


def inversion_about_mean(state):
    """
    calculate inversion about mean of input state

    :param state state: state for which we want the inversion
    """
    factors = []
    # get avg
    mean = 0
    for e in state.args:
        aa = [e for e in e.args if isinstance(e, Qubit) is False]
        factors.append(Mul(*aa))
        mean += Mul(*aa)
    mean = (mean / len(factors)).doit()

    # apply inversion about mean
    r = 0
    for s, f in zip(state.args, factors):
        aa = [e for e in s.args if isinstance(e, Qubit)]
        r += Mul(*aa, -f + 2 * mean)

    return r


def grover(f, n):
    """
    Run Grover algorithm and return |x>*|y XOR f(x)>
    :param func f: oracle function
    :param int n: string length

    The problem:
    Given a function f {0, 1}^n -> {0, 1} that we can evaluate
    The oracle takes as input Qubits |x> and|y>
    and returns |x, y XOR f(x)>

    The solution:
                        +--------------------------------------------------------+
                        |   sqrt(2**n) times                                     |
                        |            +-----------------+         +---------+     |
      |x>  |0>-/n--H*n--|------------|                 |---\n----| -I - 2A |--\n-|----M
                        |            |       U_f       |         +---------+     |
      |y>               |  |1>---H---|                 |------- |y XOR f(x)>     |
                        |            +-----------------+                         |
                        +--------------------------------------------------------+
    We obtain a high probability on the input chosen by f
    """
    # apply H*n gate to |x>
    x = qapply(hn(n) * Qubit('0' * n))
    print(f"|x>: {x}")

    # iterate over phase inversion block
    for i in range(int(sqrt(2 ** n))):
        print(f"\nIter {i}")
        y = qapply(HadamardGate(0) * Qubit(1))
        print(f"|y>: {y}")

        xy = TensorProduct(x, y)
        xy = matrix_to_qubit(represent(xy))
        print(f"|xy>: {xy}")

        # apply oracle
        state = oracle(x, y, f)

        # we measure the y bit
        measure = measure_partial(state, (0,))

        # get x component of the tensor product, remove y
        x = get_sub_state(measure[0][0], 0, n)

        x = inversion_about_mean(x)
        print(f"|x>: {x}")
    return x
