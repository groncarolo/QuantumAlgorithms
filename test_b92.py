from testbook import testbook


@testbook("b92.ipynb", execute=True)
def test_0(testbook):
    test = testbook.get("test_0")
    test()
