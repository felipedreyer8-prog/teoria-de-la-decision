# 1. Introducción

La **teoría de la decisión** estudia cómo elegir entre alternativas cuando los resultados dependen de factores que el decisor no controla.

## Elementos de un problema de decisión

- **Decisor**: quien elige.
- **Alternativas** $a_1, \dots, a_m$: acciones posibles.
- **Estados de la naturaleza** $e_1, \dots, e_n$: situaciones que no controla el decisor, mutuamente excluyentes y exhaustivas.
- **Resultados / pagos** $x_{ij}$: consecuencia de elegir $a_i$ si ocurre $e_j$.
- **Matriz de pagos**: tabla $m \times n$ con los $x_{ij}$.

## Ambientes de decisión

| Ambiente | Información sobre los estados |
|---|---|
| Certeza | Se sabe qué estado ocurrirá |
| Riesgo | Se conocen las probabilidades de cada estado |
| Incertidumbre | No se conocen las probabilidades |
| Conflicto | Los estados los elige un oponente racional (teoría de juegos) |

## Dominancia

La alternativa $a_k$ **domina** a $a_i$ si $x_{kj} \ge x_{ij}$ para todo $j$, con desigualdad estricta en al menos un estado. Las alternativas dominadas se eliminan antes de aplicar cualquier criterio.
