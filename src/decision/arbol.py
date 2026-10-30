"""Árboles de decisión resueltos por inducción hacia atrás."""

from dataclasses import dataclass, field


@dataclass
class Terminal:
    valor: float

    def resolver(self):
        return self.valor


@dataclass
class Azar:
    """Nodo de azar: ``ramas`` es una lista de ``(probabilidad, nodo)``."""

    ramas: list

    def resolver(self):
        if abs(sum(p for p, _ in self.ramas) - 1) > 1e-9:
            raise ValueError("las probabilidades de un nodo de azar deben sumar 1")
        return sum(p * nodo.resolver() for p, nodo in self.ramas)


@dataclass
class Decision:
    """Nodo de decisión: ``opciones`` es un dict ``{nombre: nodo}``.

    Tras ``resolver()``, ``eleccion`` contiene el nombre de la rama óptima.
    """

    opciones: dict
    eleccion: str = field(default=None, init=False)

    def resolver(self):
        valores = {nombre: nodo.resolver() for nombre, nodo in self.opciones.items()}
        self.eleccion = max(valores, key=valores.get)
        return valores[self.eleccion]
