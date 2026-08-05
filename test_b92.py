from testbook import testbook


@testbook("b92.ipynb", execute=True)
def test_0(tb):
    tb.ref("test_0")()


@testbook("b92.ipynb", execute=True)
def test_1(tb):
    tb.ref("test_1")()


@testbook("b92.ipynb", execute=True)
def test_2(tb):
    tb.ref("test_2")()


@testbook("b92.ipynb", execute=True)
def test_3(tb):
    tb.ref("test_3")()


@testbook("b92.ipynb", execute=True)
def test_4(tb):
    tb.ref("test_4")()


@testbook("b92.ipynb", execute=True)
def test_5(tb):
    tb.ref("test_5")()
