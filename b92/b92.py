"""Module providing B92 code

Two non-orthogonal bases
+ = {|→>,|↑>} = {[1,0]T, [0,1]T}
X = {|↖>,|↗>} = {1/sqtr(2)[-1,1]T, 1/sqtr(2)[1,1]T}

state  +      X
|0>    |→>   |↖>
|1>    |↑>   |↗>

we use a non-orthogonal base
{|→>, |↗>} = {zero, plus}
"""
from sympy.physics.quantum import qapply
from sympy.physics.quantum.gate import HadamardGate
from sympy.physics.quantum.qubit import measure_all, Qubit

from util.measure_all import measure_all_oneshot
from util.util import zero

def find_ones(bob_bits):
    """
    :param bob_bits: Bob bits
    :return list of indexes where bob_bits are one
    """
    indices = []
    for i in range(len(bob_bits)):
        if bob_bits[i] == Qubit(1):
            indices.append(i)
    return indices

def b92_alice_part(alice_bits):
    """
    :param alice_bits: Alice bits
    :return alice_sent: alice measured qubits
    """

    # get bits and bases Alice side
    print(f"Alice bits: {alice_bits}")

    # we use a non-orthogonal base
    # {|→>, |↗>} = {zero, plus}
    alice_sent = [qapply(HadamardGate(0) * Qubit(0)) if b == 1 else zero for b in alice_bits]

    print(f"Alice sent: {alice_sent}")
    return alice_sent


def b92_bob_part(bob_bases, alice_sent):
    """
    :param func bob_bases: function Bob bases
    :param qubit list alice_sent: alice measured qubits (might have been eavesdropped)
    return measures: bob measured bits
    """
    bob_bases = ['Z' if b == 0 else 'X' for b in bob_bases]
    print(f"Bob bases: {bob_bases}")

    measures = []
    for q, bb in zip(alice_sent, bob_bases):
        qq = q
        if bb == 'X':
            # base change
            qq = qapply(HadamardGate(0) * q)
        m = measure_all_oneshot(qq)
        measures.append(m)
    return measures


def b92(alice_bits,bob_bases):
    """
    Run B92 algorithm and return a private key

    :param func alice_bits: Alice bits
    :param func bob_bases: Bob bases
    """
    alice_sent = b92_alice_part(alice_bits)
    bob_measures = b92_bob_part(bob_bases, alice_sent)
    print(f"bob measures={bob_measures}")

    bob_one_indices = find_ones(bob_measures)
    print(f"bob_one_indices={bob_one_indices}")

    key_alice = []
    for i in bob_one_indices:
        key_alice.append(1 - alice_bits[i])
    print(f"alice key={key_alice}")

    key_bob = []
    for i in bob_one_indices:
        key_bob.append(bob_bases[i])
    print(f"bob key={key_bob}")
    return key_alice, key_bob
