""" This module implements some utilities"""

from sympy.physics.quantum.qubit import Qubit
from sympy.physics.quantum.gate import HadamardGate


def get_qubit_size(q):
    """
    Returns a qubit size
    """
    if isinstance(q, Qubit):
        return q.nqubits
    for expr in q.args:
        for e in expr.args:
            if isinstance(e, Qubit):
                return e.nqubits
    return -1


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
