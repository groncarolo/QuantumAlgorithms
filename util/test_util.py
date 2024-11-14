from sympy import sqrt, simplify, I
from sympy.physics.quantum import qapply
from sympy.physics.quantum.qubit import Qubit

from util.util import plus, minus, change_basis, i_minus_state, i_state


def test_change_basis_0():
    q = sqrt(3) / 2 * Qubit('0') + 1 / 2 * Qubit('1')
    new_base = (plus, minus)
    q_new = change_basis(q, new_base)
    truth = (sqrt(3) + 1) / (2 * sqrt(2)) * Qubit('0') + (sqrt(3) - 1) / (2 * sqrt(2)) * Qubit('1')
    assert simplify(truth - q_new) == 0


def test_change_basis_1():
    q = sqrt(3) / 2 * Qubit('0') + 1 / 2 * Qubit('1')
    new_base = (sqrt(3) / 2 * Qubit(0) + I / 2 * Qubit(1), I / 2 * Qubit(0) + sqrt(3) / 2 * Qubit(1))
    q_new = change_basis(q, new_base)
    truth = (3 - 1.0 * I) / 4 * Qubit('0') + sqrt(3) * (1.0 - I) / 4 * Qubit('1')
    assert simplify(truth - q_new) == 0


def test_change_basis_2():
    q = sqrt(3) / 2 * Qubit('0') + 1 / 2 * Qubit('1')
    new_base = (i_state, i_minus_state)
    q_new = change_basis(q, new_base)
    truth = (sqrt(3) - I) / (2 * sqrt(2)) * Qubit('0') + (sqrt(3) + I) / (2 * sqrt(2)) * Qubit('1')
    assert simplify(truth - q_new) == 0


def test_change_basis_3():
    q = (1 - 2 * I) / sqrt(6) * Qubit('0') + 1 / sqrt(6) * Qubit('1')
    new_base = (plus, minus)
    q_new = change_basis(q, new_base)
    truth = (1 - I) / (sqrt(3)) * Qubit('0') - I / (sqrt(3)) * Qubit('1')
    assert simplify(truth - q_new) == 0


def test_change_basis_4():
    q = (1 - 2 * I) / sqrt(6) * Qubit('0') + 1 / sqrt(6) * Qubit('1')
    new_base = (i_state, i_minus_state)
    q_new = change_basis(q, new_base)
    truth = (1 - 3*I) / (2*sqrt(3)) * Qubit('0') + (1-I) / (2*sqrt(3)) * Qubit('1')
    assert simplify(truth - q_new) == 0
