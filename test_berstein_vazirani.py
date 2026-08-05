from testbook import testbook


@testbook("berstein_vazirani.ipynb", execute=True)
def test_0(tb):
    tb.ref("test_0")()


@testbook("berstein_vazirani.ipynb", execute=True)
def test_1(tb):
    tb.ref("test_1")()


@testbook("berstein_vazirani.ipynb", execute=True)
def test_2(tb):
    tb.ref("test_2")()


@testbook("berstein_vazirani.ipynb", execute=True)
def test_3(tb):
    tb.ref("test_3")()


@testbook("berstein_vazirani.ipynb", execute=True)
def test_4(tb):
    tb.ref("test_4")()


@testbook("berstein_vazirani.ipynb", execute=True)
def test_5(tb):
    tb.ref("test_5")()
