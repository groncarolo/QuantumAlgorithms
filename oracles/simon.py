""" This module implements Simons periodicity algorithm"""
from sympy.physics.quantum.qapply import qapply
from sympy.physics.quantum.qubit import Qubit, matrix_to_qubit, measure_partial
from sympy import Symbol, preorder_traversal, Xor, Or, And, satisfiable, Not, simplify
from sympy.physics.quantum import TensorProduct
from sympy.physics.quantum.represent import represent
from oracle import oracle
from util import hn


def find_req_on_f(c, ys):
    """
    Find requirements on f
    :param int c: number c
    :param tuple ys: range of values
    :returns collection of [(val, req) ... ]
    example:
    c= 0b101 ys=[0,1,...,7]
    returns  [(0, 5),(1, 4),...,(7, 2)]
    """
    xs = [y ^ c for y in ys]
    return zip(ys, xs)


def find_c(constraints):
    """
    Find c given the constraints
    :param tuple collection constraints:
    :returns int c
    example
    [(0, 0, 0), (0, 1, 0), (1, 0, 1), (1, 1, 1)]
    we create the equivalent expression
    ~b & ~(a ^ c) & (a | b | c) & ~(a ^ b ^ c)
    and solve for it
    """
    bit_num = len(constraints[0])

    # limit to 16 bits
    assert bit_num < 16
    for i in range(bit_num):
        Symbol(chr(ord('a') + i))

    # create the equivalent expression NOT( c_1 XOR c_2 XOR ... c_n-1)
    expressions = []
    for elem in constraints:
        expressions.append(Not(Xor(*[elem[i] * Symbol(chr(ord('a') + i)) for i in range(bit_num)])))

    # add final expression (c_1 OR c_2 OR ... c_n-1)
    # as we do not want a solution where all Cs are zero
    expressions.append(Or(*[Symbol(chr(ord('a') + i)) for i in range(bit_num)]))

    # put them in one
    fe = And(*expressions)
    # solve it
    models = satisfiable(fe, all_models=True)

    # find the equivalent number C (a collection of them)
    ret = []
    for model in models:
        model = sorted(model.items(), key=lambda item: item[0].name)
        r = 0
        n = bit_num - 1
        for d in model:
            r = r + d[1] * 2 ** n
            n = n - 1
        ret.append(r)
    # sort the results for ease of comparison
    return sorted(ret)


def simon(f, n):
    """
    Run Simon algorithm and return |x>*|y XOR f(x)>
    :param func f: oracle function
    :param int n: string length

    The problem:
    consider f {0,1}^n  -> f {0, 1}^n that is not known
    we are told that exists c = c0c1c2...cn-1
    such that for all string x, y belonging to {0,1}^n
    we have
    f(x) == f(y)  if and only if x = y XOR c

    The Solution:
                         +-----------------+
      |x>  |0>-/n--H*n---|                 |--/n--H*n---M |x>
                         |       U_f       |
      |y>  |0>-/n--------|                 |--/n--------  |y XOR f(x)>
                         +-----------------+
    """
    # apply H gate to both inputs
    x = qapply(hn(n) * Qubit('0' * n))
    print(f"|x>: {x}")
    y = Qubit('0' * n)
    print(f"|y>: {y}")
    xy = TensorProduct(x, y)
    print(f"|xy>: {xy}")
    xy = matrix_to_qubit(represent(xy))
    print(f"|xy>: {xy}")

    # apply oracle
    state = oracle(x, y, f)

    # apply H*m to the top bits
    state = simplify(qapply(hn(n, start=3) * state))
    print(f'State: {state}')

    # measure the first 3 bits
    measures = measure_partial(state, range(n))
    print(f'Measures: {measures}')

    constraints = []
    for m in measures:
        m_contr = []
        for arg in preorder_traversal(m[0]):
            if isinstance(arg, Qubit):
                m_contr.append(arg.qubit_values[:3])
        constraints.append(m_contr)

    # find c
    c = find_c(constraints[0])
    print(f'c: {c[0] :03b}')

    #  Find requirements on f(x)
    req = find_req_on_f(c[0], range(0, 2 ** 3))
    print(f'Req: {list(req)}')

    return state, measures, c, constraints[0], req
