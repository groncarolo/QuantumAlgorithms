"""Shared quantum-computing utilities used across all notebooks.

Provides:
- Pre-built single-qubit state constants (zero, one, plus, minus, ...).
- Helpers to generate random bits and bases for QKD simulations.
- Gate-building helpers (hn -- n-fold Hadamard).
- State-manipulation helpers (get_sub_state, change_basis).
"""

import numpy as np
from sympy import sqrt, I
from sympy import preorder_traversal
from sympy.physics.quantum.qubit import Qubit
from sympy.physics.quantum.gate import HadamardGate
from sympy.physics.quantum.dagger import Dagger
from sympy.physics.quantum import qapply

# ---------------------------------------------------------------------------
# Single-qubit state constants
# ---------------------------------------------------------------------------

# Computational (Z) basis
zero = Qubit(0)                              # |0>
one = Qubit(1)                               # |1>

# Hadamard (X) basis
plus = Qubit(0) / sqrt(2) + Qubit(1) / sqrt(2)   # |+> = (|0> + |1>)/sqrt(2)
minus = Qubit(0) / sqrt(2) - Qubit(1) / sqrt(2)  # |-> = (|0> - |1>)/sqrt(2)

# Circular (Y) basis
# |i>  = (|0> + i|1>) / sqrt(2)
i_state = Qubit(0) / sqrt(2) + I * Qubit(1) / sqrt(2)
# |-i> = (|0> - i|1>) / sqrt(2)
i_minus_state = Qubit(0) / sqrt(2) - I * Qubit(1) / sqrt(2)

# Placeholder used by BB84 / B92 to mark discarded key positions
unkn = "-"


# ---------------------------------------------------------------------------
# Random-generation helpers  (used by BB84 / B92)
# ---------------------------------------------------------------------------

def get_random_bases(size=10):
    """Return a list of `size` randomly chosen measurement bases.

    Each basis is independently drawn from {'X', '+'} with equal
    probability.  In BB84, 'X' corresponds to the Hadamard basis and
    '+' (equivalently 'Z') to the computational basis.

    :param size: number of bases to generate (default 10)
    :return: numpy array of basis labels ('X' or '+')
    """
    return np.random.choice(["X", "+"], size=(size,))


def get_random_bits(size=10):
    """Return a list of `size` random classical bits (0 or 1).

    Each bit is independently drawn from {0, 1} with equal probability.

    :param size: number of bits to generate (default 10)
    :return: numpy array of integers (0 or 1)
    """
    return np.random.choice([0, 1], size=(size,))


# ---------------------------------------------------------------------------
# Qubit introspection
# ---------------------------------------------------------------------------

def get_qubit_size(q):
    """Return the number of qubits in a (possibly symbolic) qubit state.

    Walks the SymPy expression tree until a concrete Qubit node is found
    and returns its qubit count.  Returns None if no Qubit is present.

    :param q: SymPy quantum expression
    :return: int -- number of qubits, or None if q contains no Qubit
    """
    for arg in preorder_traversal(q):
        if isinstance(arg, Qubit):
            return arg.nqubits
    return None


# ---------------------------------------------------------------------------
# Gate-building helpers
# ---------------------------------------------------------------------------

def hn(n, start=0):
    """Build the n-fold tensor-product Hadamard gate H^n.

    Constructs H_{start} * H_{start+1} * ... * H_{start+n-1} as a
    product of SymPy HadamardGate objects.  This is the gate applied to
    the query register in algorithms such as Bernstein-Vazirani and
    Deutsch-Jozsa.

    :param n: number of Hadamard gates to tensor together
    :param start: index of the first qubit (default 0)
    :return: SymPy gate product representing H^n
    """
    gate = 1
    for i in range(start, start + n):
        gate = gate * HadamardGate(i)
    return gate


# ---------------------------------------------------------------------------
# State-manipulation helpers
# ---------------------------------------------------------------------------

def get_sub_state(state, start, stop):
    """Extract the qubit sub-register at positions [start, stop).

    For a multi-qubit state, discards qubits outside [start, stop) and
    returns the reduced state.  This is used to separate the query
    register from the ancilla qubit after an oracle application.

    :param state: SymPy quantum state (Qubit or superposition)
    :param start: first qubit index to keep (inclusive)
    :param stop: last qubit index to keep (exclusive)
    :return: reduced SymPy qubit expression
    """
    if isinstance(state, Qubit):
        # Single basis state -- just slice the qubit values
        return Qubit(*state.qubit_values[start:stop])

    reduced = 0
    for term in state.args:
        # Each term is a product of a scalar amplitude and a Qubit
        amplitude = 1
        qubit = None
        for factor in term.args:
            if isinstance(factor, Qubit):
                qubit = factor
            else:
                amplitude *= factor
        # Keep only the requested qubit range, preserving the amplitude
        reduced += amplitude * Qubit(*qubit.qubit_values[start:stop])
    return reduced


def change_basis(q, new_basis):
    """Project qubit `q` onto the two states of `new_basis`.

    Computes the overlap of `q` with each basis state using the inner
    product (Dagger), then re-expresses the result in the computational
    basis with the basis-state index as the label.

    Example: change_basis(|0>, (|+>, |->)) rotates |0> to the X basis,
    giving the |+> component |0> and the |-> component |1>.

    :param q: single-qubit SymPy state to rotate
    :param new_basis: tuple (state_0, state_1) defining the target basis
    :return: SymPy qubit expression in the new basis
    """
    # Overlap with basis state 0 -> label it |0> in the new basis
    coeff_0 = qapply(Dagger(new_basis[0]) * q) * Qubit("0")
    # Overlap with basis state 1 -> label it |1> in the new basis
    coeff_1 = qapply(Dagger(new_basis[1]) * q) * Qubit("1")
    return coeff_0 + coeff_1
