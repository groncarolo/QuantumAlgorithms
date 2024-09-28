"""Module providing BB84 code"""

import numpy as np
from sympy.physics.quantum.gate import HadamardGate
from sympy.physics.quantum.qapply import qapply
from sympy.physics.quantum.qubit import Qubit
from measure_all import measure_all_oneshot


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


def bb84(get_alice_bits, get_alice_bases, get_bob_bases, gen_bit_size=10, eavesdropping=False, check_size=0):
    """
    Run BB84 algorithm and return a private key

    :param func get_alice_bits: function that returns Alice bits
    :param func get_alice_bases: function that returns Alice bases
    :param func get_bob_bases: function that returns Bob bases
    :param int gen_bit_size: how many bit we want to generate
    :param Bool eavesdropping: simulate Eve eavesdropping
    :param int check_size: how many bit of the key should be used to check eavesdropping


    To make sure Eve did not eavesdrop Alice and Bob can generate
    say 256 + 50 bits and share the 50 additional bits

    Supposing Alice and Bob reveals 50 bits we can calculate the probability
    they have to catch Eve eavesdropping
                           Eve  ----------------- Bob     0.5 undetected
                    0.5 /  Z, |0>                 Z,|0>
    Alice   ---> Eve -
    Z, |0>             \             ------------ Bob
                    0.5 \          / 0.5          Z,|0>   0.25 undetcted
                         \        /
                          Eve---------
                          X, |+>,|->  \
                                       --------- Bob
                                                 Z,|1>   0.25 Detected
    On n bit the probability the Eve is not detected is
    1 - (3/4)**n
    """
    # get bits and bases Alice side
    alice_bits = get_alice_bits(gen_bit_size)
    alice_bases = get_alice_bases(gen_bit_size)
    print(f"Alice bits: {alice_bits}")
    print(f"Alice bases: {alice_bases}")

    alice_sent = []
    for bit, base in zip(alice_bits, alice_bases):
        qubit = Qubit(bit)
        if base == 'X':
            qubit = qapply(HadamardGate(0) * qubit)
        alice_sent.append(qubit)
    alice_sent = alice_sent
    print(f"Alice sent: {alice_sent}")

    if eavesdropping:
        eve_bases = get_random_bases(gen_bit_size)
        eavesdropped = []
        for q, bb in zip(alice_sent, eve_bases):
            qq = q
            # change base if needed
            if bb == 'X':
                qq = qapply(HadamardGate(0) * q)

            m = measure_all_oneshot(qq)
            eavesdropped.append(m)

        # measuring changes what alice_sent
        alice_sent = eavesdropped

    bob_bases = get_bob_bases(gen_bit_size)
    print(f"Bob bases: {bob_bases}")

    private_key = []

    for q, bb in zip(alice_sent, bob_bases):
        qq = q
        # change base if needed
        if bb == 'X':
            qq = qapply(HadamardGate(0) * q)

        m = measure_all_oneshot(qq)
        private_key.append(m)

    # match bases
    for ab, bb, i in zip(alice_bases, bob_bases, range(gen_bit_size)):
        # if Alice and Bob bases match
        # than the measure is good
        if bb != ab:
            private_key[i] = '-'

    pk_size = sum(1 for x in private_key if x != '-')

    print(f"private_key {private_key} size:{pk_size}")

    eavesdropped = 0
    if eavesdropping:
        eavesdropped = 0
        for pk, al in zip(private_key, alice_bits):
            # the bases have to match
            if pk != '-':
                check_size -= 1
                # the values too
                if pk != Qubit(al):
                    eavesdropped += 1
            if check_size == 0:
                break

    return private_key, alice_sent, eavesdropped
