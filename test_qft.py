from testbook import testbook


@testbook('qft.ipynb', execute=True)
def test_0(testbook):
    test = testbook.get('test_0')
    test()


@testbook('qft.ipynb', execute=True)
def test_1(testbook):
    test = testbook.get('test_1')
    test()
