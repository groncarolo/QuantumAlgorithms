from testbook import testbook


@testbook('grover.ipynb', execute=True)
def test_0(testbook):
    test = testbook.get('test_0')
    test()


@testbook('grover.ipynb', execute=True)
def test_1(testbook):
    test = testbook.get('test_1')
    test()
