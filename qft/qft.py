"""This module implements a simple QFT"""
from sympy import I,  pi, exp, ImmutableMatrix

from sympy.physics.quantum.gate import HadamardGate
from sympy.physics.quantum.gate import UGate, SwapGate, CGate


def qft(begin, end):
    """
    QFT implementation
    :param int begin: from bit begin
    :param int end: to bit end
    :return QFT circuit

    Example with 4 bits
    l0---------------o-----------o-------o---H--x---
    l1-----------o---|--------o--|---H--R2------|--x
    l2--------o--|---|----H--R2--R3-------------|--x
    l3----H--R2--R3--R4-------------------------x---
    """
    circuit = 1
    # we iterate in reverse order
    for line in reversed(range(begin, end)):
        # add the H gate
        circuit = HadamardGate(line) * circuit
        # Add rotate gates
        for i in range(line - begin):
            # start at n = i+2
            n = i + 2
            # create a rotation gate
            gate = UGate(line, ImmutableMatrix([[1, 0], [0, exp(2 * pi * I / (2 ** n))]]))
            # gate added under Control on line -i -1
            circuit = CGate(line - i - 1, gate) * circuit

    #  add swap gates
    for i in range((end - begin) // 2):
        circuit = SwapGate(i + begin, end - i - 1) * circuit
    return circuit


