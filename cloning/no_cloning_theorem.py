"""Module providing No Cloning Theorem demonstration"""

from sympy.physics.quantum.qubit import Qubit, matrix_to_qubit
from sympy import sqrt
from sympy.physics.quantum import TensorProduct
from sympy.physics.quantum.represent import represent

# From Mathematics of Quantum Computing
# 4.6.2 Perfect Quantum Copier


def clone(q1, q2):
    """Function that returns a q1*q1 state"""
    return TensorProduct(q1, q1)


x = 1
r = clone(Qubit(0), x)
print(f"1. clone should satisfy:\nclone(|0>*|x>) = |0>*|0>:\nr={r}")

r = clone(Qubit(1), Qubit(x))
print(f"\n2. clone should satisfy:\nclone(|1>*|x>) = |1>*|1>:\nr={r}")

q = 1 / sqrt(2) * (Qubit(0) + Qubit(1))
r = clone(q, Qubit(x))
print("\n3. clone should satisfy:")
print("clone([1/sqrt(2)(|0> + |1>)]*|x>) = [1/sqrt(2)[(|0> + |1>)]*[1/sqrt(2)(|0> + |1>)]")
print(f"r={r}")
r = matrix_to_qubit(represent(r))
print("Equivalent to:")
print(r)

print("\n4. clone is supposed to be linear so it must satisfy:")
print("1 / sqrt(2) * (clone(Qubit(0), x) + clone(Qubit(1), x))")
r1 = 1 / sqrt(2) * (clone(Qubit(0), x) + clone(Qubit(1), x))
print(f"r={r1}")
r1 = matrix_to_qubit(represent(r1))
print("Equivalent to:")
print(r1)

print("\n5. r and r1 are not the same => clone is not possible")
assert r != r1
