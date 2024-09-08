from sympy.physics.quantum.qapply import qapply
from sympy.physics.quantum.qubit import Qubit, matrix_to_qubit, measure_partial
from sympy import  Symbol, preorder_traversal
from sympy.physics.quantum import TensorProduct
from sympy.physics.quantum.represent import represent
from oracle import oracle
from sympy import Xor, Or, And, satisfiable, Not, simplify
from util import hn


# This code implements Simons periodicity algorithm
# The problem:
# consider f {0,1}^n  -> f {0, 1}^n that is not known
# we are told that exists c = c0c1c2...cn-1
# such that for all string x, y belonging to {0,1}^n
# we have
# f(x) == f(y)  if and only if x = y XOR c

#                      +-----------------+
#   |x>  |0>-/n--H*n---|                 |--/n--H*n---M |x>
#                      |       U_f       |
#   |y>  |0>-/n--------|                 |--/n--------  |y XOR f(x)>
#                      +-----------------+


def find_req_on_f(c, ys):
    xs = [y ^ c for y in ys]
    return zip(ys, xs)


def find_c(constraints):
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
    # apply H gate to both inputs
    x = qapply(hn(n) * Qubit('0' * n))
    print("|x>: {x}".format(x=x))
    y = Qubit('0' * n)
    print("|y>: {y}".format(y=y))
    xy = TensorProduct(x, y)
    print("|xy>: {xy}".format(xy=xy))
    xy = matrix_to_qubit(represent(xy))
    print("|xy>: {xy}".format(xy=xy))

    # apply oracle
    state = oracle(x, y, f)

    # apply H*m to the top bits
    state = simplify(qapply(hn(n, start=3) * state))
    print('\nState: {state}'.format(state=state))

    # measure the first 3 bits
    measures = measure_partial(state, range(n))
    print('\nMeasures: {m}'.format(m=measures))

    constraints = []
    for m in measures:
        m_contr = []
        for arg in preorder_traversal(m[0]):
            if isinstance(arg, Qubit):
                m_contr.append(  arg.qubit_values[:3] )
        constraints.append(m_contr)

    # find C
    c = find_c(constraints[0])
    print('\nc: {:03b}'.format(c[0]))

    #  Find requirements on f(x)
    req = find_req_on_f(c[0], range(0, 2 ** 3))
    print('\nReq: {req}'.format(req=list(req)))

    return state, measures, c, constraints[0], req
