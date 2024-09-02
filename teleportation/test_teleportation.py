from sympy.physics.quantum.qapply import qapply
from sympy.physics.quantum.qubit import Qubit, matrix_to_qubit
from sympy import Symbol, sqrt
from sympy.physics.quantum import TensorProduct
from sympy.physics.quantum.gate import CNOT, XGate, ZGate, HadamardGate
from sympy.physics.quantum.represent import represent


# Introduction to classical and quantum computing
# 6.5.3 exercise 6.16

def test_6_16():
    psi_p = 1 / sqrt(2) * (Qubit('01') + Qubit('10'))
    print("\n|PSI+>: {psi}".format(psi=psi_p))

    # qubit to teleport
    alpha = Symbol('alpha', real=True)
    beta = Symbol('beta', real=True)
    q = alpha * Qubit(0) + beta * Qubit(1)
    print("State to teleport: |q>={q}".format(q=q))

    # full state
    full_state = TensorProduct(q, psi_p)
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
    Q_00 = alpha * Qubit(1) + beta * Qubit(0)
    Q_01 = alpha * Qubit(0) + beta * Qubit(1)
    Q_10 = alpha * Qubit(1) - beta * Qubit(0)
    Q_11 = alpha * Qubit(0) - beta * Qubit(1)

    a = (TensorProduct(Qubit('00'), Q_00) +
         TensorProduct(Qubit('01'), Q_01) +
         TensorProduct(Qubit('10'), Q_10) +
         TensorProduct(Qubit('11'), Q_11)) / 2
    a = matrix_to_qubit(represent(a))
    assert a == full_state

    print("\nQ_00 -> Apply XGate")
    r = qapply(XGate(0) * Q_00)
    print("X*{q}=({r})".format(q=Q_00, r=r))
    assert r == q

    print("\nQ_01 -> nothing to do")
    r = Q_01
    print("{q}=({r})".format(q=Q_01, r=r))
    assert r == q

    print("\nQ_10 -> Apply ZGate ZGate")
    r = qapply(XGate(0) * Q_10)
    r = qapply(ZGate(0) * r)
    print("X*Z*({q})={r}".format(q=Q_10, r=r))
    assert r == q

    print("\nQ_11 -> Apply ZGate")
    r = qapply(ZGate(0) * Q_11)
    print("Z*({q})={r}".format(q=Q_11, r=r))
    assert r == q


def test_6_17():
    GHZ = 1 / sqrt(2) * (Qubit('000') + Qubit('111'))
    print("\n|GHZ+>: {ghz}".format(ghz=GHZ))

    # qubit to teleport
    alpha = Symbol('alpha', real=True)
    beta = Symbol('beta', real=True)
    psi = alpha * Qubit(0) + beta * Qubit(1)
    print("State to teleport: |psi>={psi}".format(psi=psi))

    # full state
    full_state = TensorProduct(psi, GHZ)
    full_state = matrix_to_qubit(represent(full_state))
    print("|psi>|GHZ>={full}".format(full=full_state))

    # apply CNOT_21
    print("Apply CNOT_21")
    c = CNOT(2, 1)  # that qubits are indexed from right to left
    full_state = qapply(c * full_state)
    print("CNOT_2_1*|psi>|GHZ>={full}".format(full=full_state))

    # apply CNOT_32
    print("Apply CNOT_32")
    c = CNOT(3, 2)  # that qubits are indexed from right to left
    full_state = qapply(c * full_state)
    print("CNOT_3_2*CNOT_2_1*|psi>|GHZ>={full}".format(full=full_state))

    # apply Hadamard
    print("Apply Hadamard")
    full_state = qapply(HadamardGate(3) * full_state)
    print("H(3)*CNOT_3_2*CNOT_2_1*|psi>|GHZ>={full}".format(full=full_state))

    # factoring the first 2 qubits:
    Q_000 = alpha * Qubit(0) + beta * Qubit(1)
    Q_010 = alpha * Qubit(1) + beta * Qubit(0)
    Q_100 = alpha * Qubit(0) - beta * Qubit(1)
    Q_110 = alpha * Qubit(1) - beta * Qubit(0)

    a = (TensorProduct(Qubit('000'), Q_000) +
         TensorProduct(Qubit('010'), Q_010) +
         TensorProduct(Qubit('100'), Q_100) +
         TensorProduct(Qubit('110'), Q_110)) / 2
    a = matrix_to_qubit(represent(a))
    assert a == full_state

    print("Q_000 -> nothing to do")
    r = Q_000
    print("{q}={r}".format(q=Q_000, r=r))
    assert r == psi

    print("\nQ_010 -> Apply XGate")
    r = qapply(XGate(0) * Q_010)
    print("X*({q})=({r})".format(q=Q_010, r=r))
    assert r == psi

    print("\nQ_100 -> Apply ZGate")
    r = qapply(ZGate(0) * Q_100)
    print("Z*({q})=({r})".format(q=Q_100, r=r))

    print("\nQ_110 -> Apply XGate, ZGate")
    r = qapply(XGate(0) * Q_110)
    r = qapply(ZGate(0) * r)
    print("X*Z*({q})=({r})".format(q=Q_110, r=r))
    assert r == psi


