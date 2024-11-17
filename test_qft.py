from testbook import testbook

@testbook('qft.ipynb', execute=True)
def test(testbook):

    test = testbook.get('test')
    test()
