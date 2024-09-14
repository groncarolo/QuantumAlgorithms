""" This module implements Shor factorization algorithm"""
import fractions
import random

from math import gcd
from sympy import isprime
from sympy.physics.quantum.qapply import qapply
from sympy.physics.quantum.qubit import Qubit, matrix_to_qubit, IntQubit, measure_partial_oneshot, \
    measure_all_oneshot
from sympy.physics.quantum import TensorProduct
from sympy.physics.quantum.represent import represent
from sympy.physics.quantum.qft import IQFT
from oracle import oracle
from util import hn


def fan(x, N, a):
    """
    Function to calculate a**x%N
    :param x: |x> qubit
    :param N: product we want to find the factors of
    :param a: relatively prime number to N
  """
    x = IntQubit(Qubit(*x)).as_int()
    r = (a ** x) % N
    return r


def shor_period(f, m, n, N, a):
    """
    Shor's algorithm, find the period quantumly
    :param func f: fan function returning a**x%N
    :param m: |x> bit number
    :param n: |y> bit number
    :param N: product we want to find the factors of
    :param a: relatively prime number to N
    :returns int period

    The problem:
    Factor an interger N into its prime components

    The Solution:
                         +-----------------+
      |x>  |0>-/m-H*m----|                 |--/m--QFT+---M |x>
                         |       U_f_a,N   |
      |y>  |0>-/n--------|                 |--/n--------  |y XOR f(x, a, N)>
                         +-----------------+
    """
    # apply H gate to both inputs
    x = qapply(hn(m) * Qubit('0' * m))
    print(f"|x>: {x}")
    y = Qubit('0' * n)
    print(f"|y>: {y}")
    xy = TensorProduct(x, y)
    print(f"|xy>: {xy}")
    xy = matrix_to_qubit(represent(xy))
    print(f"|xy>: {xy}")

    # apply oracle
    xy_xor_fx = oracle(x, y, f, N, a)
    print(f"|xy_xor_fx>: {xy_xor_fx}")

    xy_xor_fx = measure_partial_oneshot(xy_xor_fx, range(n))
    print(f"|xy_xor_fx>: {xy_xor_fx} n = {n}")

    # create a new state without y qubit
    y_xor_fx = 0
    for expr in xy_xor_fx.args:
        ee = 1
        for e in expr.args:
            if isinstance(e, Qubit):
                qbit = e
            else:
                ee *= e
        # throw y part and just keep x
        y_xor_fx += ee * Qubit(*qbit.qubit_values[0:qbit.dimension - n])

    print(f"New state without y |y_xor_fx>: {y_xor_fx}")

    # apply QFT to
    y_xor_fx = qapply(IQFT(0, m).decompose() * y_xor_fx)
    print(f"After IQFT |y_xor_fx>={y_xor_fx}")

    mea = measure_all_oneshot(y_xor_fx)
    print(f"measure(state) = {mea} as int = {IntQubit(mea).as_int()}")

    f = fractions.Fraction.from_float(float(IntQubit(mea).as_int() / 2 ** m)).limit_denominator(N)
    r = f.denominator

    if f.numerator == 0:
        return None

    if a ** r % N != 1:
        return None

    return r


def shor(N, *args):
    """
    Shor's algorithm, non-quantum part
    :param N: product we want to find the factors of
    :returns [int] factors
    """
    if isprime(N):
        print(f"{N} is prime!")
        return None

    r = None
    max_tries = 30
    i = 0
    factors = []
    while i < max_tries and r is None:
        if args:
            a = args[0]
            assert a < N
        else:
            a = random.randint(2, N - 1)
        m = n = len(bin(N)[2:]) + 1

        if 1 < gcd(a, N) < N:
            print(f"a = {a} and N = {N} are not relatively prime")
            factors.append(gcd(a, N))
            factors.append(int(N / gcd(a, N)))
            return factors

        print(f"{'=' * 40}")
        print(f"Shore N={N}, m={m}, n={n}, a={a} iter {i}")
        r = shor_period(fan, m, n, N, a)
        i = i + 1
    print(f"period r = {r}")
    if r is None:
        return factors

    factors.append(gcd(int(a ** (r / 2)) - 1, N))
    factors.append(gcd(int(a ** (r / 2)) + 1, N))
    return factors
