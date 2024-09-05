"""Module providing BB84 code"""

import numpy as np
from sympy.physics.quantum.gate import HadamardGate
from sympy.physics.quantum.qapply import qapply
from sympy.physics.quantum.qubit import Qubit, measure_all


def get_random_bases(size=10):
    """
    Get a collection of size random bases between X and Z

    :param int size: number of bases
    """
    return np.random.choice(['X', 'Z'], size=(size,))


def get_random_bits(size=10):
    """
    Get a collection of size random bits

    :param int size: number of bits
    """
    return np.random.choice([0, 1], size=(size,))


def bb84(get_alice_bits, get_alice_bases, get_bob_bases):
    """
    Run BB84 algorithm and return a private key

    :param func get_alice_bits: function that returns Alice bits
    :param func get_alice_bases: function that returns Alice bases
    :param func get_bob_bases: function that returns Bob bases
    """
    # get bits and bases Alice side
    alice_bits = get_alice_bits()
    alice_bases = get_alice_bases()
    print(f"Alice bits: {alice_bits}")
    print(f"Alice bases: {alice_bases}")

    alice_sent = []
    for bit, base in zip(alice_bits, alice_bases):
        qubit = Qubit(bit)
        if base == 'X':
            qubit = qapply(HadamardGate(0) * qubit)
        alice_sent.append(qubit)
    print(f"Alice sent: {alice_sent}")

    bob_bases = get_bob_bases()
    print(f"Bob bases: {bob_bases}")

    private_key = []

    for q, bb, ab in zip(alice_sent, bob_bases, alice_bases):
        qq = q
        # change base if needed
        if bb == 'X':
            qq = qapply(HadamardGate(0) * q)

        # if Alice and Bob bases match
        # and the measure to the private key
        if bb == ab:
            m = measure_all(qq)
            private_key.append(m[0][0])
        else:
            private_key.append('-')

    return private_key, alice_sent
