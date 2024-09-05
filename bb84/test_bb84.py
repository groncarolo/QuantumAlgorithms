from bb84 import bb84, get_random_bases, get_random_bits
from sympy.physics.quantum.qubit import Qubit
from sympy import sqrt
import numpy as np


def test_bb84():
    print()

    def get_alice_bits():
        return [0, 1, 0, 1, 1, 0, 1, 1, 1]

    def get_alice_bases():
        return ['Z', 'Z', 'X', 'Z', 'X', 'X', 'X', 'Z', 'Z']

    def get_bob_bases():
        return ['Z', 'X', 'X', 'Z', 'Z', 'X', 'Z', 'X', 'Z']

    private_key, _ = bb84(get_alice_bits, get_alice_bases, get_bob_bases)
    truth = [Qubit(0), '-', Qubit(0), Qubit(1), '-', Qubit(0), '-', '-', Qubit(1)]
    assert private_key == truth


def test_bb84_1():
    print()
    np.random.seed(10)

    private_key, _ = bb84(get_random_bits, get_random_bases, get_random_bases)
    truth = [Qubit(1), Qubit(1), '-', Qubit(1), '-', Qubit(1), Qubit(1), Qubit(0), '-', Qubit(1)]
    assert private_key == truth


def test_bb84_6_25():
    print()

    def get_alice_bits():
        return [1, 0, 0, 1, 0, 0, 0, 1, 1]

    def get_alice_bases():
        return ['X', 'X', 'Z', 'Z', 'Z', 'X', 'X', 'X', 'X']

    def get_bob_bases():
        return ['Z', 'X', 'X', 'Z', 'Z', 'X', 'Z', 'X', 'Z']

    plus = Qubit(0) / sqrt(2) + Qubit(1) / sqrt(2)
    minus = Qubit(0) / sqrt(2) - Qubit(1) / sqrt(2)
    zero = Qubit(0)
    one = Qubit(1)

    private_key, alice_sent = bb84(get_alice_bits, get_alice_bases, get_bob_bases)
    truth = [minus, plus, zero, one, zero, plus, plus, minus, minus]
    assert truth == alice_sent


def test_bb84_6_26():
    print()

    def get_alice_bits():
        return [0, 1, 0, 1, 0, 1, 1, 0, 1]

    def get_alice_bases():
        return ['X', 'X', 'Z', 'X', 'Z', 'Z', 'X', 'X', 'Z']

    def get_bob_bases():
        return ['Z', 'Z', 'Z', 'Z', 'Z', 'X', 'X', 'Z', 'Z']

    private_key, _ = bb84(get_alice_bits, get_alice_bases, get_bob_bases)
    truth = ['-', '-', Qubit(0), '-', Qubit(0), '-', Qubit(1), '-', Qubit(1)]
    assert private_key == truth
