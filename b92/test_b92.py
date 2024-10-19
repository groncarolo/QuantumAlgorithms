from b92.b92 import b92
from util.util import minus, zero, plus, one, unkn


def test_b92():
    print()

    def get_alice_bits(*args):
        return [0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0]

    def get_bob_bases(*args):
        return ['X', '+', 'X', 'X', '+', 'X', '+', '+', 'X', '+', 'X', '+']

    bob_measures = [minus, zero, plus, minus, one, minus, zero, zero, plus, one, plus, zero]
    bob_measure_iterator = iter(bob_measures)

    def get_bob_measure(*args):
        return next(bob_measure_iterator)

    private_key, _ = b92(get_alice_bits, get_bob_bases, get_bob_measure)
    truth = [zero, unkn, unkn, zero, one, zero, unkn, unkn, unkn, one, unkn, unkn]
    assert private_key == truth
