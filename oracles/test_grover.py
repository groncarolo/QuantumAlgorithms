from simon import find_req_on_f, find_c
from simon import simon
from sympy.physics.quantum import TensorProduct
from sympy.physics.quantum.represent import represent
from sympy.physics.quantum.qubit import Qubit, IntQubit, matrix_to_qubit, measure_all, measure_partial
from sympy import sqrt, simplify, preorder_traversal, Rational, Mul

from sympy import simplify
from grover import grover


def test_grover_1():
    print()
    def f(x):
        x = IntQubit(Qubit(*x)).as_int()
        match x:
            case 0b101:
                return 1
            case _:
                return 0

    n = 3
    r = grover(f, n)
    truth = -sqrt(2)*Qubit('000')/16 - sqrt(2)*Qubit('001')/16 - sqrt(2)*Qubit('010')/16 - sqrt(2)*Qubit('011')/16 - sqrt(2)*Qubit('100')/16 + 11*sqrt(2)*Qubit('101')/16 - sqrt(2)*Qubit('110')/16 - sqrt(2)*Qubit('111')/16
    assert r == truth


def test_grover_2():
    print()
    def f(x):
        x = IntQubit(Qubit(*x)).as_int()
        match x:
            case 0b1101:
                return 1
            case _:
                return 0

    n = 4
    r = grover(f, n)
    truth = - 171*Qubit('0000')/1024 - 171*Qubit('0001')/1024 - 171*Qubit('0010')/1024 - 171*Qubit('0011')/1024 - 171*Qubit('0100')/1024 - 171*Qubit('0101')/1024 - 171*Qubit('0110')/1024 - 171*Qubit('0111')/1024 - 171*Qubit('1000')/1024 - 171*Qubit('1001')/1024 - 171*Qubit('1010')/1024 - 171*Qubit('1011')/1024 - 171*Qubit('1100')/1024 + 781*Qubit('1101')/1024 - 171*Qubit('1110')/1024 - 171*Qubit('1111')/1024
    assert r == truth
