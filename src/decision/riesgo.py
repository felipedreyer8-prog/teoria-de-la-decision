"""Decisión bajo riesgo (probabilidades conocidas)."""

from .criterios import _mejor, matriz_arrepentimiento


def _validar(probs):
    if abs(sum(probs) - 1) > 1e-9 or any(p < 0 for p in probs):
        raise ValueError("las probabilidades deben ser no negativas y sumar 1")


def valor_esperado(pagos, probs):
    """Alternativa con mayor valor esperado: ``(indice, VE)``."""
    _validar(probs)
    return _mejor([sum(p * x for p, x in zip(probs, f)) for f in pagos])


def perdida_oportunidad_esperada(pagos, probs):
    """Alternativa con menor pérdida de oportunidad esperada: ``(indice, POE)``."""
    _validar(probs)
    r = matriz_arrepentimiento(pagos)
    return _mejor([sum(p * x for p, x in zip(probs, f)) for f in r], maximizar=False)


def veip(pagos, probs):
    """Valor esperado de la información perfecta."""
    _validar(probs)
    vecip = sum(p * max(col) for p, col in zip(probs, zip(*pagos)))
    return vecip - valor_esperado(pagos, probs)[1]
