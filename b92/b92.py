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

from sympy.physics.quantum.gate import HadamardGate
from sympy.physics.quantum.qapply import qapply

from util.util import one, unkn, minus, zero, plus


def b92_alice_part(get_alice_bits_fx, gen_bit_size):
    """
    :param func get_alice_bits_fx: function that returns Alice bits
    :param int gen_bit_size: how many bit we want to generate
    :return alice_sent: alice measured qubits
    :return alice_bits: alice randomly picked bits
    """

    # get bits and bases Alice side
    alice_bits = get_alice_bits_fx(gen_bit_size)
    print(f"Alice bits: {alice_bits}")

    # we use a non-orthogonal base
    # {|→>, |↗>} = {zero, plus}
    alice_sent = [plus if b == 1 else zero for b in alice_bits]

    print(f"Alice sent: {alice_sent}")
    return alice_sent, alice_bits


def b92_bob_part(get_bob_bases_fx, measure_all_oneshot_fx,  gen_bit_size, alice_sent):
    """
    :param func get_bob_bases_fx: function that returns Bob bases
    :param int gen_bit_size: how many bit we want to generate
    :param qubit list alice_sent: alice measured qubits (might have been eavesdropped)
    return private_key: matching bases private key
    """
    bob_bases = get_bob_bases_fx(gen_bit_size)
    print(f"Bob bases: {bob_bases}")

    private_key = []

    for q, bb in zip(alice_sent, bob_bases):
        if bb == '+':
            # change base
            q = qapply(HadamardGate(0) * q)
            m = measure_all_oneshot_fx(q)
            if m == plus:
                private_key.append(one)
            elif m == one:
                private_key.append(one)
            else:
                private_key.append(unkn)
        elif bb == 'X':
            m = measure_all_oneshot_fx(q)
            if m == minus:
                private_key.append(zero)
            elif m == zero:
                private_key.append(zero)
            else:
                private_key.append(unkn)

    pk_size = sum(1 for x in private_key if x != '-')
    print(f"private_key {private_key} size:{pk_size}")
    return private_key


def b92(get_alice_bits_fx, get_bob_bases_fx, measure_all_oneshot_fx, gen_bit_size=10):
    """
    Run B92 algorithm and return a private key

    :param func get_alice_bits_fx: function that returns Alice bits
    :param func get_bob_bases_fx: function that returns Bob bases
    :param int gen_bit_size: how many bit we want to generate
    """
    alice_sent, alice_bits = b92_alice_part(get_alice_bits_fx,
                                            gen_bit_size)

    private_key = b92_bob_part(get_bob_bases_fx, measure_all_oneshot_fx, gen_bit_size, alice_sent)

    return private_key, alice_sent
