from testbook import testbook

@testbook('simon.ipynb', execute=True)
def test_0(testbook):
    test = testbook.get('test_0')
    test()

@testbook('simon.ipynb', execute=True)
def test_1(testbook):
    test = testbook.get('test_1')
    test()

@testbook('simon.ipynb', execute=True)
def test_2(testbook):
    test = testbook.get('test_2')
    test()

@testbook('simon.ipynb', execute=True)
def test_3(testbook):
    test = testbook.get('test_3')
    test()

@testbook('simon.ipynb', execute=True)
def test_4(testbook):
    test = testbook.get('test_4')
    test()

@testbook('simon.ipynb', execute=True)
def test_5(testbook):
    test = testbook.get('test_5')
    test()