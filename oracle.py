""" This module implements a quantum Oracle"""

from sympy.physics.quantum.qubit import Qubit, matrix_to_qubit, IntQubit
from sympy.physics.quantum import TensorProduct
from sympy.physics.quantum.represent import represent
from util.util import get_qubit_size


#            +-----------------+
#   |x>  ----|                 |--- |x>
#            |       U_f       |
#   |y>  ----|                 |--- |y XOR f(x)>
#            +-----------------+
# |x, y> goes to |x, y XOR f(x)>


def oracle(x, y, f, *args):
    """
    Execute and oracle function on |x>*|y> input and return |x>*|y XOR f(x)>

    :param func f: oracle function
    :param state x: |x> state
    :param state y: |y> state
    """
    c = TensorProduct(x, y)
    c = matrix_to_qubit(represent(c))

    y_dim = get_qubit_size(y)
    assert y_dim != 0

    r = 0

    if isinstance(c, Qubit):
        x = c.qubit_values[0 : c.dimension - y_dim]
        y = c.qubit_values[c.dimension - y_dim :]
        # get integer equivalent so we can XOR easily
        y_as_int = IntQubit(Qubit(*y)).as_int()
        xor = y_as_int ^ f(x, *args)
        r += TensorProduct(Qubit(*x), Qubit(IntQubit(xor, nqubits=y_dim)))
    else:
        for expr in c.args:
            ee = 1
            for e in expr.args:
                if isinstance(e, Qubit):
                    qbit = e
                else:
                    ee *= e
            x = qbit.qubit_values[0 : qbit.dimension - y_dim]
            y = qbit.qubit_values[qbit.dimension - y_dim :]

            # get integer equivalent so we can XOR easily
            y_as_int = IntQubit(Qubit(*y)).as_int()
            xor = y_as_int ^ f(x, *args)

            # nqubits=y_dim keeps the resulting qubit the correct size
            r += TensorProduct(ee * Qubit(*x), Qubit(IntQubit(xor, nqubits=y_dim)))

    return matrix_to_qubit(represent(r))
