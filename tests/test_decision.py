import pytest

from decision import (
    Azar, Decision, Terminal,
    hurwicz, laplace, matriz_arrepentimiento, maximax, maximin,
    perdida_oportunidad_esperada, savage, valor_esperado, veip,
)

PAGOS = [
    [200, 50, -20],
    [150, 100, 30],
    [80, 80, 80],
]
PROBS = [0.3, 0.5, 0.2]


def test_maximin():
    assert maximin(PAGOS) == (2, 80)


def test_maximax():
    assert maximax(PAGOS) == (0, 200)


def test_hurwicz_extremos():
    assert hurwicz(PAGOS, 0) == maximin(PAGOS)
    assert hurwicz(PAGOS, 1) == maximax(PAGOS)
    with pytest.raises(ValueError):
        hurwicz(PAGOS, 1.5)


def test_savage():
    assert matriz_arrepentimiento(PAGOS) == [[0, 50, 100], [50, 0, 50], [120, 20, 0]]
    assert savage(PAGOS) == (1, 50)


def test_laplace():
    i, v = laplace(PAGOS)
    assert i == 1 and v == pytest.approx(280 / 3)


def test_riesgo():
    i, ve = valor_esperado(PAGOS, PROBS)
    assert i == 1 and ve == pytest.approx(101)
    j, poe = perdida_oportunidad_esperada(PAGOS, PROBS)
    assert j == i
    assert veip(PAGOS, PROBS) == pytest.approx(poe)


def test_arbol():
    arbol = Decision({
        "Lanzar": Azar([(0.6, Terminal(500)), (0.4, Terminal(-300))]),
        "No lanzar": Terminal(0),
    })
    assert arbol.resolver() == pytest.approx(180)
    assert arbol.eleccion == "Lanzar"
