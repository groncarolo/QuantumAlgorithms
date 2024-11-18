from testbook import testbook


@testbook('teleportation.ipynb', execute=True)
def test_0(testbook):
    test = testbook.get('test_0')
    test()


@testbook('teleportation.ipynb', execute=True)
def test_1(testbook):
    test = testbook.get('test_1')
    test()


@testbook('teleportation.ipynb', execute=True)
def test_2(testbook):
    test = testbook.get('test_2')
    test()
