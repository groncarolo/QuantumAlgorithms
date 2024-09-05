import numpy as np
from sympy.physics.quantum.gate import HadamardGate
from sympy.physics.quantum.qapply import qapply
from sympy.physics.quantum.qubit import Qubit, measure_all


def get_random_bases():
    return np.random.choice(['X', 'Z'], size=(10,))


def get_random_bits():
    return np.random.choice([0, 1], size=(10,))


def get_random_alice_bits():
    return get_random_bits()


def get_random_alice_bases():
    return get_random_bases()


def get_random_bob_bases():
    return get_random_bases()


def bb84(get_alice_bits, get_alice_bases, get_bob_bases):
    # get bits and bases
    alice_bits = get_alice_bits()
    alice_bases = get_alice_bases()
    print("Alice bits: {bit}".format(bit=alice_bits))
    print("Alice bases: {bases}".format(bases=alice_bases))

    alice_sent = []
    for bit, base in zip(alice_bits, alice_bases):
        qubit = Qubit(bit)
        if base == 'X':
            qubit = qapply(HadamardGate(0) * qubit)
        alice_sent.append(qubit)
    print("Alice sent: {sent}".format(sent=alice_sent))

    bob_bases = get_bob_bases()
    print("Bob bases: {bases}".format(bases=bob_bases))

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


p_key, _ = bb84(get_random_alice_bits, get_random_alice_bases, get_random_bob_bases)
print("Private key: {key}".format(key=p_key))
