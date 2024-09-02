"""
Module providing teleportation code

The problem:
Teleport a quantum state

The Solution:
           SENDING      |  RECEIVING
          ------X-------|--X-Z
|PHI+>    ---H--o---X---|--o-|
a|0>+b|1> ----------o-H-|----o

"""
from sympy.physics.quantum.qapply import qapply
from sympy.physics.quantum.qubit import Qubit, matrix_to_qubit
from sympy import Symbol, sqrt
from sympy.physics.quantum import TensorProduct
from sympy.physics.quantum.gate import CNOT, XGate, ZGate, HadamardGate
from sympy.physics.quantum.represent import represent


phi_p = 1 / sqrt(2) * (Qubit('00') + Qubit('11'))
print(f"|PHI+>: {phi_p}")

# qubit to teleport
alpha = Symbol('alpha', real=True)
beta = Symbol('beta', real=True)
q = alpha * Qubit(0) + beta * Qubit(1)
print(f"State to teleport: |q>={q}")

# full state
full_state = TensorProduct(q, phi_p)
full_state = matrix_to_qubit(represent(full_state))
print(f"|q>|PHI+>={full_state}")

# apply CNOT
print("Apply CNOT")
c = CNOT(2, 1)  # that qubits are indexed from right to left
full_state = qapply(c * full_state)
print(f"CNOT_2_1*|q>|PHI+>={full_state}")

# apply Hadamard
print("Apply Hadamard")
full_state = qapply(HadamardGate(2) * full_state)
print(f"H(2)*CNOT_2_1*|q>|PHI+>={full_state}")

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
print(f"({Q_00})={r}")
assert r == q

print("\nQ_01 -> Apply XGate")
r = qapply(XGate(0) * Q_01)
print(f"X*({Q_01})={r}")
assert r == q

print("\nQ_10 -> Apply ZGate")
r = qapply(ZGate(0) * Q_10)
print(f"Z*({Q_10})={r}")
assert r == q

print("\nQ_11 -> Apply XGate, ZGate")
r = qapply(XGate(0) * Q_11)
r = qapply(ZGate(0) * r)
print(f"X*Z*({Q_11})={r}")
assert r == q
