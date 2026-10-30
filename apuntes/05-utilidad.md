# 5. Teoría de la utilidad

El valor esperado monetario no siempre refleja las preferencias reales: las personas suelen ser **aversas al riesgo**.

## Axiomas de von Neumann–Morgenstern
Completitud, transitividad, continuidad e independencia. Si se cumplen, existe una función de utilidad $u$ tal que se prefiere la lotería con mayor **utilidad esperada**:
$$UE_i = \sum_j p_j\, u(x_{ij})$$

## Actitud frente al riesgo

| Actitud | Forma de $u$ | Equivalente cierto vs VE |
|---|---|---|
| Aversión | Cóncava | EC < VE |
| Neutralidad | Lineal | EC = VE |
| Propensión | Convexa | EC > VE |

**Prima de riesgo** = VE − EC.

## Construcción de la función de utilidad (método de la lotería estándar)
1. Asignar $u(\text{peor}) = 0$ y $u(\text{mejor}) = 1$.
2. Para cada resultado intermedio $x$, preguntar qué probabilidad $p$ hace indiferente recibir $x$ seguro o la lotería (mejor con $p$, peor con $1-p$).
3. Entonces $u(x) = p$.
