from sympy.physics.quantum.qapply import qapply
from sympy.physics.quantum.qubit import Qubit, IntQubit, matrix_to_qubit, measure_all, measure_partial
from sympy.physics.quantum import TensorProduct
from sympy.physics.quantum.gate import HadamardGate
from sympy.physics.quantum.represent import represent
from util import hn
from oracle import oracle
from sympy import sqrt, simplify, preorder_traversal, Rational, Mul


# This code implements Deutch algorithm
# The problem:
# Given a function f {0, 1}^n -> {0, 1} that we can evaluate
# The oracle takes as input Qubits |x> and|y>
# and returns |x, y XOR f(x)>
#
#                     +--------------------------------------------------------+
#                     |   sqrt(2**n) times                                     |
#                     |            +-----------------+         +---------+     |
#   |x>  |0>-/n--H*n--|------------|                 |---\n----| -I - 2A |--\n-|----M
#                     |            |       U_f       |         +---------+     |
#   |y>               |  |1>---H---|                 |------- |y XOR f(x)>     |
#                     |            +-----------------+                         |
#                     +--------------------------------------------------------+


def get_x_component(state):
    # we measure the y bit
    m = measure_partial(state, (0,))
    state = 0

    # create a new state without y qubit
    for expr in m[0][0].args:
        ee = 1
        for e in expr.args:
            if isinstance(e, Qubit):
                qbit = e
            else:
                ee *= e
        # throw y part and just keep x
        state += ee * Qubit(*qbit.qubit_values[0:qbit.dimension - 1])
    return state


def inversion_about_mean(state):
    factors = []
    # get avg
    avg = 0
    for e in state.args:
        aa = [e for e in e.args if isinstance(e, Qubit) is False]
        factors.append(Mul(*aa))
        avg += Mul(*aa)
    avg = (avg / len(factors)).doit()

    # get inversion about mean and apply
    r = 0
    for s, f in zip(state.args, factors):
        aa = [e for e in s.args if isinstance(e, Qubit)]
        r += Mul(*aa, -f + 2 * avg)

    return r


def grover(f, n):
    # apply H*n gate to |x>
    x = qapply(hn(n) * Qubit('0' * n))
    print("|x>: {x}".format(x=x))

    # iterate over phase inversion block
    for iter in range(int(sqrt(2 ** n))):
        print("\nIter {i}".format(i=iter))
        y = qapply(HadamardGate(0) * Qubit(1))
        print("|y>: {y}".format(y=y))

        xy = TensorProduct(x, y)
        xy = matrix_to_qubit(represent(xy))
        print("|xy>: {xy}".format(xy=xy))

        # apply oracle
        state = oracle(x, y, f)

        # get x component of the tensor product
        x = get_x_component(state)

        x = inversion_about_mean(x)
        print("|x>: {x}".format(x=x))

    return x
