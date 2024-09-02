from sympy.physics.quantum.qapply import qapply
from sympy.physics.quantum.qubit import Qubit, matrix_to_qubit
from sympy import Symbol, sqrt
from sympy.physics.quantum import TensorProduct
from sympy.physics.quantum.gate import CNOT, XGate, ZGate, HadamardGate
from sympy.physics.quantum.represent import represent

# Introduction to classical and quantum computing
# 6.5.3 Quantum Solution

phi_p = 1 / sqrt(2) * (Qubit('00') + Qubit('11'))
print("|PHI+>: {phi}".format(phi=phi_p))

# qubit to teleport
alpha = Symbol('alpha', real=True)
beta = Symbol('beta', real=True)
q = alpha * Qubit(0) + beta * Qubit(1)
print("State to teleport: |q>={q}".format(q=q))

# full state
full_state = TensorProduct(q, phi_p)
full_state = matrix_to_qubit(represent(full_state))
print("|q>|PHI+>={full}".format(full=full_state))

# apply CNOT
print("Apply CNOT")
c = CNOT(2, 1)  # that qubits are indexed from right to left
full_state = qapply(c * full_state)
print("CNOT_2_1*|q>|PHI+>={full}".format(full=full_state))

# apply Hadamard
print("Apply Hadamard")
full_state = qapply(HadamardGate(2) * full_state)
print("H(2)*CNOT_2_1*|q>|PHI+>={full}".format(full=full_state))

# factoring the first 2 qubits:
Q_00 = alpha * Qubit(0) + beta * Qubit(1)
Q_01 = alpha * Qubit(1) + beta * Qubit(0)
Q_10 = alpha * Qubit(0) - beta * Qubit(1)
Q_11 = alpha * Qubit(1) - beta * Qubit(0)

a = (TensorProduct(Qubit('00'), Q_00) +
     TensorProduct(Qubit('01'), Q_01) +
     TensorProduct(Qubit('10'), Q_10) +
     TensorProduct( Qubit('11'), Q_11)) / 2
a = matrix_to_qubit(represent(a))
assert a == full_state

print("\nQ_00 -> nothing to do")
r = Q_00
print("({q})={r}".format(q=Q_00, r=r))
assert r == q

print("\nQ_01 -> Apply XGate")
r = qapply(XGate(0) * Q_01)
print("X*({q})={r}".format(q=Q_01, r=r))
assert r == q

print("\nQ_10 -> Apply ZGate")
r = qapply(ZGate(0) * Q_10)
print("Z*({q})={r}".format(q=Q_10, r=r))
assert r == q

print("\nQ_11 -> Apply XGate, ZGate")
r = qapply(XGate(0) * Q_11)
r = qapply(ZGate(0) * r)
print("X*Z*({q})={r}".format(q=Q_11, r=r))
assert r == q
