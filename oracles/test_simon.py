from simon import find_req_on_f, find_c
from simon import simon
from sympy.physics.quantum import TensorProduct
from sympy.physics.quantum.represent import represent
from sympy.physics.quantum.qubit import Qubit, IntQubit, matrix_to_qubit, measure_all, measure_partial

from sympy import simplify


def test_find_req_on_f_1():
    print()
    r = find_req_on_f(0b101, range(0, 2 ** 3))
    truth = [(0, 5), (1, 4), (2, 7), (3, 6), (4, 1), (5, 0), (6, 3), (7, 2)]

    for k in zip(r, truth):
        assert k[0] == k[1]


def test_find_req_on_f_2():
    print()
    r = find_req_on_f(0b011, range(0, 2 ** 3))

    truth = [(0, 3), (1, 2), (2, 1), (3, 0), (4, 7), (5, 6), (6, 5), (7, 4)]
    for k in zip(r, truth):
        assert k[0] == k[1]


def test_find_c_1():
    print()
    constraints = ((1, 1, 1), (1, 0, 1), (0, 1, 0))
    r = find_c(constraints)

    truth = [0b101]
    assert truth == r


def test_find_c_2():
    print()
    constraints = ((1, 0, 1, 0, 1, 1, 0),
                   (0, 0, 1, 0, 0, 0, 1),
                   (1, 1, 0, 0, 1, 0, 1),
                   (0, 0, 1, 1, 0, 1, 1),
                   (0, 1, 0, 1, 0, 0, 1),
                   (0, 0, 1, 1, 0, 1, 0),
                   (0, 1, 1, 0, 1, 1, 1))
    r = find_c(constraints)

    truth = [0b1101010]
    assert truth == r


# def test_find_c_3():
#     constraints = ((1, 1, 1, 1, 0, 0, 0, 0),
#                    (0, 1, 1, 0, 1, 0, 0, 1),
#                    (1, 0, 0, 1, 0, 1, 1, 0),
#                    (0, 0, 1, 1, 1, 1, 0, 0),
#                    (1, 1, 1, 1, 1, 1, 1, 1),
#                    (1, 1, 0, 0, 0, 0, 1, 1),
#                    (1, 0, 0, 0, 1, 1, 1, 0),
#                    (0, 1, 1, 1, 0, 0, 0, 1))
#     r = find_c(constraints)
#
#     truth = [0b10011001, 0b00111100, 0b01011010, 0b01100110, 0b10100101, 0b11000011, 0b11111111]
#     truth.sort()
#     assert truth == r


def test_simon_1():
    print()
    def f(x, *args):
        x = IntQubit(Qubit(*x)).as_int()
        match x:
            case 0b000:
                return 0b100
            case 0b101:
                return 0b100
            case 0b001:
                return 0b001
            case 0b100:
                return 0b001
            case 0b010:
                return 0b101
            case 0b111:
                return 0b101
            case 0b011:
                return 0b111
            case 0b110:
                return 0b111

    n = 3
    truth_state = 1 / 4 * (TensorProduct(Qubit('000'), Qubit('100') + Qubit('001') + Qubit('101') + Qubit('111')) +
                           TensorProduct(Qubit('010'), Qubit('100') + Qubit('001') - Qubit('101') - Qubit('111')) +
                           TensorProduct(Qubit('101'), Qubit('100') - Qubit('001') + Qubit('101') - Qubit('111')) +
                           TensorProduct(Qubit('111'), Qubit('100') - Qubit('001') - Qubit('101') + Qubit('111')))
    truth_constraints = [(0,0,0), (0, 1, 0), (1, 0, 1), (1, 1, 1)]
    truth_c = 0b101
    state, measures, c, constraints, req = simon(f, n)
    assert constraints == truth_constraints

    truth_state = matrix_to_qubit(represent(truth_state))
    assert simplify(truth_state - state) == 0
    assert c[0] == truth_c


def test_simon_2():
    print()

    def f(x, *args):
        x = IntQubit(Qubit(*x)).as_int()
        match x:
            case 0b000:
                return 0b000
            case 0b001:
                return 0b100
            case 0b010:
                return 0b100
            case 0b011:
                return 0b000
            case 0b100:
                return 0b010
            case 0b101:
                return 0b110
            case 0b110:
                return 0b110
            case 0b111:
                return 0b010

    n = 3
    truth_state = 1 / 4 * (TensorProduct(Qubit('000'), Qubit('000') + Qubit('010') + Qubit('100') + Qubit('110')) +
                           TensorProduct(Qubit('011'), Qubit('000') + Qubit('010') - Qubit('100') - Qubit('110')) +
                           TensorProduct(Qubit('100'), Qubit('000') - Qubit('010') + Qubit('100') - Qubit('110')) +
                           TensorProduct(Qubit('111'), Qubit('000') - Qubit('010') - Qubit('100') + Qubit('110')))
    truth_constraints = [(0, 0, 0), (0, 1, 1), (1, 0, 0), (1, 1, 1)]
    truth_c = 0b011
    state, measures, c, constraints, req = simon(f, n)

    assert constraints == truth_constraints
    truth_state = matrix_to_qubit(represent(truth_state))
    assert simplify(truth_state - state) == 0
    assert c[0] == truth_c
