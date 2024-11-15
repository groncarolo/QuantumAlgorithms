""" This module implements Deutch_Jozsa algorithm """
from sympy.physics.quantum.qapply import qapply
from sympy.physics.quantum.qubit import Qubit, matrix_to_qubit
from sympy.physics.quantum import TensorProduct
from sympy.physics.quantum.gate import HadamardGate
from sympy.physics.quantum.represent import represent

from oracles.oracle import oracle
from util.util import hn


def deutsch_jozsa(f, n):
    """
    Run  Deutsch Jozsa algorithm and return |x>*|y XOR f(x)>
    :param func f: oracle function
    :param int n: string length

    The problem:
    This is a generalization of Deutsch algorithm
    consider f {0,1}^n  -> f {0, 1}^n that is not known
    determine if f is balanced or constant
    where f is
    balanced if exactly half of the input go to zero ( and the other half to one)
    constant if all input go to zero OR all got to one

    The Solution:
                         +-----------------+
      |x>  |0>-/n--H*n---|                 |--/n--H*n---M |x>
                         |       U_f       |
      |y>  |1>---H-------|                 |------------  |y XOR f(x)>
                         +-----------------+

    Constant zero -> +|0*n>*|->
    Constant  one -> -|0*n>*|->
    Balanced 0->1 ->  NOT (+|0*n>*|->) and NOT (-|0*n>*|->)
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
    r = oracle(x, y, f)

    # apply H*n on top Qubits
    r = qapply(hn(n, start=1) * r)
    return r
