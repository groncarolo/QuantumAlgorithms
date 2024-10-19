from oracles.shor import shor


def test_shor_1():
    N = 15
    factors = shor(N, 2)
    print("factors = {factors}".format(factors=factors))
    truth = [3, 5]
    assert truth == sorted(factors)


def test_shor_2():
    N = 15
    factors = shor(N, 7)
    print("factors = {factors}".format(factors=factors))
    truth = [3, 5]
    assert truth == sorted(factors)

def test_shor_3():
    N = 15
    factors = shor(N, 13)
    print("factors = {factors}".format(factors=factors))
    truth = [3, 5]
    assert truth == sorted(factors)

def test_shor_4():
     N = 3*7
     factors = shor(N, 13)
     print("factors = {factors}".format(factors=factors))
     truth = [3, 7]
     assert truth == sorted(factors)
