"""Module providing BB84 code"""

from sympy.physics.quantum.gate import HadamardGate
from sympy.physics.quantum.qapply import qapply
from sympy.physics.quantum.qubit import Qubit

from util.measure_all import measure_all_oneshot
from util.util import get_random_bases


def bb84_alice_part(get_alice_bits_fx, get_alice_bases_fx, gen_bit_size):
    """
    :param func get_alice_bits_fx: function that returns Alice bits
    :param func get_alice_bases_fx: function that returns Alice bases
    :param int gen_bit_size: how many bit we want to generate
    :return alice_sent: alice measured qubits
    :return alice_bases: alice (randomly picked) bases
    return alice_bits: alice randomly picked bits
    """

    # get bits and bases Alice side
    alice_bits = get_alice_bits_fx(gen_bit_size)
    alice_bases = get_alice_bases_fx(gen_bit_size)
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
    return alice_sent, alice_bases, alice_bits


def bb84_eve_part(alice_sent, gen_bit_size):
    """
    :param qubit list alice_sent: alice measured qubits
    :param int gen_bit_size: how many bit we want to generate
    return eavesdropped: alice eavesdropped qubits
    """

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
    return eavesdropped


def bb84_bob_part(get_bob_bases_fx, gen_bit_size, alice_sent, alice_bases):
    """
    :param func get_bob_bases_fx: function that returns Bob bases
    :param int gen_bit_size: how many bit we want to generate
    :param bases list alice_bases: alice (randomly picked) bases
    :param qubit list alice_sent: alice measured qubits (might have been eavesdropped)
    return private_key: matching bases private key
    """
    bob_bases = get_bob_bases_fx(gen_bit_size)
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
    return private_key


def bb84_detect_eavesdropping(private_key, alice_bits, check_size):
    '''
    :param list private_key: complete private key
    :param int check_size: how many bit of the key should be used to check
           eavesdropping
    :param alice_bits: alice randomly picked bits (we use just check_size portion)
    '''
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
    return eavesdropped


def bb84(get_alice_bits_fx, get_alice_bases_fx, get_bob_bases_fx,
         gen_bit_size=10, eavesdropping=False, check_size=0):
    """
    Run BB84 algorithm and return a private key

    :param func get_alice_bits_fx: function that returns Alice bits
    :param func get_alice_bases_fx: function that returns Alice bases
    :param func get_bob_bases_fx: function that returns Bob bases
    :param int gen_bit_size: how many bit we want to generate
    :param Bool eavesdropping: simulate Eve eavesdropping
    :param int check_size: how many bit of the key should be used to check
           eavesdropping


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
    alice_sent, alice_bases, alice_bits = bb84_alice_part(get_alice_bits_fx,
                                                          get_alice_bases_fx,
                                                          gen_bit_size)

    if eavesdropping:
        alice_sent = bb84_eve_part(alice_sent, gen_bit_size)

    private_key = bb84_bob_part(get_bob_bases_fx, gen_bit_size, alice_sent,
                                alice_bases)

    eavesdropped = 0
    if eavesdropping:
        eavesdropped = bb84_detect_eavesdropping(private_key, alice_bits,
                                                 check_size)

    return private_key, alice_sent, eavesdropped
