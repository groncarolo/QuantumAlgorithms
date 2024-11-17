from testbook import testbook

@testbook('berstein_vazirani.ipynb', execute=True)
def test(testbook):
    test = testbook.get('test_0')
    test()
