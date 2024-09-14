import fractions
import random

import sympy
from sympy.physics.quantum.qapply import qapply
from sympy.physics.quantum.qubit import Qubit, matrix_to_qubit, IntQubit, measure_partial_oneshot, \
    measure_all, measure_all_oneshot
from sympy import Symbol, preorder_traversal
from sympy.physics.quantum import TensorProduct
from sympy.physics.quantum.represent import represent
from oracle import oracle
from sympy import Xor, Or, And, satisfiable, Not, simplify
from util import hn
from sympy.physics.quantum.qft import IQFT, QFT
from math import gcd


# This code implements Simons periodicity algorithm
# The problem:
# consider f {0,1}^n  -> f {0, 1}^n that is not known
# we are told that exists c = c0c1c2...cn-1
# such that for all string x, y belonging to {0,1}^n
# we have
# f(x) == f(y)  if and only if x = y XOR c

#                      +-----------------+
#   |x>  |0>-/m-H*m----|                 |--/m--QFT+---M |x>
#                      |       U_f_a,N   |
#   |y>  |0>-/n--------|                 |--/n--------  |y XOR f_a,N(x)>
#                      +-----------------+


def fan(x, N, a):
    x = IntQubit(Qubit(*x)).as_int()
    r = (a ** x) % N
    return r


def shor_period(f, m, n, N, a):
    # apply H gate to both inputs
    x = qapply(hn(m) * Qubit('0' * m))
    print("|x>: {x}".format(x=x))
    y = Qubit('0' * n)
    print("|y>: {y}".format(y=y))
    xy = TensorProduct(x, y)
    print("|xy>: {xy}".format(xy=xy))
    xy = matrix_to_qubit(represent(xy))
    print("|xy>: {xy}".format(xy=xy))

    # apply oracle
    xy_xor_fx = oracle(x, y, f, N, a)
    print("|xy_xor_fx>: {xy_xor_fx}".format(xy_xor_fx=xy_xor_fx))

    xy_xor_fx = measure_partial_oneshot(xy_xor_fx, range(n))
    print("|xy_xor_fx>: {xy_xor_fx} n = {n}".format(xy_xor_fx=xy_xor_fx, n=n))

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

    print("New state without y |y_xor_fx>: {y_xor_fx}".format(y_xor_fx=y_xor_fx))

    # apply QFT to
    y_xor_fx = qapply(IQFT(0, m).decompose() * y_xor_fx)
    print("After IQFT |y_xor_fx>={y_xor_fx}".format(y_xor_fx=y_xor_fx))

    mea = measure_all_oneshot(y_xor_fx)
    print("measure(state) = {mea} as int = {d}".format(mea=mea, d=IntQubit(mea).as_int()))

    f = fractions.Fraction.from_float(float(IntQubit(mea).as_int() / 2 ** m)).limit_denominator(N)
    r = f.denominator

    if f.numerator == 0:
        return None

    if a ** r % N != 1:
        return None
    else:
        return r


def shor(N, *args):
    if sympy.isprime(N):
        print("{N} is prime!")
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
            print("a = {a} and N = {N} are not relatively prime".format(a=a, N=N))
            factors.append(gcd(a, N))
            factors.append(int(N / gcd(a, N)))
            return factors

        print("{s}".format(s="=" * 40))
        print("Shore N={N}, m={m}, n={n}, a={a} iter {i}".format(N=N, m=m, n=n, a=a, i=i))
        r = shor_period(fan, m, n, N, a)
        i = i + 1
    print("period r = {r}".format(r=r))
    if r is None:
        return factors

    factors.append(gcd(int(a ** (r / 2)) - 1, N))
    factors.append(gcd(int(a ** (r / 2)) + 1, N))
    return factors


