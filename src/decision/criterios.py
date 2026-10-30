"""Criterios de decisión bajo incertidumbre.

Todas las funciones reciben una matriz de pagos (beneficios) como lista de filas:
una fila por alternativa y una columna por estado de la naturaleza.
Devuelven una tupla ``(indice_alternativa_optima, valor)``.
"""


def _mejor(valores, maximizar=True):
    elegir = max if maximizar else min
    valor = elegir(valores)
    return valores.index(valor), valor


def maximin(pagos):
    """Criterio de Wald (pesimista)."""
    return _mejor([min(fila) for fila in pagos])


def maximax(pagos):
    """Criterio optimista."""
    return _mejor([max(fila) for fila in pagos])


def hurwicz(pagos, alfa):
    """Criterio de Hurwicz con coeficiente de optimismo ``alfa`` en [0, 1]."""
    if not 0 <= alfa <= 1:
        raise ValueError("alfa debe estar entre 0 y 1")
    return _mejor([alfa * max(f) + (1 - alfa) * min(f) for f in pagos])


def matriz_arrepentimiento(pagos):
    """r_ij = max_k x_kj - x_ij."""
    mejores = [max(col) for col in zip(*pagos)]
    return [[m - x for m, x in zip(mejores, fila)] for fila in pagos]


def savage(pagos):
    """Criterio de Savage (minimax arrepentimiento)."""
    return _mejor([max(f) for f in matriz_arrepentimiento(pagos)], maximizar=False)


def laplace(pagos):
    """Criterio de Laplace (estados equiprobables)."""
    return _mejor([sum(f) / len(f) for f in pagos])
