from bb84.bb84 import bb84
import numpy as np

from ..util.util import get_random_bits, get_random_bases, zero, one, minus, plus


def test_bb84():
    print()

    def get_alice_bits(*args):
        return [0, 1, 0, 1, 1, 0, 1, 1, 1]

    def get_alice_bases(*args):
        return ['Z', 'Z', 'X', 'Z', 'X', 'X', 'X', 'Z', 'Z']

    def get_bob_bases(*args):
        return ['Z', 'X', 'X', 'Z', 'Z', 'X', 'Z', 'X', 'Z']

    private_key, _, _ = bb84(get_alice_bits, get_alice_bases, get_bob_bases)
    truth = [zero, '-', zero, one, '-', zero, '-', '-', one]
    assert private_key == truth


def test_bb84_1():
    print()
    np.random.seed(10)

    private_key, _, _ = bb84(get_random_bits, get_random_bases, get_random_bases)
    truth = [one, one, '-', one, '-', one, one, zero, '-', one]
    assert private_key == truth


def test_bb84_6_25():
    print()

    def get_alice_bits(*args):
        return [1, 0, 0, 1, 0, 0, 0, 1, 1]

    def get_alice_bases(*args):
        return ['X', 'X', 'Z', 'Z', 'Z', 'X', 'X', 'X', 'X']

    def get_bob_bases(*args):
        return ['Z', 'X', 'X', 'Z', 'Z', 'X', 'Z', 'X', 'Z']


    private_key, alice_sent, _ = bb84(get_alice_bits, get_alice_bases, get_bob_bases)
    truth = [minus, plus, zero, one, zero, plus, plus, minus, minus]
    assert truth == alice_sent


def test_bb84_6_26():
    print()

    def get_alice_bits(*args):
        return [0, 1, 0, 1, 0, 1, 1, 0, 1]

    def get_alice_bases(*args):
        return ['X', 'X', 'Z', 'X', 'Z', 'Z', 'X', 'X', 'Z']

    def get_bob_bases(*args):
        return ['Z', 'Z', 'Z', 'Z', 'Z', 'X', 'X', 'Z', 'Z']

    private_key, _, _ = bb84(get_alice_bits, get_alice_bases, get_bob_bases)
    truth = ['-', '-', zero, '-', zero, '-', one, '-', one]
    assert private_key == truth


def test_bb84_eavesdropping_probability_detection():
    print()

    key_size = 256
    check_size = 50

    private_key, _, eavesdropped = bb84(get_random_bits, get_random_bases, get_random_bases,
                                        gen_bit_size=key_size + check_size, eavesdropping=True, check_size=check_size)
    prob = 1. - (3 / 4) ** check_size
    print(f"prob to catch Eve: {prob} with {check_size} bits" )
    print(f"Eve was caught {eavesdropped} times")

    usable_pk = sum(1 if x != '-' else 0 for x in private_key)
    print(f"Usable key len {usable_pk}")
