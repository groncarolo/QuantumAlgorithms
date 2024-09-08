from sympy.physics.quantum.qubit import Qubit, matrix_to_qubit, IntQubit
from sympy.physics.quantum import TensorProduct
from sympy.physics.quantum.represent import represent
from util import get_qubit_size


#            +-----------------+
#   |x>  ----|                 |--- |x>
#            |       U_f       |
#   |y>  ----|                 |--- |y XOR f(x)>
#            +-----------------+
# |x, y> goes to |x, y XOR f(x)>

def oracle(x, y, f):
    c = TensorProduct(x, y)
    c = matrix_to_qubit(represent(c))

    y_dim = get_qubit_size(y)
    assert y_dim != 0

    r = 0
    for expr in c.args:
        ee = 1
        for e in expr.args:
            if isinstance(e, Qubit):
                qbit = e
            else:
                ee *= e
        x = qbit.qubit_values[0:qbit.dimension - y_dim]
        y = qbit.qubit_values[qbit.dimension - y_dim:]

        # get integer equivalent so we can XOR easily
        y_as_int = IntQubit(Qubit(*y)).as_int()
        xor = y_as_int ^ f(x)

        # nqubits=y_dim keeps the resulting qubit the correct size
        r += TensorProduct(ee * Qubit(*x), Qubit(IntQubit(xor, nqubits=y_dim)))
    #print(r)
    return matrix_to_qubit(represent(r))
