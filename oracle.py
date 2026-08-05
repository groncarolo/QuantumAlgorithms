"""Quantum oracle implementation for quantum algorithm simulations.

A quantum oracle is a reversible black-box that implements a classical
function f inside a quantum circuit.  It acts on a two-register state
|x>|y> and produces |x>|y XOR f(x)>:

    U_f |x>|y>  =  |x> |y XOR f(x)>

Circuit diagram
---------------

         +-----------+
  |x> ---|           |--- |x>
         |    U_f    |
  |y> ---|           |--- |y XOR f(x)>
         +-----------+

Why XOR?
--------
XOR (addition mod 2) keeps the operation reversible: applying U_f twice
returns to the original state because (y XOR f(x)) XOR f(x) = y.
Reversibility is required for quantum circuits.

Phase-kickback trick
--------------------
When the ancilla is set to |-> = (|0> - |1>) / sqrt(2) instead of |0>,
the XOR flips become phase flips:

    U_f |x>|->  =  (-1)^f(x) |x>|->

The ancilla state is unchanged; the phase (-1)^f(x) is "kicked back"
onto the query register.  This is the mechanism used by Deutsch,
Deutsch-Jozsa, Bernstein-Vazirani, and Simon's algorithm.

Numeric example (1-qubit query, f(x) = x)
------------------------------------------
    |x> = |0>,  |y> = |0>  ->  |0> |0 XOR f(0)> = |0> |0>   (f(0)=0)
    |x> = |1>,  |y> = |0>  ->  |1> |0 XOR f(1)> = |1> |1>   (f(1)=1)

Superposition example (Hadamard query, |y> = |0>)
-------------------------------------------------
    |x> = (|0> + |1>)/sqrt(2)

    U_f acting on the superposition:

    U_f (|0>+|1>)/sqrt(2) |0>
      = (U_f|0>|0> + U_f|1>|0>) / sqrt(2)
      = (|0>|f(0)>  +  |1>|f(1)>) / sqrt(2)

    For f(x)=x: = (|0>|0> + |1>|1>) / sqrt(2)   -- Bell state

Multi-bit example (2-qubit query, f(x) = x0 XOR x1)
----------------------------------------------------
    |x> = |10>,  |y> = |0>  ->  |10> |0 XOR f(10)> = |10> |1>
    |x> = |11>,  |y> = |1>  ->  |11> |1 XOR f(11)> = |11> |0>
"""

from sympy.physics.quantum.qubit import Qubit, matrix_to_qubit, IntQubit
from sympy.physics.quantum import TensorProduct
from sympy.physics.quantum.represent import represent
from util.util import get_qubit_size


def oracle(x, y, f, *args):
    """Apply the quantum oracle U_f to the state |x>|y>.

    Computes |x> |y XOR f(x)> for every basis state |x> in the
    superposition, preserving amplitudes.

    The implementation:
      1. Forms the combined register |x>|y> as a single qubit state.
      2. For each basis term, splits the qubit values into the x part
         (query, top qubits) and the y part (ancilla, bottom qubits).
      3. Evaluates f(x, *args) classically, XORs the result with y,
         and rebuilds the combined qubit.
      4. Converts back to a SymPy qubit expression.

    :param x: SymPy qubit state representing the query register |x>
    :param y: SymPy qubit state representing the ancilla register |y>
    :param f: classical oracle function f(x_bits, *args) -> int
    :param args: extra arguments forwarded to f (e.g. the secret string s)
    :return: SymPy qubit expression |x>|y XOR f(x)>

    Example (f = identity, 1-qubit query)::

        oracle(|0>, |0>, lambda x, : x[0])  ->  |00>  (0 XOR f(0)=0)
        oracle(|1>, |0>, lambda x, : x[0])  ->  |11>  (0 XOR f(1)=1)
    """
    # Step 1: combine |x> and |y> into a single (n+1)-qubit register
    combined = TensorProduct(x, y)
    combined = matrix_to_qubit(represent(combined))

    # Number of qubits in the ancilla register
    y_dim = get_qubit_size(y)
    assert y_dim != 0, "Ancilla register must have at least one qubit"

    result = 0

    if isinstance(combined, Qubit):
        # --- Pure basis state (no superposition) ---
        # Split: top qubits are x, bottom y_dim qubits are y
        x_bits = combined.qubit_values[0: combined.dimension - y_dim]
        y_bits = combined.qubit_values[combined.dimension - y_dim:]

        # Convert y to an integer for XOR, evaluate f, XOR together
        y_int = IntQubit(Qubit(*y_bits)).as_int()
        xor_val = y_int ^ f(x_bits, *args)

        # Rebuild |x>|y XOR f(x)> -- nqubits=y_dim preserves qubit width
        result = TensorProduct(
            Qubit(*x_bits),
            Qubit(IntQubit(xor_val, nqubits=y_dim))
        )
    else:
        # --- Superposition: iterate over each basis term ---
        for term in combined.args:
            # Each term is amplitude * |qubit_state>
            amplitude = 1
            qubit = None
            for factor in term.args:
                if isinstance(factor, Qubit):
                    qubit = factor
                else:
                    amplitude *= factor  # accumulate scalar amplitude

            # Split qubit values into x and y parts
            x_bits = qubit.qubit_values[0: qubit.dimension - y_dim]
            y_bits = qubit.qubit_values[qubit.dimension - y_dim:]

            # XOR the ancilla with f(x)
            y_int = IntQubit(Qubit(*y_bits)).as_int()
            xor_val = y_int ^ f(x_bits, *args)

            # Accumulate: amplitude * |x>|y XOR f(x)>
            result += TensorProduct(
                amplitude * Qubit(*x_bits),
                Qubit(IntQubit(xor_val, nqubits=y_dim))
            )

    # Convert the tensor-product expression back to a qubit state
    return matrix_to_qubit(represent(result))
