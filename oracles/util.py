from sympy.physics.quantum.qubit import Qubit
from sympy.physics.quantum.gate import HadamardGate

def get_qubit_size(q):
    if isinstance(q, Qubit):
        return q.nqubits
    else:
        for expr in q.args:
            for e in expr.args:
                if isinstance(e, Qubit):
                    return e.nqubits
    return 0


def hn(n, start=0):
    ret = 1
    for i in range(start, start + n):
        ret = ret * HadamardGate(i)
    return ret
