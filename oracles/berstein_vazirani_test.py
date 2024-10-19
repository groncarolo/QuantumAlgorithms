from oracles.berstein_vazirani import berstein_vazirani
from sympy import preorder_traversal
from sympy.physics.quantum.qubit import Qubit,  measure_partial_oneshot
import numpy as np


def test_berstein_vazirani():
    print()
    size = 4
    s = np.random.choice([0, 1], size=(size,))
    print(f'\ns: {s}')

    r = berstein_vazirani(s, size)
    print(f'Result: {r}')

    m = measure_partial_oneshot(r, range(size))
    print(f'Measure: {m}')
    s_found = None
    # skip y part of the measure
    for arg in preorder_traversal(m):
        if isinstance(arg, Qubit):
            s_found = Qubit(*arg.qubit_values[0:size])

    assert Qubit(*s) == s_found
