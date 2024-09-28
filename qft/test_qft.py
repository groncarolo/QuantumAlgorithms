from sympy.physics.quantum.qapply import qapply
from sympy.physics.quantum.qubit import Qubit
from sympy.physics.quantum.qft import QFT

from qft import qft
def test_dft():
    n = 4
    circ = qft(0, n)
    print(f"\nQFT={circ}")

    q = Qubit('0101')
    r = qapply(circ * q)

    qft_ref = qapply(QFT(0, n).decompose() * q)

    assert r == qft_ref
