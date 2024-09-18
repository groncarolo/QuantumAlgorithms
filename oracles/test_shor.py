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

from shor import shor


def test_shor_1():
    N = 15
    factors = shor(N, 2)
    print("factors = {factors}".format(factors=factors))
    truth = [3, 5]
    assert truth == sorted(factors)


def test_shor_2():
    N = 15
    factors = shor(N, 7)
    print("factors = {factors}".format(factors=factors))
    truth = [3, 5]
    assert truth == sorted(factors)

def test_shor_3():
    N = 15
    factors = shor(N, 13)
    print("factors = {factors}".format(factors=factors))
    truth = [3, 5]
    assert truth == sorted(factors)

def test_shor_4():
     N = 3*7
     factors = shor(N, 13)
     print("factors = {factors}".format(factors=factors))
     truth = [3, 7]
     assert truth == sorted(factors)
