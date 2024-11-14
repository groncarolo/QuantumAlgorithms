from random import getrandbits
from sympy.physics.quantum.qubit import Qubit
from b92.b92 import b92


def get_alice_bits(size):
    bits = []
    for i in range(size):
        bits.append(getrandbits(1))
    return bits


def get_bob_bases(size):
    bases = []
    for i in range(size):
        bases.append(getrandbits(1))
    return bases




def test_b92():
    print()
    size = 64
    alice_bits = get_alice_bits(size)
    bob_bases = get_bob_bases(size)
    key_alice, key_bob = b92(alice_bits, bob_bases)

    assert key_bob == key_alice
