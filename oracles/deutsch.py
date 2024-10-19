""" This mudule implements Deutsch algorithm """
from sympy.physics.quantum.qapply import qapply
from sympy.physics.quantum.qubit import Qubit, matrix_to_qubit
from sympy.physics.quantum import TensorProduct
from sympy.physics.quantum.gate import HadamardGate
from sympy.physics.quantum.represent import represent

from oracles.oracle import oracle



def deutsch(f):
    """
    Run Deutsch algorithm and return |x>*|y XOR f(x)>
    :param func f: oracle function

    The problem:
    Given a function f {0, 1} -> {0, 1} that we can evaluate
    but is unknown to us determine if it is balanced or
    constant
    The oracle takes as input Qubits |x> and|y>
    and returns |x, y XOR f(x)>

    The Solution:
                     +-----------------+
      |x>  |0>---H---|                 |---H--M |x>
                     |       U_f       |
      |y>  |1>---H---|                 |------   |y XOR f(x)>
                     +-----------------+
    Constant zero -> +|0>*|->
    Constant  one -> -|0>*|->
    Balanced 0->1 -> +|1>*|->
    Balanced 1->0 -> -|1>*|->

    """
    # apply H gate to both inputs
    x = qapply(HadamardGate(0) * Qubit(0))
    print(f"|x>={x}")
    y = qapply(HadamardGate(0) * Qubit(1))
    print(f"|y>={y}")

    # calculate the Tensor Product of the inputs
    xy = TensorProduct(x, y)
    xy = matrix_to_qubit(represent(xy))
    print(f"|xy>={xy}")

    # apply oracle
    r = oracle(x, y, f)

    # apply H on top Qubit
    return qapply(HadamardGate(1) * r)
