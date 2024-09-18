""" This module implements some utilities"""

from sympy import preorder_traversal
from sympy.physics.quantum.qubit import Qubit
from sympy.physics.quantum.gate import HadamardGate


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
