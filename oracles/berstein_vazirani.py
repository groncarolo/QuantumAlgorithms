""" This module implements Berstein-Vairani algorithm """
from sympy.physics.quantum.qapply import qapply
from sympy.physics.quantum.qubit import Qubit, matrix_to_qubit
from sympy.physics.quantum import TensorProduct
from sympy.physics.quantum.gate import HadamardGate
from sympy.physics.quantum.represent import represent

from oracles.oracle import oracle
from util.util import hn


def fbv(x, s):
    """
    Calculate dot product with XOR instead of SUM
    """
    r = 0
    for a, b in zip(x, s):
        r ^= a * b
    return r


def berstein_vazirani(s, n):
    """
    Run Berstein-Vazirani algorithm and return |x>*|y XOR f(x)>
    :param int s: bit string string
    :param int n: string length

    The problem:
    We have a function f {0,1}^n -> {0,1}
    f(x) = s dot x
    s is a n-bit string
    s dot x = s_n-1x_n-1 + ... + s1x1 + s0x0
    We want to find s = s_n-1...s1s0

    The Solution:
                         +-----------------+
      |x>  |0>-/n--H*n---|                 |--/n--H*n---M |x>
                         |       U_f       |
      |y>  |1>---H-------|                 |------------  |y XOR f(x)>
                         +-----------------+

    """
    x = qapply(hn(n) * Qubit('0' * n))
    print(f"|x>: {x}")
    y = qapply(HadamardGate(0) * Qubit(1))
    print(f"|y>: {y}")

    # calculate the Tensor Product of the inputs
    xy = TensorProduct(x, y)
    xy = matrix_to_qubit(represent(xy))
    print(f"|xy>: {xy}")

    # apply oracle
    r = oracle(x, y, fbv, s)

    # apply H*n on top Qubits
    r = qapply(hn(n, start=1) * r)
    return r
