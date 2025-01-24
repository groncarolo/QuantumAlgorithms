import numpy as np
from sympy import sqrt, I
from sympy import preorder_traversal
from sympy.physics.quantum.qubit import Qubit
from sympy.physics.quantum.gate import HadamardGate
from sympy.physics.quantum.dagger import Dagger
from sympy.physics.quantum import Bra, Ket, qapply

plus = Qubit(0) / sqrt(2) + Qubit(1) / sqrt(2)
minus = Qubit(0) / sqrt(2) - Qubit(1) / sqrt(2)
zero = Qubit(0)
one = Qubit(1)
i_state = Qubit(0) / sqrt(2) + I * Qubit(1) / sqrt(2)
i_minus_state = Qubit(0) / sqrt(2) - I * Qubit(1) / sqrt(2)
unkn = "-"


def get_random_bases(size=10):
    """
    Get a collection of size random bases between X and Z

    :param int size: number of bases
    """
    return np.random.choice(["X", "+"], size=(size,))


def get_random_bits(size=10):
    """
    Get a collection of size random bits

    :param int size: number of bits
    """
    return np.random.choice([0, 1], size=(size,))


def get_qubit_size(q):
    """
    Returns a qubit size
    """
    for arg in preorder_traversal(q):
        if isinstance(arg, Qubit):
            return arg.nqubits


def hn(n, start=0):
    """
    Get a H*n state
    """
    ret = 1
    for i in range(start, start + n):
        ret = ret * HadamardGate(i)
    return ret


def get_sub_state(state, start, stop):
    """
    Returns a substate
    """
    if isinstance(state, Qubit):
        return Qubit(*state.qubit_values[start:stop])

    ret = 0
    for expr in state.args:
        ee = 1
        for e in expr.args:
            if isinstance(e, Qubit):
                qbit = e
            else:
                ee *= e
        # throw y part and just keep x
        ret += ee * Qubit(*qbit.qubit_values[start:stop])
    return ret


def change_basis(q, new_base):
    a = qapply(Dagger(new_base[0]) * q) * Qubit("0")
    b = qapply(Dagger(new_base[1]) * q) * Qubit("1")

    return a + b