def test_6_18():
    GHZ = 1 / sqrt(2) * (Qubit('000') + Qubit('111'))
    print("\n|GHZ+>: {ghz}".format(ghz=GHZ))

    # qubit to teleport
    alpha = Symbol('alpha', real=True)
    beta = Symbol('beta', real=True)
    psi = alpha * Qubit(0) + beta * Qubit(1)
    print("State to teleport: |psi>={psi}".format(psi=psi))

    # full state
    full_state = TensorProduct(psi, GHZ)
    full_state = matrix_to_qubit(represent(full_state))
    print("|psi>|GHZ>={full}".format(full=full_state))

    # apply CNOT_32
    print("Apply CNOT_32")
    c = CNOT(3, 2)  # that qubits are indexed from right to left
    full_state = qapply(c * full_state)
    print("CNOT_3_2*|psi>|GHZ>={full}".format(full=full_state))

    # apply Hadamard
    print("Apply Hadamard")
    full_state = qapply(HadamardGate(3) * full_state)
    print("H(3)*CNOT_3_2*|psi>|GHZ>={full}".format(full=full_state))

    # factoring the first 2 qubits:
    Q_00 = alpha * Qubit('00') + beta * Qubit('11')
    Q_01 = alpha * Qubit('11') + beta * Qubit('00')
    Q_10 = alpha * Qubit('00') - beta * Qubit('11')
    Q_11 = alpha * Qubit('11') - beta * Qubit('00')

    a = (TensorProduct(Qubit('00'), Q_00) +
         TensorProduct(Qubit('01'), Q_01) +
         TensorProduct(Qubit('10'), Q_10) +
         TensorProduct(Qubit('11'), Q_11)) / 2
    a = matrix_to_qubit(represent(a))
    assert a == full_state

    print("\nApply Hadamard to Q_00")
    r = qapply(HadamardGate(1) * Q_00)
    print("Q_00={r}".format(r=r))
    # factoring the first qubit:
    Q_00_a = alpha * Qubit('0') + beta * Qubit('1')
    Q_00_b = alpha * Qubit('0') - beta * Qubit('1')
    c = 1 / sqrt(2) * (TensorProduct(Qubit('0'), Q_00_a) + TensorProduct(Qubit('1'), Q_00_b))
    c = matrix_to_qubit(represent(c))
    assert c == r

    print("\nApply Hadamard Q_01")
    r = qapply(HadamardGate(1) * Q_01)
    print("Q_01={r}".format(r=r))
    # factoring the first qubit:
    Q_01_a = beta * Qubit('0') + alpha * Qubit('1')
    Q_01_b = beta * Qubit('0') - alpha * Qubit('1')
    c = 1 / sqrt(2) * (TensorProduct(Qubit('0'), Q_01_a) + TensorProduct(Qubit('1'), Q_01_b))
    c = matrix_to_qubit(represent(c))
    assert c == r

    print("\nApply Hadamard Q_10")
    r = qapply(HadamardGate(1) * Q_10)
    print("Q_10={r}".format(r=r))
    # factoring the first qubit:
    Q_10_a = alpha * Qubit('0') - beta * Qubit('1')
    Q_10_b = alpha * Qubit('0') + beta * Qubit('1')
    c = 1 / sqrt(2) * (TensorProduct(Qubit('0'), Q_10_a) + TensorProduct(Qubit('1'), Q_10_b))
    c = matrix_to_qubit(represent(c))
    print("c={c}".format(c=c))
    assert c == r

    print("\nApply Hadamard Q_11")
    r = qapply(HadamardGate(1) * Q_11)
    print("Q_11={r}".format(r=r))
    # factoring the first qubit:
    Q_11_a = (alpha * Qubit('1') - beta * Qubit('0'))
    Q_11_b = (-alpha * Qubit('1') - beta * Qubit('0'))
    c = 1 / sqrt(2) * (TensorProduct(Qubit('0'), Q_11_a) + TensorProduct(Qubit('1'), Q_11_b))
    c = matrix_to_qubit(represent(c))
    assert c == r

    print("\nQ_000  nothing to do")
    r = Q_00_a
    print("{q}={r}".format(q=Q_00_a, r=r))
    assert r == psi

    print("\nQ_001 -> Apply ZGate")
    r = qapply(ZGate(0) * Q_00_b)
    print("Z*({q})={r}".format(q=Q_00_b, r=r))
    assert r == psi

    print("\nQ_010 -> Apply XGate")
    r = qapply(XGate(0) * Q_01_a)
    print("X*({q})={r}".format(q=Q_01_a, r=r))
    assert r == psi

    print("\nQ_011 -> Apply ZGate XGate")
    r = qapply(ZGate(0) * Q_01_b)
    r = qapply(XGate(0) * r)
    print("Z*X*({q})={r}".format(q=Q_01_b, r=r))
    assert r == psi

    print("\nQ_100 -> Apply ZGate")
    r = qapply(ZGate(0) * Q_10_a)
    print("Z*({q})={r}".format(q=Q_10_a, r=r))
    assert r == psi

    print("\nQ_101 -> Nothing")
    r = Q_10_b
    print("{q}={r}".format(q=Q_10_b, r=r))
    assert r == psi

    print("\nQ_110 -> Apply XGate, ZGate")
    r = qapply(XGate(0) * Q_11_a)
    r = qapply(ZGate(0) * r)
    print("X*Z*({q})={r}".format(q=Q_11_a, r=r))
    assert r == psi

    print("\nQ_111 -> ZGate, XGate, ZGate")
    r = qapply(ZGate(0) * Q_11_b)
    r = qapply(XGate(0) * r)
    r = qapply(ZGate(0) * r)
    print("Z*X*Z*({q})={r}".format(q=Q_11_b, r=r))
    assert r == psi
