from sympy.physics.quantum.qubit import Qubit, IntQubit
from sympy import sqrt
from oracles.grover import grover


def test_grover_1():
    print()
    def f(x, *args):
        x = IntQubit(Qubit(*x)).as_int()
        match x:
            case 0b101:
                return 1
            case _:
                return 0

    n = 3
    r = grover(f, n)
    truth = (-sqrt(2)*Qubit('000')/16 - sqrt(2)*Qubit('001')/16 - sqrt(2)*Qubit('010')/16 - sqrt(2)*Qubit('011')/16 -
             sqrt(2)*Qubit('100')/16 + 11*sqrt(2)*Qubit('101')/16 - sqrt(2)*Qubit('110')/16 - sqrt(2)*Qubit('111')/16)
    assert r == truth


def test_grover_2():
    print()
    def f(x, *args):
        x = IntQubit(Qubit(*x)).as_int()
        match x:
            case 0b1101:
                return 1
            case _:
                return 0

    n = 4
    r = grover(f, n)
    truth = (- 171*Qubit('0000')/1024 - 171*Qubit('0001')/1024 - 171*Qubit('0010')/1024 - 171*Qubit('0011')/1024 -
             171*Qubit('0100')/1024 - 171*Qubit('0101')/1024 - 171*Qubit('0110')/1024 - 171*Qubit('0111')/1024 -
             171*Qubit('1000')/1024 - 171*Qubit('1001')/1024 - 171*Qubit('1010')/1024 - 171*Qubit('1011')/1024 -
             171*Qubit('1100')/1024 + 781*Qubit('1101')/1024 - 171*Qubit('1110')/1024 - 171*Qubit('1111')/1024)
    assert r == truth
